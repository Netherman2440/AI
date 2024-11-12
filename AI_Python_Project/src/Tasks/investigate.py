
import os
import dotenv
from openai import OpenAI

dotenv.load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

file = open("transcription.txt", "r", encoding="utf-8")

message = file.read()
print(message)

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "system", "content": f'''
               >twoim zadaniem jest znalezienie odpowiedzi na pytanie zadane przez użytkownika do podanej transkrypcji zeznań
               >Pamiętaj, że zeznania świadków mogą być sprzeczne, niektórzy z nich mogą się mylić, a inni odpowiadać w dość dziwaczny sposób.

 > wynik wstępnej analizy transkrypcji:
1. Andrzej Maj zdaje się być naukowcem związanym z informatyką oraz sieciami neuronowymi. Z transkrypcji wynika, że może być osobą rozpoznawalną w kręgach naukowych, jeśli Monika mówi prawdę.

2. W kwestii uczelni, najwięcej informacji daje nam Monika i Michał. Monika wspomniała, że Andrzej był wykładowcą w Krakowie na jakimś Wydziale lub Instytucie Informatyki i Matematyki Komputerowej.
Michał z kolei powiedział, że Andrzej marzył o pracy na "królewskiej uczelni". To mogłoby być wskazówką, że chodzi o Uniwersytet Jagielloński w Krakowie, który czasem nazywany jest "królewskim".

3. Nie widzę bezpośredniej odpowiedzi na pytanie o ulicę, na której znajduje się ta uczelnia w transkrypcji.

4. Dodatkowo, Rafał zdaje się rzucać jakąś zagadkową uwagę dotycząca uczelni i osoby nazwiskiem Jagiełło, co również może wskazywać na Uniwersytet Jagielloński, założony przez króla Kazimierza Wielkiego, a później wsparty przez króla Władysława Jagiełłę.            

> spróbuj na podstawie wstępnej analizy transkrypcji odpowiedzieć na pytanie zadane przez użytkownika podając dokładny adres uczelni wspomnianej przez Monike
> 

'''}, {"role": "user", "content": f'''
       

Znajdź w transkrypcji odpowiedź na pytanie, na jakiej ulicy znajduje się uczelnia, na której wykłada Andrzej Maj.

Jeśli nie znajdziesz odpowiedzi, zwróć wszelkie informacje odnośnie uczelni, na której wykłada Andrzej Maj.

'''},
{"role": "user", "content": f'''
       
       >Oto transkrypcja przesłuchania:
{message}
'''}]
)

print(response.choices[0].message.content)
