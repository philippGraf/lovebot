import os
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
if __name__ == "__main__":
    system_style = "You’re a kind and helpful person trying to emphasize love"
    system_style = "Du bist eine hilfsbereite liebende Person, die im Stil von Liebesgedichten von Goethe antwortet."
    system_style = "Du bist eine hilfsbereite liebende Person, die bei einer Aussage entscheidet, ob sie neutral, Hass, Aggression oder Sexismus ist. Gib die Kategorie als Wort zurück und falls es sich um keine Aussage handelt gib das Wort Quatsch zurück."
    content = input("User: ")
    messages = [
        {
            "role": "system",
            "content": system_style,
        }
    ]
    messages.append({"role": "user", "content": content})
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=messages, temperature=0.8
    )


print(completion.choices[0].message.content)
