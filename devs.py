import os
import openai
from dotenv import load_dotenv

# Załaduj zmienne środowiskowe z pliku .env
load_dotenv()

# Pobierz klucz API z zmiennych środowiskowych
openai.api_key = os.getenv("OPENAI_API_KEY")

def create_openai_request(prompt, model="gpt-3.5-turbo", max_tokens=150):
    """
    Funkcja do tworzenia zapytań do API OpenAI.
    
    :param prompt: Tekst zapytania
    :param model: Model GPT do użycia (domyślnie gpt-3.5-turbo)
    :param max_tokens: Maksymalna liczba tokenów w odpowiedzi
    :return: Odpowiedź od API OpenAI
    """
    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Wystąpił błąd: {str(e)}"

# Przykład użycia
if __name__ == "__main__":
    user_prompt = input("Wprowadź swoje zapytanie: ")
    result = create_openai_request(user_prompt)
    print(f"Odpowiedź API:\n{result}")
