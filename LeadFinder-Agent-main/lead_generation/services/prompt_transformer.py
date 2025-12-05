import os
from phi.agent import Agent
from phi.model.openai import OpenAIChat
from dotenv import load_dotenv

load_dotenv()

class PromptTransformer:
    @staticmethod
    def transform_query(user_query: str) -> str:
        agent = Agent(
            model=OpenAIChat(id="gpt-4o-mini", api_key=os.getenv('OPENAI_API_KEY')),
            system_prompt="""Transform detailed user queries into concise 3-4 word company descriptions.

Examples:
Input: "Generate leads for AI-powered customer support chatbots for e-commerce stores."
Output: "AI customer support chatbots"

Input: "Find people interested in voice cloning for audiobooks"
Output: "voice cloning technology"

Always focus on core product/service.""",
            markdown=True
        )
        
        response = agent.run(f"Transform query to 3-4 word description: {user_query}")
        return response.content