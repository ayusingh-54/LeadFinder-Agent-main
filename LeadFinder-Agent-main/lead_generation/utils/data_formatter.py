from typing import List

class DataFormatter:
    @staticmethod
    def format_user_info_to_json(user_info_list: List[dict]) -> List[dict]:
        flattened_data = []
        
        for info in user_info_list:
            website_url = info["website_url"]
            for interaction in info["user_info"]:
                flattened_data.append({
                    "Website URL": website_url,
                    "Username": interaction.get("username", ""),
                    "Bio": interaction.get("bio", ""),
                    "Post Type": interaction.get("post_type", ""),
                    "Timestamp": interaction.get("timestamp", ""),
                    "Upvotes": interaction.get("upvotes", 0),
                    "Links": ", ".join(interaction.get("links", [])),
                    "Source": interaction.get("source", ""),
                    "Snippet": interaction.get("bio", ""),
                    "Confidence": interaction.get("confidence", "unknown"),
                    "Confidence Score": interaction.get("confidence_score", 0),
                    "Title": interaction.get("title", ""),
                })
        
        # Sort by confidence score (highest first)
        flattened_data.sort(key=lambda x: x.get("Confidence Score", 0), reverse=True)
        
        return flattened_data