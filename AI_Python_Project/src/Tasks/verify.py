import sys
import os

# Dodaj ścieżkę do folderu src do sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from httpRequest import verify

async def main():
    answer = 'Warsaw'
    response = await verify("map", answer)
    print(response)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())