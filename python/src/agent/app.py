import asyncio
import json
from models.types import AssistantTool, Document
from services.assistantService import AssistantService
from services.webSearchService import WebSearchService
from prompts.assistant.understand import understand as understand_prompt

assistantService = AssistantService()
webSearchService = WebSearchService()   
tools: list[AssistantTool] = [
    AssistantTool( name='web_search', description='Use only when searching web results or scanning a specific domain (NOT the exact URL / subpage of the page such as /blog). (e.g., "search example.com for apps"). This tool uses Google search to scrape relevant website contents. NEVER use it when the user asks to load specific URLs.' ),
    AssistantTool( name='file_process', description='Use to load and process contents of a file/image from a given URL/path or to process a web search results. Can translate, summarize, synthesize, extract information, or answer questions about the file contents (answering is available for images too). No need to upload files before using this tool.' ),
    AssistantTool( name='upload', description='Use only for creating new files. Allows writing content and uploading it to receive a URL/path to the new file.' ),
    AssistantTool( name='answer', description='MUST be used as the final tool. Use to provide the final answer to the user, communicate results, or inform about limitations, missing data, or inability to complete the task.' ),
]

processors: list[AssistantTool] = [
    AssistantTool( name='translate', description='Use this tool to translate a given URL or path content to the target language. REQUIRED PARAMETERS: url or path, original_language, target_language.' ),
    AssistantTool( name='summarize', description='Use this tool to generate a summary of the given URL or path content. REQUIRED PARAMETERS: \'url or path\'.' ),
    AssistantTool( name='synthesize', description='Use this tool to synthesize the content of the given URL or path content. REQUIRED PARAMETERS: \'url or path\' and \'query\' that describes the synthesis.' ),
    AssistantTool( name='extract', description='Use this tool to extract specific information or content from a given URL or file path. This includes, but is not limited to: links, topics, concepts, article URLs, dates, or any other structured data. REQUIRED PARAMETERS: \'url or path\', \'extraction_type\' (e.g. "links", "recent article URL", "publication dates"), and \'description\' of the extraction.' ),
    AssistantTool( name='answer', description='Use this tool when you need to answer questions based on the content of a given document or image (URL or file path). This tool can interpret and respond to queries about the document\'s subject matter, facts, or visual content. REQUIRED PARAMETERS: \'url or path\', \'question\'.' )
]

async def query():

    conversation_uuid = "0"
    messages = [
        {"role": "user", "content": "Please extract all links in  https://softo.ag3nts.org"}
    ]
    plan_json = await assistantService.understand(messages, tools)
    print(json.dumps(plan_json, indent=4))

    context: list[Document] = []
    for step in plan_json["plan"]:
        if step["tool"] == "web_search":
            #web search
            #response = await webSearchService.search(step["query"], conversation_uuid)
            print("searching not implemented")
            pass
        elif step["tool"] == "file_process":
            #file process
            processes = await assistantService.process(step["query"], processors, context)
            await assistantService.process_document(processes, context)
            pass
        elif step["tool"] == "upload":
            #upload
            print("upload is not implemented")
            pass
        elif step["tool"] == "answer":
            #answer
            print("answer is not implemented")
            pass


if __name__ == "__main__":

    asyncio.run(query())
