import asyncio
from services.webCrawlService import WebCrawlService
from services.openaiService import OpenAIService
from services.aidevs import Aidevs  
crawler = WebCrawlService()
openai_service = OpenAIService()
aidevs = Aidevs()

crawl_result = crawler.get_result(domain="softo.ag3nts.org")
print(crawl_result)

async def get_questions():
    response = await aidevs.get("https://centrala.ag3nts.org/data/TUTAJ-KLUCZ/softo.json")
    return response 

async def question(question: str):
    response = await openai_service.completion(
        messages=[
        {"role": "system", "content": f"""Your task is to answer the user query about the provided website content.
         Answer in Polish. Answer with only the answer, no additional text. If user asks for a name of a company, answer with the name of the company.
         If user asks for an email, answer with the email address.
         If user asks for a URL, answer with the URL.
        The website content is: 
         {crawl_result}
        """},
        {"role": "user", "content": question}
        ]
    )
    
    return response.choices[0].message.content


questions = asyncio.run(get_questions())
print(questions)
async def aidevs_answer():
    responses = []
    answer = await question(questions['01'])
    responses.append(answer)
    answer = await question(questions['02'])
    responses.append(answer)
    answer = await question(questions['03'])
    responses.append(answer)

    final_response = {
        '01': responses[0],
        '02': responses[1],
        '03': responses[2],
    }

    return final_response
response = {"01": "kontakt@softoai.whatever", "02": "Adres interfejsu webowego do sterowania robotami zrealizowanego dla firmy BanAN to: https://banan.ag3nts.org", "03": "Firma SoftoAI zdoby\u0142a certyfikaty ISO 9001 oraz ISO/IEC 27001."}
final_response = asyncio.run(aidevs_answer())

verify = asyncio.run(aidevs.verify(task_id='softo', answer=final_response))
print(verify)