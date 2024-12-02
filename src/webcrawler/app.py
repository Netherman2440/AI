import asyncio
from dataclasses import dataclass
import json
import os
from services.openaiService import OpenAIService
from services.webSearchService import WebSearchService

from prompts.websearch.crawl import crawl_prompt
from prompts.documents.extract import extract_prompt
from prompts.documents.convert_links import convert_links_prompt
from prompts.websearch.verify_page import is_valid_page_prompt
webSearchService = WebSearchService()
aiService = OpenAIService()


    


async def start_crawl(url: str, output_file: str):
    response = await webSearchService.crawl_url(url=url)
    print(response)
    
    with open(os.path.join(os.path.dirname(__file__), output_file), "w") as f:
        json.dump(response, f, indent=4)

def get_init_crawl(init_file: str):
    with open(os.path.join(os.path.dirname(__file__), init_file), "r") as f:
        return json.load(f)

async def crawl( domain: str, init_file: str, output_file: str):
    
    init_crawl = get_init_crawl(init_file=init_file)

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
        is_valid = await is_valid_page(result["markdown"])
        if is_valid["is_trap"] == "yes":
            print(f"Skipping {result['metadata']['url']} because it is a trap")
            continue
        results.append(result)

    # Process all results instead of just one
    for result in results:
        print(f"Processing: {result['metadata']['url']}")
        print(result["markdown"])

        ai_response = await extract_links_from_text(result["markdown"])
        print(ai_response)
        extracted_links = await get_sub_pages(ai_response, domain)


        for link in extracted_links["links"]:
            # Check if the link appears in any of the results' metadata URLs
            link_exists = any(link["url"] == r["metadata"]["url"] for r in results)
            if not link_exists:
                # Handle new link here
                print(f'add new link: {link["url"]}')
                new_result = await create_crawl_result(link["url"])
                results.append(new_result)
            else:
                # Handle existing link here
                print(f"Link {link['url']} already exists in metadata URLs")

    print(results)

    with open(os.path.join(os.path.dirname(__file__), output_file), "w") as f:
        json.dump(results, f, indent=4)


async def extract_links_from_text(markdown: str):
    response = await aiService.completion(
            messages=[
                {"role": "system", "content": extract_prompt(extraction_type="links", description="all links from the user document")},
                {"role": "user", "content": markdown}
            ]
        )
    return response.choices[0].message.content
    
async def is_valid_page(markdown: str):
    response = await aiService.completion(
            messages=[
                {"role": "system", "content": is_valid_page_prompt()},
                {"role": "user", "content": markdown}
            ]
        )
    print(response.choices[0].message.content)
    return json.loads(response.choices[0].message.content)

async def get_sub_pages(ai_response: str, domain: str):
    response = await aiService.completion(
            messages=[
                {"role": "system", "content": convert_links_prompt(domain=domain)},
                {"role": "user", "content": ai_response}
            ]
        )
    print(response.choices[0].message.content)
    return json.loads(response.choices[0].message.content)

async def create_crawl_result(url:str):
    item = await webSearchService.scrape_url(url)
    result = {
            "markdown": item["markdown"],
            "metadata": {
                "url": item["metadata"]["url"],
                "title": item["metadata"]["title"],
                "description": item["metadata"]["description"]
            }
        }
    return result

if __name__ == "__main__":
    asyncio.run(crawl(domain="https://softo.ag3nts.org", init_file="softo_init_crawl.json", output_file="softo_final_result.json"))