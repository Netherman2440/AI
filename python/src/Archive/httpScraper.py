import json
import os

import dotenv
from httpRequest import post

class WebScraper:
    def __init__(self: str):
        dotenv.load_dotenv()
        self.api_key = os.getenv("FIRECRAWL_API_KEY")
        

async def scrape_website(self, url: str) -> str : 
    payload = {
        "url": url,
        "formats": ["markdown"],
        "onlyMainContent": True,
        "headers": {},
    }
    headers = {
        "Authorization": f"Bearer {self.api_key}",
        "Content-Type": "application/json"
    }

    scraper_url = "https://api.firecrawl.dev/v1/scrape"

    response = await post(scraper_url, payload, headers)
    response_json = json.loads(response.text)
    return response_json
    