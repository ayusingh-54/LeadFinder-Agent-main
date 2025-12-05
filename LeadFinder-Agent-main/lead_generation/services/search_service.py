import os
import requests
from typing import List
from dotenv import load_dotenv

load_dotenv()


class SearchService:
    @staticmethod
    def search_for_urls(company_description: str, num_links: int = 3) -> List[str]:
        """
        Aggregate URLs from multiple sources in parallel-ish fashion:
        1. Firecrawl (if API key available)
        2. DuckDuckGo generic (any domain)
        3. DuckDuckGo site-specific: LinkedIn, Reddit, Twitter, GitHub, StackOverflow, Quora
        Returns deduplicated list up to num_links.
        """
        all_urls = []

        # Try Firecrawl first
        all_urls.extend(SearchService._search_firecrawl(company_description, num_links))

        # DuckDuckGo generic search (any domain)
        all_urls.extend(SearchService._search_duckduckgo_generic(company_description, num_links))

        # Site-specific searches for popular platforms
        sites = [
            "linkedin.com",
            "reddit.com",
            "twitter.com",
            "github.com",
            "stackoverflow.com",
            "quora.com",
        ]
        for site in sites:
            all_urls.extend(SearchService._search_duckduckgo_site(company_description, num_links, site=site))

        # Fallback directly to Quora search if nothing found
        if not all_urls:
            all_urls.extend(SearchService._search_quora_direct(company_description, num_links))

        # Dedupe and return more results (multiply requested to ensure variety)
        deduped = SearchService._dedupe(all_urls)
        # Return up to 3x requested to give more options from multiple sources
        return deduped[:max(num_links * 3, 10)]

    @staticmethod
    def _search_firecrawl(company_description: str, num_links: int) -> List[str]:
        try:
            url = "https://api.firecrawl.dev/v1/search"
            headers = {
                "Authorization": f"Bearer {os.getenv('FIRECRAWL_API_KEY')}",
                "Content-Type": "application/json"
            }
            payload = {
                "query": f"people looking for {company_description} services forums jobs posts",
                "limit": num_links,
                "lang": "en",
                "location": "United States",
                "timeout": 60000,
            }
            response = requests.post(url, json=payload, headers=headers, timeout=30)
            if response.status_code == 200:
                urls = [result.get("url") for result in response.json().get("data", []) if result.get("url")]
                return SearchService._dedupe(urls)[:num_links]
        except Exception as e:
            print(f"Firecrawl search failed: {e}")
        return []

    @staticmethod
    def _search_duckduckgo_generic(company_description: str, num_links: int) -> List[str]:
        """DuckDuckGo HTML search across the web (no site restriction)."""
        try:
            query = company_description.replace('"', '').replace("'", "").strip()
            url = "https://duckduckgo.com/html/"
            params = {"q": query}
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }
            resp = requests.post(url, data=params, headers=headers, timeout=10)
            if resp.status_code != 200:
                return []

            import re
            matches = re.findall(r'href="(https?://[^"\s]+)"', resp.text)
            cleaned = []
            for m in matches:
                if "duckduckgo.com/l/?uddg=" in m:
                    # decode redirect form
                    try:
                        import urllib.parse as up
                        parsed = up.parse_qs(up.urlparse(m).query)
                        target = parsed.get("uddg", [None])[0]
                        if target:
                            m = target
                    except Exception:
                        pass
                if m.startswith("http"):
                    cleaned.append(m.split('&')[0])
            cleaned = SearchService._dedupe(cleaned)
            return cleaned[:num_links]
        except Exception as e:
            print(f"DuckDuckGo generic search failed: {e}")
        return []

    @staticmethod
    def _search_duckduckgo(company_description: str, num_links: int) -> List[str]:
        """Lightweight HTML search without extra dependencies."""
        try:
            query = company_description.replace('"', '').replace("'", "").strip()
            url = "https://duckduckgo.com/html/"
            params = {"q": f"site:quora.com {query}"}
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }
            resp = requests.post(url, data=params, headers=headers, timeout=10)
            if resp.status_code != 200:
                return []

            import re
            matches = re.findall(r'href="(https?://[^"]+quora\.com[^"]+)"', resp.text)
            cleaned = [m.split('&')[0] for m in matches]
            cleaned = SearchService._dedupe(cleaned)
            return cleaned[:num_links]
        except Exception as e:
            print(f"DuckDuckGo search failed: {e}")
        return []

    @staticmethod
    def _search_duckduckgo_site(company_description: str, num_links: int, site: str) -> List[str]:
        """DuckDuckGo HTML search restricted to a specific site (e.g., linkedin.com)."""
        try:
            query = company_description.replace('"', '').replace("'", "").strip()
            url = "https://duckduckgo.com/html/"
            params = {"q": f"site:{site} {query}"}
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }
            resp = requests.post(url, data=params, headers=headers, timeout=10)
            if resp.status_code != 200:
                return []

            import re
            matches = re.findall(r'href="(https?://[^"\s]+)"', resp.text)
            cleaned = []
            for m in matches:
                if site not in m:
                    continue
                if "duckduckgo.com/l/?uddg=" in m:
                    try:
                        import urllib.parse as up
                        parsed = up.parse_qs(up.urlparse(m).query)
                        target = parsed.get("uddg", [None])[0]
                        if target and site in target:
                            m = target
                    except Exception:
                        pass
                if m.startswith("http"):
                    cleaned.append(m.split('&')[0])
            cleaned = SearchService._dedupe(cleaned)
            return cleaned[:num_links]
        except Exception as e:
            print(f"DuckDuckGo {site} search failed: {e}")
        return []

    @staticmethod
    def _search_quora_direct(company_description: str, num_links: int) -> List[str]:
        """Generate Quora search URLs directly as a final fallback."""
        try:
            clean_query = company_description.replace('"', '').replace("'", "").strip()
            search_terms = clean_query.split()[:4]

            base_urls = [
                f"https://www.quora.com/search?q={'+'.join(search_terms)}",
            ]

            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            search_url = f"https://www.quora.com/search?q={'+'.join(search_terms)}"

            try:
                response = requests.get(search_url, headers=headers, timeout=10, allow_redirects=True)
                if response.status_code == 200:
                    import re
                    question_pattern = r'href=\"(/[^\"?]+\??[^\"]*)\"'
                    matches = re.findall(question_pattern, response.text)

                    quora_urls = []
                    for match in matches:
                        if not any(x in match for x in ['profile', 'topic', 'search', 'about', 'contact']):
                            full_url = f"https://www.quora.com{match}" if match.startswith('/') else match
                            if full_url not in quora_urls and 'quora.com' in full_url:
                                quora_urls.append(full_url)

                    if quora_urls:
                        return quora_urls[:num_links]
            except Exception as e:
                print(f"Direct Quora search failed: {e}")

            return base_urls[:num_links]
        except Exception as e:
            print(f"Quora direct search failed: {e}")
        return []

    @staticmethod
    def _dedupe(urls: List[str]) -> List[str]:
        seen = set()
        unique = []
        for u in urls:
            if not u:
                continue
            if u in seen:
                continue
            seen.add(u)
            unique.append(u)
        return unique