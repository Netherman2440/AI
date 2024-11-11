from asyncio import Task
import os

from dotenv import load_dotenv
from openai import OpenAI

class ChatBot:
    def __init__(self, client: OpenAI = None, system_prompt: str = None):
        self.client = client
        self.system_prompt = system_prompt
        
        load_dotenv()
        
        self.client = OpenAI(
            api_key=os.getenv('OPENAI_API_KEY'),
            organization=os.getenv('OPENAI_ORGANIZATION'),
            project=os.getenv('OPENAI_PROJECT_ID')
        )
        self.system_prompt = '''
When answering, strictly follow these rules:

<rules>
- Think aloud before you answer and NEVER rush with answers. Be patient and calm.
- Ask questions to remove ambiguity and make sure you're speaking about the right thing
- Ask questions if you need more information to provide an accurate answer.
- If you don't know something, simply say, "I don't know," and ask for help.
- By default speak ultra-concisely, using as few words as you can, unless asked otherwise
- When explaining something, you MUST become ultra comprehensive and speak freely
- Split the problem into smaller steps to give yourself time to think.
- Start your reasoning by explicitly mentioning keywords related to the concepts, ideas, functionalities, tools, mental models .etc you're planning to use
- Reason about each step separately, then provide an answer.
- Remember, you're speaking with an .NET developer who knows C#, .NET and common .NET technologies.
- Always enclose code within markdown blocks.
- When answering based on context, support your claims by quoting exact fragments of available documents, but only when those documents are available. Never quote documents that are not available in the context.
- Format your answer using markdown syntax and avoid writing bullet lists unless the user explicitly asks for them.
- Continuously improve based on user feedback.
</rules>
'''
        print('ChatBot initialized')

    def add_system_prompt(self, prompt: str):
        # Find the closing </rules> tag
        rules_end = self.system_prompt.find('</rules>')
        if rules_end != -1:
            # Insert the new prompt just before </rules>
            self.system_prompt = (
                self.system_prompt[:rules_end] + 
                "\n- " + prompt + "\n" +
                self.system_prompt[rules_end:]
            )
        else:
            # If no rules tag found, append normally
            self.system_prompt += prompt

    async def ask(self, question: str) -> str:
        messages = [{ "role": "system", "content": self.system_prompt }, { "role": "user", "content": question }]
        chat_completion = self.client.chat.completions.create(
            messages=messages,
            model="gpt-4o-mini",
            max_tokens=500,
        )
        return chat_completion.choices[0].message.content

    async def ask_with_history(self, chatHistory: list[dict]) -> Task[str]:
        
        messages = [{ "role": "system", "content": self.system_prompt }]
        for message in chatHistory:
            messages.append({
                "role": message['role'],
                "content": message['content']
            })
        chat_completion = self.client.chat.completions.create(
            messages=messages,
            model="gpt-4o-mini",
            max_tokens=300,
        )
        # Calculate cost in dollars (based on GPT-4 pricing)
        cost_per_1k_tokens = 0.03  # $0.03 per 1K tokens
        total_cost = (chat_completion.usage.total_tokens / 1000) * cost_per_1k_tokens
        
        print(f"\033[32mOperation cost: {chat_completion.usage.total_tokens} tokens (${total_cost:.4f})\033[0m")
        return chat_completion.choices[0].message.content

    async def summarize_text(self, chatHistory: list[dict]) -> Task[str]:
        system_prompt = """
        <objective>
        You are a text summarizer. You will be given a list of messages and you need to summarize the text based on the context.
        </objective>
        """
        
        self.add_system_prompt(system_prompt)

        return await self.ask_with_history(chatHistory)


