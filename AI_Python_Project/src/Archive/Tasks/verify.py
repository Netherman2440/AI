import sys
import os

# Dodaj ścieżkę do folderu src do sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from httpRequest import verify

async def main():
    answer = 'https://app.circle.so/rails/active_storage/representations/redirect/eyJfcmFpbHMiOnsibWVzc2FnZSI6IkJBaHBCUGRDeHdNPSIsImV4cCI6bnVsbCwicHVyIjoiYmxvYl9pZCJ9fQ==--3cb72337eaa977da391443424b3f607c50026c75/eyJfcmFpbHMiOnsibWVzc2FnZSI6IkJBaDdDRG9MWm05eWJXRjBTU0lJY0c1bkJqb0dSVlE2RkhKbGMybDZaVjkwYjE5c2FXMXBkRnNITUdrQ09BUTZDbk5oZG1WeWV3WTZDbk4wY21sd1ZBPT0iLCJleHAiOm51bGwsInB1ciI6InZhcmlhdGlvbiJ9fQ==--cfda350175ba87e768b4e96e935a8171fc679bec/openart-image_GIM52PCB_1731517844100_raw.png'

    response = await verify("robotid", answer)
    print(response)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())