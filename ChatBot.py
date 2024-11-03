from asyncio import Task
import os

from dotenv import load_dotenv
from openai import OpenAI



class ChatBot:
    def __init__(self):
        load_dotenv()

        self.client = OpenAI(
            api_key=os.getenv('OPENAI_API_KEY'),
            organization=os.getenv('OPENAI_ORGANIZATION'),
            project=os.getenv('OPENAI_PROJECT_ID')
        )
    

    

    async def askAI(self, question: str, chatHistory: list[dict]) -> Task[str]:
        
        messages = []
        for message in chatHistory:
            messages.append({
                "role": message['role'],
                "content": message['content']
            })
        chat_completion = self.client.chat.completions.create(
            messages=messages,
            model="gpt-4o-mini",
            max_tokens=150,
        )
        # Calculate cost in dollars (based on GPT-4 pricing)
        cost_per_1k_tokens = 0.03  # $0.03 per 1K tokens
        total_cost = (chat_completion.usage.total_tokens / 1000) * cost_per_1k_tokens
        
        print(f"\033[32mOperation cost: {chat_completion.usage.total_tokens} tokens (${total_cost:.4f})\033[0m")
        return chat_completion.choices[0].message.content


        

