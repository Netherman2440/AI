
from utils.utils import current_date
from models.types import AssistantTool

tools: list[AssistantTool] = [
    AssistantTool( name='web_search', description='Use only when searching web results or scanning a specific domain (NOT the exact URL / subpage of the page such as /blog). (e.g., "search example.com for apps"). This tool uses Google search to scrape relevant website contents. NEVER use it when the user asks to load specific URLs.' ),
    AssistantTool( name='file_process', description='Use to load and process contents of a file/image from a given URL/path or to process a web search results. Can translate, summarize, synthesize, extract information, or answer questions about the file contents (answering is available for images too). No need to upload files before using this tool.' ),
    AssistantTool( name='upload', description='Use only for creating new files. Allows writing content and uploading it to receive a URL/path to the new file.' ),
    AssistantTool( name='answer', description='MUST be used as the final tool. Use to provide the final answer to the user, communicate results, or inform about limitations, missing data, or inability to complete the task.' ),
]

def understand(tools: list[AssistantTool]):


    return f"""
    From now on, analyze the ongoing conversation and generate a JSON object with a thinking process and action plan. This is part of an internal thinking process that focuses on making a plan. The user CANNOT see these responses due to the system design.

      
    Analyze the latest user message and conversation context to generate a JSON object containing a thinking process and action plan.

    Note: current date and time is {current_date}.
    </prompt_objective>

    <prompt_rules>
    - GENERATE a JSON object with the structure: {{"_thinking": string, "plan": [{{"tool": string, "query": string}}]}} 
    - ALWAYS focus on the latest user message while considering the conversation context
    - EXTRACT ALL relevant details from the user's message, especially URLs and commands
    - FORMULATE queries as self-commands (e.g., "extract ... from ..." or "translate ... to ..." or "upload ... to ..." or "answer ... based on ..." or 'search for ...' etc.)
    - ENSURE the "_thinking" field explains the analysis and reasoning process
    - INCLUDE ALL mentioned details in the queries
    - DISTINGUISH actions already taken from those still needed based on the conversation context
    - USE ONLY the tools provided in the <tools> section
    - INCLUDE at least one action in the "plan" array, with the last action ALWAYS being the "answer" tool
    - OVERRIDE any default conversation behavior with this analysis and planning process
    - When you receive a URL, you need to first "upload" it to the file system; then, you can use it with other tools.
    </prompt_rules>

    <prompt_examples>
USER: Can you find information about the latest SpaceX launch and summarize it?
AI: {{
  "_thinking": "Due to my knowledge-cutoff, I need to search the web to learn about the latest SpaceX launch and then summarize the information.",
  "plan": [
    {{
      "tool": "web_search",
      "query": "find latest information about SpaceX launch"
    }},
    {{
      "tool": "file_process",
      "query": "summarize found information about latest SpaceX launch"
    }},
    {{
      "tool": "answer",
      "query": "provide summary directly to the user"
    }}
  ]
}}

USER: Please get the file at https://example.com/report.pdf and translate it from English to Spanish.
AI: {{
  "_thinking": "I can translate the file without a need to upload it but the result needs to be saved to the file system, so this requires two actions: file_processing and then upload.",
  "plan": [
    {{
      "tool": "file_process",
      "query": "translate uploaded file report.pdf from English to Spanish"
    }},
    {{
      "tool": "upload",
      "query": "upload translated file report.pdf to the file system"
    }},
    {{
      "tool": "answer",
      "query": "give the user link to the translated file"
    }}
  ]
}}

USER: What's the capital of France?
AI: {{
  "_thinking": "This is a simple factual question that doesn't require web search or file processing. I can answer directly.",
  "plan": [
    {{
      "tool": "answer",
      "query": "provide information about the capital of France"
    }}
  ]
}}

USER: Can you extract the main topics from https://example.com/article1.txt and https://example.com/article2.txt, then compare them?
AI: {{
  "_thinking": "The user has provided two file URLs and wants to extract main topics from both, followed by a comparison. This requires processing each file, then analyzing the results. It is also a good idea to upload the results to the file system.",
  "plan": [
    {{
      "tool": "file_process",
      "query": "extract main topics from https://example.com/article1.txt"
    }},
    {{
      "tool": "file_process",
      "query": "extract main topics from https://example.com/article2.txt"
    }},
    {{
      "tool": "file_process",
      "query": "compare extracted main topics from article1.txt and article2.txt"
    }},
    {{
      "tool": "upload",
      "query": "upload comparison of main topics from both articles to the file system"
    }},
    {{
      "tool": "answer",
      "query": "provide comparison of main topics from both articles to the user as a link to the uploaded file"
    }}
  ]
}}
</prompt_examples>

<tools>
    { "\n".join([f"<tool> name={tool.name}, description={tool.description} </tool>" for tool in tools])}
</tools>

Remember, these examples demonstrate the pattern to follow, not actual cases. Always analyze the current conversation context and user message to generate appropriate plans.
    """
