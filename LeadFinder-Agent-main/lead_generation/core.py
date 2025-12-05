from .services.prompt_transformer import PromptTransformer
from .services.search_service import SearchService
from .services.extraction_service import ExtractionService
from .utils.data_formatter import DataFormatter
from typing import Optional, Dict, Any, List


def _placeholder_leads_from_urls(urls: List[str]) -> List[dict]:
    placeholders = []
    for url in urls:
        placeholders.append({
            "Website URL": url,
            "Username": "Potential Lead",
            "Bio": "Profile link collected; detailed data unavailable from this source.",
            "Post Type": "unknown",
            "Timestamp": "",
            "Upvotes": 0,
            "Links": url,
            "Source": "unknown",
            "Snippet": "No snippet available.",
            "Confidence": "low",
        })
    return placeholders


def generate_leads(user_query: str, num_links: int = 3) -> Optional[Dict[str, Any]]:
    try:
        # Transform query
        company_description = PromptTransformer.transform_query(user_query)
        print(f"Transformed query: {company_description}")

        # Search URLs
        urls = SearchService.search_for_urls(company_description, num_links)
        print(f"Found URLs: {urls}")

        if not urls:
            # Return empty result instead of None
            return {"urls": [], "user_data": []}

        # Extract user info
        user_info_list = ExtractionService.extract_user_info_from_urls(urls)
        print(f"Extracted {len(user_info_list)} user info entries")

        # Format data
        flattened_data = DataFormatter.format_user_info_to_json(user_info_list)

        # If we still have no data, create placeholders so UI can show something
        if not flattened_data:
            flattened_data = _placeholder_leads_from_urls(urls)

        return {
            "urls": urls,
            "user_data": flattened_data
        }
    except Exception as e:
        print(f"Error in generate_leads: {e}")
        return {"urls": [], "user_data": []}