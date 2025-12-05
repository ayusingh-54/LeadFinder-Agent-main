import os
import re
import requests
from typing import List
from datetime import datetime
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()


class ExtractionService:
    @staticmethod
    def extract_user_info_from_urls(urls: List[str]) -> List[dict]:
        user_info_list = []

        for url in urls:
            try:
                # Try Firecrawl extraction first
                extracted = ExtractionService._extract_with_firecrawl(url)

                # Fallback to scraping if Firecrawl fails
                if not extracted:
                    extracted = ExtractionService._extract_with_scraping(url)

                # If still nothing, create a minimal placeholder entry so UI shows something
                if not extracted:
                    extracted = [ExtractionService._placeholder_entry(url)]

                user_info_list.append({
                    "website_url": url,
                    "user_info": extracted
                })
            except Exception as e:
                print(f"Extraction failed for {url}: {e}")
                user_info_list.append({
                    "website_url": url,
                    "user_info": [ExtractionService._placeholder_entry(url)]
                })

        return user_info_list

    @staticmethod
    def _extract_with_firecrawl(url: str) -> List[dict]:
        try:
            from firecrawl import FirecrawlApp
            from ..schemas import QuoraPageSchema

            firecrawl_app = FirecrawlApp(api_key=os.getenv('FIRECRAWL_API_KEY'))
            response = firecrawl_app.extract(
                [url],
                {
                    'prompt': 'Extract user info from Quora posts',
                    'schema': QuoraPageSchema.model_json_schema(),
                }
            )

            if response.get('success'):
                interactions = response.get('data', {}).get('interactions', [])
                if interactions:
                    return interactions
        except Exception as e:
            print(f"Firecrawl extraction failed: {e}")
        return []

    @staticmethod
    def _extract_with_scraping(url: str) -> List[dict]:
        """Fallback extraction using lightweight HTML parsing."""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(url, headers=headers, timeout=10)

            if response.status_code != 200:
                return []

            soup = BeautifulSoup(response.text, "html.parser")

            title = soup.title.string.strip() if soup.title else "Lead source"
            meta_desc = ""
            meta = soup.find("meta", attrs={"name": "description"}) or soup.find("meta", attrs={"property": "og:description"})
            if meta and meta.get("content"):
                meta_desc = meta.get("content").strip()

            # Try to grab some meaningful text from headers/paragraphs
            header_texts = [h.get_text(strip=True) for h in soup.find_all(["h1", "h2", "h3"], limit=3)]
            paragraph = soup.find("p")
            para_text = paragraph.get_text(strip=True) if paragraph else ""

            snippet_parts = [meta_desc, *header_texts, para_text]
            snippet = next((part for part in snippet_parts if part), "" )
            snippet = snippet[:280] if snippet else "No detailed snippet available."

            # Collect links on the page for context
            links = []
            for a in soup.find_all("a", href=True):
                href = a["href"]
                if href.startswith("http") and len(links) < 5:
                    links.append(href)
            if not links:
                links = [url]

            domain = ExtractionService._get_domain(url)
            post_type = ExtractionService._detect_post_type(url, domain)
            username = ExtractionService._extract_username_from_url(url)

            # Calculate confidence score based on data quality
            confidence_score, confidence_label = ExtractionService._calculate_confidence(
                snippet=snippet,
                username=username,
                domain=domain,
                title=title,
                meta_desc=meta_desc,
                links=links
            )

            interactions = [{
                "username": username,
                "bio": snippet,
                "post_type": post_type,
                "timestamp": datetime.now().isoformat(),
                "upvotes": 0,
                "links": links,
                "source": domain,
                "confidence": confidence_label,
                "confidence_score": confidence_score,
                "title": title[:100] if title else ""
            }]

            return interactions
        except Exception as e:
            print(f"Scraping failed: {e}")
        return []

    @staticmethod
    def _detect_post_type(url: str, domain: str) -> str:
        """Detect post type based on URL patterns."""
        url_lower = url.lower()
        if "linkedin.com" in domain:
            if "/in/" in url_lower:
                return "profile"
            if "/jobs/" in url_lower:
                return "job"
            if "/company/" in url_lower:
                return "company"
            return "linkedin"
        if "reddit.com" in domain:
            return "discussion"
        if "twitter.com" in domain or "x.com" in domain:
            return "tweet"
        if "github.com" in domain:
            return "repo"
        if "stackoverflow.com" in domain:
            return "question"
        if "quora.com" in domain:
            return "question"
        return "page"

    @staticmethod
    def _extract_username_from_url(url: str) -> str:
        """Best-effort username/entity extraction from common patterns."""
        try:
            parts = url.split('/')
            domain = ExtractionService._get_domain(url)

            # LinkedIn: /in/username or /company/name
            if "linkedin.com" in domain:
                for i, part in enumerate(parts):
                    if part in ('in', 'company') and i + 1 < len(parts):
                        return parts[i + 1].replace('-', ' ').title()

            # Reddit: /r/subreddit or /user/username
            if "reddit.com" in domain:
                for i, part in enumerate(parts):
                    if part in ('r', 'user') and i + 1 < len(parts):
                        return parts[i + 1]

            # Twitter/X: /@handle or /handle
            if "twitter.com" in domain or "x.com" in domain:
                for part in parts:
                    if part and part != "status" and not part.isdigit():
                        return f"@{part}"

            # GitHub: /username/repo
            if "github.com" in domain:
                if len(parts) > 3:
                    return parts[3]

            # Generic patterns
            for i, part in enumerate(parts):
                if part in ('profile', 'user', 'u', 'answer', 'p') and i + 1 < len(parts):
                    return parts[i + 1].replace('-', ' ')

            # fallback to domain
            return domain
        except Exception:
            return "unknown"

    @staticmethod
    def _get_domain(url: str) -> str:
        try:
            return urlparse(url).netloc or "unknown"
        except Exception:
            return "unknown"

    @staticmethod
    def _calculate_confidence(snippet: str, username: str, domain: str, title: str, meta_desc: str, links: List[str]) -> tuple:
        """
        Calculate confidence score (0-100) based on data quality.
        Returns (score, label) tuple.
        """
        score = 0

        # Has meaningful snippet (not placeholder)
        if snippet and len(snippet) > 50 and "unavailable" not in snippet.lower():
            score += 25
        elif snippet and len(snippet) > 20:
            score += 15

        # Has extracted username (not just domain)
        if username and username != domain and username != "unknown":
            score += 20

        # Has title
        if title and len(title) > 10:
            score += 15

        # Has meta description
        if meta_desc and len(meta_desc) > 30:
            score += 15

        # Has multiple links (indicates rich page)
        if links and len(links) >= 3:
            score += 10
        elif links and len(links) >= 1:
            score += 5

        # Bonus for trusted domains
        trusted_domains = ["linkedin.com", "github.com", "stackoverflow.com", "reddit.com"]
        if any(td in domain for td in trusted_domains):
            score += 15

        # Determine label
        if score >= 70:
            label = "high"
        elif score >= 45:
            label = "medium"
        else:
            label = "low"

        return (score, label)

    @staticmethod
    def _placeholder_entry(url: str) -> dict:
        domain = ExtractionService._get_domain(url)
        return {
            "username": "Potential Lead",
            "bio": "Profile link collected; detailed data unavailable from this source.",
            "post_type": "unknown",
            "timestamp": datetime.now().isoformat(),
            "upvotes": 0,
            "links": [url],
            "source": domain,
            "confidence": "low",
            "confidence_score": 10,
            "title": ""
        }