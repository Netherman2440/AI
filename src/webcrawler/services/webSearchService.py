import json
import os
from urllib.parse import urlparse
from dotenv import load_dotenv
import httpx
from prompts.websearch.askDomains import prompt as askDomainsPrompt
from models.types import Domain, Query
from firecrawl import FirecrawlApp
from openai.types.chat import ChatCompletionMessageParam
from services.openaiService import OpenAIService


allowed_domains: list[Domain] = [
    Domain(name="Wikipedia", url="wikipedia.org", scrappable=True),
    Domain(name="easycart", url="easy.tools", scrappable=True),
    Domain(name="FS.blog", url="fs.blog", scrappable=True),
    Domain(name="arXiv", url="arxiv.org", scrappable=True),
    Domain(name="Instagram", url="instagram.com", scrappable=False),
    Domain(name="OpenAI", url="openai.com", scrappable=True),
    Domain(name="Brain overment", url="brain.overment.com", scrappable=True),
    Domain(name="Reuters", url="reuters.com", scrappable=True),
    Domain(name="MIT Technology Review", url="technologyreview.com", scrappable=True),
    Domain(name="Youtube", url="youtube.com", scrappable=False),
    Domain(name="Mrugalski / UWteam", url="mrugalski.pl", scrappable=True),
    Domain(name="overment", url="brain.overment.com", scrappable=True),
    Domain(name="Hacker News", url="news.ycombinator.com", scrappable=True),
    Domain(name="IMDB", url="imdb.com", scrappable=True),
    Domain(name="TechCrunch", url="techcrunch.com", scrappable=True),
    Domain(name="Hacker News Newest", url="https://news.ycombinator.com/newest", scrappable=True),
    Domain(name="TechCrunch Latest", url="https://techcrunch.com/latest", scrappable=True),
    Domain(name="OpenAI News", url="https://openai.com/news", scrappable=True),
    Domain(name="Anthropic News", url="https://www.anthropic.com/news", scrappable=True),
    Domain(name="DeepMind Press", url="https://deepmind.google/about/press", scrappable=True),
    Domain(name="Softo", url="softo.ag3nts.org", scrappable=True),
]


class WebSearchService:
    allowed_domains: list[Domain]
    firecrawl_app: FirecrawlApp
    openaiService: OpenAIService

    def __init__(self):
        load_dotenv()
        self.allowed_domains = allowed_domains
        self.api_key = os.getenv("FIRECRAWL_API_KEY")
        self.firecrawl_app = FirecrawlApp(api_key=self.api_key)
        self.openaiService = OpenAIService()
        pass
    
    async def search(self, query: str, conversation_uuid: str):
        queries = await self.generate_queries(query)
        await self.search_web(queries, conversation_uuid)

        


        return queries
    

    async def scrape_url(self, url: str):
        return self.firecrawl_app.scrape_url(url, {'formats': ['markdown']})

    async def scrape_urls(self, urls: list[str]):
        results = []
        for url in urls:
            raw_result = self.firecrawl_app.scrape_url(url, {'formats': ['markdown']})
            print(json.dumps(raw_result, indent=4))
            results.append(raw_result)
        return results
        

    async def map_url(self, url: str):
        if not url.startswith(("http://", "https://")):
            url = f"https://{url}"
        domain = urlparse(url).netloc.replace("www.", "")
        map_result = self.firecrawl_app.map_url(domain, params= {

        })
        print(json.dumps(map_result, indent=4))
        return map_result


    async def crawl_url(self, url: str):
        if not url.startswith(("http://", "https://")):
            url = f"https://{url}"
        domain = urlparse(url).netloc.replace("www.", "")
        site_query = f'{domain}/'
        print(site_query)

        crawl_result = self.firecrawl_app.crawl_url(site_query,params={
            'limit': 10, 
            'scrapeOptions': {'formats': ['markdown']}
        })
        print(json.dumps(crawl_result, indent=4))
        return crawl_result

    async def crawl(self, query: Query, conversation_uuid: str):
        url = query.url
        if not url.startswith(("http://", "https://")):
            url = f"https://{url}"
                    
        domain = urlparse(url).netloc.replace("www.", "")
        site_query = f'{domain}/{query.q}'
        print(site_query)
        async with httpx.AsyncClient() as client:
            response = await client.post(
                'https://api.firecrawl.dev/v0/search',
                headers={
                            'Authorization': f'Bearer {self.api_key}',
                            'Content-Type': 'application/json'
                        },
                        json={
                            'query': site_query,
                            'searchOptions': {'limit': 6},
                            'pageOptions': {'fetchPageContent': False}
                        }
                    )
                    
        result = response.json()    
        print(json.dumps(result, indent=4))
        return result
    
    async def search_web(self, queries: list[Query], conversation_uuid: str):
        for query in queries:
            await self.crawl(query, conversation_uuid)
        pass
    
    async def generate_queries(self, query: str):
        messages: ChatCompletionMessageParam = [
            {"role": "system", "content": askDomainsPrompt(self.allowed_domains)},
            {"role": "user", "content": query}
        ]
        response = await self.openaiService.completion(messages, jsonMode=True)
        response = json.loads(response.choices[0].message.content)
        queries = [Query(q=query["q"], url=query["url"]) for query in response["queries"]]

        #todo: filter queries by allowed_domains

        return queries

    