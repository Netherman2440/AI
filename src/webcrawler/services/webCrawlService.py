import asyncio
import json
import os
from services.openaiService import OpenAIService
from services.webSearchService import WebSearchService

from prompts.documents.extract import extract_prompt    
from prompts.documents.convert_links import convert_links_prompt
from prompts.websearch.verify_page import is_valid_page_prompt
webSearchService = WebSearchService()
aiService = OpenAIService()


class WebCrawlService:
    def __init__(self):
        self.webSearchService = WebSearchService()
        self.aiService = OpenAIService()

    async def start_crawl(self, domain: str):
        page_name = self.extract_page_name(domain)
        output_file = f"{page_name}_init.json"
        response = await self.webSearchService.crawl_url(url=domain)
        print(response)
        
        # Navigate up two levels (from services to webcrawler) and then into results directory
        results_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "results")
        # Create results directory if it doesn't exist
        os.makedirs(results_dir, exist_ok=True)
        # Save file in the results directory
        output_path = os.path.join(results_dir, output_file)
        with open(output_path, "w") as f:
            json.dump(response, f, indent=4)

    def get_init_crawl(self, init_file: str):
        results_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "results")
        init_path = os.path.join(results_dir, init_file)
        with open(init_path, "r") as f:
            return json.load(f)

    async def crawl(self, domain: str):
        page_name = self.extract_page_name(domain)
        init_file = f"{page_name}_init.json"
        output_file = f"{page_name}_result.json"
        
        init_crawl = self.get_init_crawl(init_file=init_file)
        print(init_crawl)
        results = []

        for item in init_crawl["data"]:
            result = {
                "markdown": item["markdown"],
                "metadata": {
                    "url": item["metadata"]["url"],
                    "title": item["metadata"]["title"],
                    "description": item["metadata"]["description"]
                }
            }
            is_valid = await self.is_valid_page(result["markdown"])
            if is_valid["is_trap"] == "yes":
                print(f"Skipping {result['metadata']['url']} because it is a trap")
                continue
            results.append(result)

        # Process all results instead of just one
        for result in results:
            print(f"Processing: {result['metadata']['url']}")
            print(result["markdown"])

            ai_response = await self.extract_links_from_text(result["markdown"])
            print(ai_response)
            extracted_links = await self.get_sub_pages(ai_response, domain)


            for link in extracted_links["links"]:
                # Check if the link appears in any of the results' metadata URLs
                link_exists = any(link["url"] == r["metadata"]["url"] for r in results)
                if not link_exists:
                    # Handle new link here
                    print(f'add new link: {link["url"]}')
                    new_result = await self.create_crawl_result(link["url"])
                    results.append(new_result)
                else:
                    # Handle existing link here
                    print(f"Link {link['url']} already exists in metadata URLs")

        print(results)

        # Navigate up two levels and into results directory
        results_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "results")
        os.makedirs(results_dir, exist_ok=True)
        output_path = os.path.join(results_dir, output_file)
        with open(output_path, "w") as f:
            json.dump(results, f, indent=4)

    def extract_page_name(self, domain: str) -> str:
        # Remove 'http://' or 'https://' and any trailing slashes
        domain = domain.replace('http://', '').replace('https://', '').rstrip('/')
        # Extract the main part of the domain
        return domain.split('.')[0]

    async def extract_links_from_text(self, markdown: str):
        response = await self.aiService.completion(
                messages=[
                    {"role": "system", "content": extract_prompt(extraction_type="links", description="all links from the user document")},
                    {"role": "user", "content": markdown}
                ]
            )
        return response.choices[0].message.content
    
    async def is_valid_page(self, markdown: str):
        response = await self.aiService.completion(
                messages=[
                    {"role": "system", "content": is_valid_page_prompt()},
                    {"role": "user", "content": markdown}
                ]
            )
        print(response.choices[0].message.content)
        return json.loads(response.choices[0].message.content)

    async def get_sub_pages(self, ai_response: str, domain: str):
        response = await self.aiService.completion(
                messages=[
                    {"role": "system", "content": convert_links_prompt(domain=domain)},
                    {"role": "user", "content": ai_response}
                ]
            )
        print(response.choices[0].message.content)
        return json.loads(response.choices[0].message.content)

    async def create_crawl_result(self, url:str):
        item = await self.webSearchService.scrape_url(url)
        result = {
                "markdown": item["markdown"],
                "metadata": {
                    "url": item["metadata"]["url"],
                    "title": item["metadata"]["title"],
                    "description": item["metadata"]["description"]
                }
            }
        return result

    def get_result(self, domain: str):
        page_name = self.extract_page_name(domain)
        result_file = f"{page_name}_result.json"
        
        results_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "results")
        result_path = os.path.join(results_dir, result_file)
        
        try:
            with open(result_path, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"No result file found for domain: {domain}")
            return None
