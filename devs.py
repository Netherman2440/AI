from asyncio import Task
import os
from openai import OpenAI
from dotenv import load_dotenv
import asyncio

# Load environment variables from .env file
load_dotenv()

client = OpenAI(
    api_key=os.getenv('OPENAI_API_KEY'),
    organization=os.getenv('OPENAI_ORGANIZATION'),
    project=os.getenv('OPENAI_PROJECT_ID')
)

async def askAI(question) -> Task[str]:
    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": question},
        ],
        model="gpt-3.5-turbo",
        max_tokens=150,
    )
    return chat_completion.choices[0].message.content

if __name__ == "__main__":
    async def main():
        while True:
            user_input = input("Enter your question (or 'exit' to quit): ")
            if user_input.lower() == "exit":
                break
            response = await askAI(user_input)
            print(response)

    asyncio.run(main())
