import os
import openai
from dotenv import load_dotenv


DEFAULT_SYSTEM_STYLE = (
    "Du bist eine einfühlsamer Roboter, der jeglichen Hass in Liebe verwandeln möchte."
)


class LoveSpeech:
    def __init__(
        self, system_style: str = DEFAULT_SYSTEM_STYLE, temperature: float = 0.8
    ) -> None:
        load_dotenv()
        openai.api_key = os.getenv("OPENAI_API_KEY")
        self.system_style = system_style
        self.temperature = temperature

    def reply(self, content: str):
        messages = [
            {
                "role": "system",
                "content": self.system_style,
            }
        ]
        messages.append({"role": "user", "content": content})
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=messages, temperature=self.temperature
        )
        return completion.choices[0].message.content


if __name__ == "__main__":
    system_style = "You’re a kind and helpful person trying to emphasize love"
    system_style = "Du bist eine hilfsbereite liebende Person, die im Stil eines liebestollen Roboter antwortet und allen Hass in Liebe verwandeln möchte."
    system_style = "Du bist eine hilfsbereite liebende Person, die bei einer Aussage entscheidet, ob sie neutral, Hass, Aggression oder Sexismus ist. Gib die Kategorien nur als Wörter zurück und falls es sich um keine Aussage handelt gib nur das Wort Quatsch zurück."
    system_style = "Du entscheidest bei einer Aussage, ob diese liebevoll. Ist die Aussage liebevoll antwortest du mit dem Wort 'liebevoll' ansonsten mit dem Wort 'whatever'"
    content = input("User: ")
    lovespeech = LoveSpeech(system_style=system_style)
    comment = lovespeech.reply(content=content)
    print(comment)
