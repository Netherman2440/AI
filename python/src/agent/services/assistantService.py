import json
from services.fileService import FileService
from services.documentService import DocumentService
from services.openaiService import OpenAIService

from prompts.assistant.understand import understand as understand_prompt
from prompts.assistant.process import process as process_prompt
from models.types import AssistantTool, Document, Plan, Action


from openai.types.chat import ChatCompletionMessageParam

class AssistantService:
    def __init__(self):
        self.openaiService = OpenAIService()
        self.documentService = DocumentService()
        self.fileService = FileService()
    async def understand(self, messages: list[ChatCompletionMessageParam],tools: list[AssistantTool]):
        response = await self.openaiService.completion( messages = [{
            "role": "system",
            "content": understand_prompt(tools)
        },
        *messages],
        jsonMode=True
        )

        return json.loads(response.choices[0].message.content)
    
    async def web_search(self, query: str):
        pass
    async def process(self, query: str, processors: list[AssistantTool], documents: list[Document]):
        response = await self.openaiService.completion( messages = [{
            "role": "system",
            "content": process_prompt(processors, documents)
        },{
            "role": "user",
            "content": query
        }],
        jsonMode=True
        )
        json_result = json.loads(response.choices[0].message.content)
        
        return [Action(**result) for result in json_result["process"]]
    
    async def process_document(self, process: list[Action], context: list[Document])->list[Document]:

        result: list[Document] = []
       

        for action in process:

            source = action.url
            documents = await self.fileService.process(source)
            match action.type:
                case "extract":
                    response = await self.documentService.extract(documents, action.extraction_type, action.description)
                    print(response)
                    result.extend(response)
                case "answer":
                    print('answer not implemented')
                    pass
                case "translate":
                    print('translate not implemented')
                    pass
                case "summarize":
                    print('summarize not implemented')
                    pass
                case "synthesize":
                    print('synthesize not implemented')
                    pass
        return result
