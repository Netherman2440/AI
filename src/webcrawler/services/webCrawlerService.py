from typing import List, Dict
import json
import os
from services.openaiService import OpenAIService
from services.webSearchService import WebSearchService
from prompts.documents.extract import extract_prompt
from prompts.documents.convert_links import convert_links_prompt
from prompts.websearch.verify_page import is_valid_page_prompt
from models.types import CrawlResult, PageMetadata

class WebCrawlerService:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.web_service = WebSearchService()
        self.ai_service = OpenAIService()
        self.results: List[CrawlResult] = []

    def get_results(self) -> List[CrawlResult]:
        with open(os.path.join(os.path.dirname(__file__), "result.json"), "r") as f:
            data = json.load(f)
            return [
                CrawlResult(markdown=item["markdown"], metadata=PageMetadata(**item["metadata"])) for item in data
            ]

    async def crawl(self) -> None:
        """Main crawling function that processes initial results and follows links."""
        # First, get initial results from the base URL
        initial_response = await self.web_service.crawl_url(url=self.base_url)
        with open(os.path.join(os.path.dirname(__file__), "init.json"), "w") as f:
            json.dump(initial_response, f, indent=4)

        # Load and process results
        self.results = self._load_init_crawl()
        processed_results = []

        for result in self.results:
            if not await self._is_valid_page(result.markdown):
                print(f"Skipping {result.metadata.url} because it is a trap")
                continue
            
            processed_results.append(result)
            await self._process_page_links(result)

        self.results = processed_results
        self._save_results()

    async def _process_page_links(self, result: CrawlResult) -> None:
        """Extract and process links from a single page."""
        print(f"Processing: {result.metadata.url}")
        
        ai_response = await self._extract_links_from_text(result.markdown)
        extracted_links = await self._get_sub_pages(ai_response)
        
        await self._handle_new_links(extracted_links)

    async def _handle_new_links(self, extracted_links: Dict) -> None:
        """Process extracted links and crawl new ones."""
        for link in extracted_links["links"]:
            if not self._link_exists(link["url"]):
                print(f'Adding new link: {link["url"]}')
                new_result = await self._create_crawl_result(link["url"])
                self.results.append(new_result)
            else:
                print(f"Link {link['url']} already exists")

    def _link_exists(self, url: str) -> bool:
        """Check if a URL has already been processed."""
        return any(url == result.metadata.url for result in self.results)

    async def _is_valid_page(self, markdown: str) -> bool:
        """Check if a page is valid for processing."""
        response = await self.ai_service.completion(
            messages=[
                {"role": "system", "content": is_valid_page_prompt()},
                {"role": "user", "content": markdown}
            ]
        )
        result = json.loads(response.choices[0].message.content)
        return result["is_trap"] != "yes"

    async def _extract_links_from_text(self, markdown: str) -> str:
        """Extract links from markdown content."""
        response = await self.ai_service.completion(
            messages=[
                {"role": "system", "content": extract_prompt(extraction_type="links", description="all links from the user document")},
                {"role": "user", "content": markdown}
            ]
        )
        return response.choices[0].message.content

    async def _get_sub_pages(self, ai_response: str) -> Dict:
        """Convert extracted links to proper format."""
        response = await self.ai_service.completion(
            messages=[
                {"role": "system", "content": convert_links_prompt(domain=self.base_url)},
                {"role": "user", "content": ai_response}
            ]
        )
        return json.loads(response.choices[0].message.content)

    async def _create_crawl_result(self, url: str) -> CrawlResult:
        """Create a new crawl result from a URL."""
        item = await self.web_service.scrape_url(url)
        return CrawlResult(
            markdown=item["markdown"],
            metadata=PageMetadata(
                url=item["metadata"]["url"],
                title=item["metadata"]["title"],
                description=item["metadata"]["description"]
            )
        )

    def _load_init_crawl(self) -> List[CrawlResult]:
        """Load initial crawl results from file."""
        with open(os.path.join(os.path.dirname(__file__), "init.json"), "w") as f:
            data = json.load(f)
            return [
                CrawlResult(
                    markdown=item["markdown"],
                    metadata=PageMetadata(
                        url=item["metadata"]["url"],
                        title=item["metadata"]["title"],
                        description=item["metadata"]["description"]
                    )
                ) for item in data["data"]
            ]

    def _save_results(self) -> None:
        """Save processed results to file."""
        results_dict = [
            {
                "markdown": result.markdown,
                "metadata": {
                    "url": result.metadata.url,
                    "title": result.metadata.title,
                    "description": result.metadata.description
                }
            } for result in self.results
        ]
        
        with open(os.path.join(os.path.dirname(__file__), "result.json"), "w") as f:
            json.dump(results_dict, f, indent=4)