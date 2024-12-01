from datetime import datetime
import json
import os
from urllib.parse import urlparse
from services.webSearchService import WebSearchService

MIME_TYPES = {
        "text": {
            "extensions": [".txt", ".md", ".json", ".html", ".csv"],
            "mimes": [
                "text/plain",
                "text/markdown", 
                "application/json",
                "text/html",
                "text/csv"
            ]
        },
        "audio": {
            "extensions": [".mp3", ".wav", ".ogg"],
            "mimes": [
                "audio/mpeg",
                "audio/wav", 
                "audio/ogg"
            ]
        },
        "image": {
            "extensions": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp"],
            "mimes": [
                "image/jpeg",
                "image/png",
                "image/gif", 
                "image/bmp",
                "image/webp"
            ]
        },
        "document": {
            "extensions": [".pdf", ".doc", ".docx", ".xls", ".xlsx"],
            "mimes": [
                "application/pdf",
                "application/msword",
                "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                "application/vnd.ms-excel", 
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            ]
        }
    }
class FileService:
    webSearchService: WebSearchService
    STORE_PATH = os.path.join(os.path.dirname(__file__), "..", "storage")
    def __init__(self):
        self.webSearchService = WebSearchService()

    def save(self, file_content, file_name, file_uuid, mime_type, source_url):
        date = datetime.now().strftime("%Y-%m-%d")
        file_path = f"{self.STORE_PATH}/{mime_type}/{date}/{file_uuid}"
        os.makedirs(file_path, exist_ok=True)

        #here do sth with mime type later


        with open(f"{file_path}/{file_name}", "wb") as file:
            file.write(file_content)
        return {
            mime_type,
            file_path,
            file_name,
            file_uuid
        }

    async def process(self,filePathOrUrl: str):
        if filePathOrUrl.startswith("http"):    
            result = await self.fetchUrl(filePathOrUrl)
            print(result)
            return result
        else:
            print("not http")

    async def fetchUrl(self, url: str):

        parsed_url = urlparse(url)
        file_name = os.path.basename(parsed_url.path) or ''
        possible_extension = file_name.split('.')[-1] if '.' in file_name else ''
        if possible_extension and '?' in possible_extension:
            file_name = file_name.split('?')[0]
        file_extension = os.path.splitext(file_name)[1].lower()


            # Jeśli URL nie wskazuje na plik z rozpoznawalnym rozszerzeniem, użyj web scrapingu
        if not file_extension:
            scraped_content = await self.webSearchService.scrape_urls([url])
            
            if scraped_content:

                content_dict = json.loads(scraped_content)
                content = content_dict["markdown"]
                file_name = f"{parsed_url.hostname}.md"
                file_content = content.encode('utf-8')

                saved_file = self.save(file_content, file_name, "uuid", 'text', url)
                return {"text":saved_file, 'mime_type': 'text/markdown'}
            else:
                raise ValueError('Failed to scrape content from the URL')


            pass

    
