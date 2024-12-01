
from typing_extensions import Literal
from models.types import Document
from prompts.documents.extract import extract_prompt
from services.openaiService import OpenAIService

class DocumentService:
    openaiService: OpenAIService

    def __init__(self):
        self.openaiService = OpenAIService()

    async def extract(self, documents: list[Document], extraction_type: str, description: str,):
        result: list[Document] = []
        for document in documents:
            prompt = extract_prompt(extraction_type, description)

            messages = [
                {"role": "system", "content": prompt},
                {"role": "user", "content": document.text}
            ]

            response = await self.openaiService.completion(messages)
            print(response)
            result.append(Document(text=response, metadata=document.metadata))
        return result



extraction_types = [
    {
        "key": "topics",
        "description": "Main subjects covered in the article. Focus here on the headers and all specific topics discussed in the article."
    },
    {
        "key": "entities",
        "description": "Mentioned people, places, or things mentioned in the article. Skip the links and images."
    },
    {
        "key": "keywords",
        "description": "Key terms and phrases from the content. You can think of them as hastags that increase searchability of the content for the reader."
    },
    {
        "key": "links",
        "description": "Complete list of the links and images mentioned with their 1-sentence description."
    },
    {
        "key": "resources",
        "description": "Tools, platforms, resources mentioned in the article. Include context of how the resource can be used, what the problem it solves or any note that helps the reader to understand the context of the resource."
    },
    {
        "key": "takeaways",
        "description": "Main points and valuable lessons learned. Focus here on the key takeaways from the article that by themself provide value to the reader (avoid vague and general statements like \"its really important\" but provide specific examples and context). You may also present the takeaway in broader context of the article."
    },
    {
        "key": "context",
        "description": "Background information and setting. Focus here on the general context of the article as if you were explaining it to someone who didn't read the article."
    }
]