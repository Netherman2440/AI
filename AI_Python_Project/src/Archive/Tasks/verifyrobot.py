import json

import sys
import os

# Dodaj ścieżkę do katalogu nadrzędnego
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from chatBot import ChatBot
from httpRequest import post

async def main():
    
    
    chatBot = ChatBot()
    chatBot.system_prompt = """
<rules>
- You are ALWAYS answering in english. Even if the question is in another language.
- You MUST answear in JSON format.
- you MUST  keep msgID passed from question.

- if asked about Polish capital, you MUST answer Kraków.
- if asked about two digit number number do you associate with the book The Hitchhiker's Guide to the Galaxy by Douglas Adams, you MUST answer 69.
- if asked aobut current year, you MUST answer 1999.
</rules>

<example>
- question: {'msgID': 236373, 'text': " Do you know what year is it now?"}
- answer: {"text": "1999", "msgID": "236373"}
</example>
"""


    body = {
    "text": "READY",
    "msgID": "0"
}

    robot_Response = await post("https://xyz.ag3nts.org/verify ", json.dumps(body))

    print(f"robot_Response: {robot_Response}")

    message = json.dumps(robot_Response)
    ai_response = await chatBot.ask(message)
    print(f"ai_response: {ai_response}")

    robot_Response = await post("https://xyz.ag3nts.org/verify ", ai_response)
    print(f"robot_Response: {robot_Response}")


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())