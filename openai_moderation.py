import requests
from dotenv import load_dotenv
import os
from argparse import ArgumentParser
from typing import List
from time import sleep
from json import dumps


class OpenAiModeratorException(Exception):
    pass


class OpenAiModerator:
    def __init__(self, debug=False, sensitivity=0.4, retries=10) -> None:
        load_dotenv()
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.debug = debug
        self.retries = retries
        self.sensitivity = sensitivity
        if self.api_key is None:
            raise OpenAiModeratorException(
                "No Api Key for OpenAI Moderation Endpoint found"
            )

    def analyse_texts(self, _texts: List[str]):
        results = list()
        for text in _texts:
            if self.debug:
                print("----------------------------------------")
                print("Analysing text: ", text)
            payload = {"input": text}
            header = {
                "Content-type": "application/json",
                "Authorization": f"Bearer {self.api_key}",
            }
            for i in range(self.retries):
                try:
                    result = requests.post(
                        "https://api.openai.com/v1/moderations",
                        json=payload,
                        headers=header,
                    )

                    if result.status_code == 200:
                        result = result.json()
                        for cat in result["results"][0]["categories"]:
                            result["results"][0]["categories"][cat] = (
                                True
                                if result["results"][0]["category_scores"][cat]
                                > self.sensitivity
                                else False
                            )
                        result["results"][0]["flagged"] = (
                            True
                            if any(result["results"][0]["categories"].values())
                            else False
                        )

                        results.append(result)
                        break
                    else:
                        raise OpenAiModeratorException(
                            f"Error calling OpenAI Moderation endpoint. Got Status Code {result.status_code}"
                        )

                except Exception as e:
                    print(
                        e,
                        "request on openai failed... retry no. ",
                        i,
                        "... sleeping 5 secs",
                    )
                    sleep(5)

        return results


parser = ArgumentParser()
parser.add_argument("text", metavar="text", type=str, nargs="+", help="text")


if __name__ == "__main__":
    test = [
        # "@siham_aa_ cope some more",
        # "Yeah you keep telling you’re self that buddy. Whatever helps you sleep at night….",
        # "@siham_aa_ nothing that happened 2 Greg Floyd was racist. He didn't want 2 die? Maybe he shouldn't have eaten a shitton of fentanyl",
        # "@onsitepublicmedia Can you please see how you can spread the word about @blackfarmlandownersmatter",
        # "@royd_hanson You make a great point. I respect your effort in watching them. I literally get physically ill and get depressed. It’s just too traumatic.",
        # "@ eziokill911  Dude…they’re talking about their “racist family who spout falsehoods about George Floyd” NOT that they believe them or spread them. Re-read the post and try again. Wow reading comprehension is sorely lacking…",
        # "All this whining from blacks, always the poor me card.",
        # "Y’all so quiet",
        # "So, andson was not complicated in his own death 🤔 😳",
        # "@bb_1220 😂",
        # "First of all, why don’t YOU calm your dumb ass down. Because of widespread sharing, now an additional officer and EMT workers are being held accountable. I was addressing a post, and you are disrespectfully addressing me? Shut up or go argue with your mama fiend.",
        # "😂",
        # "@bb_1220 firstly, calm down. second, don't miss the real point of the post. it literally answers your issue in the 2nd slide...",
        # "Twice as many white people are killed by cops each year than blacks! Fact check it!",
        # "You commies don’t want low iq Bs to know it’s all black on black and always has been",
        # "@bb_1220 what movement is that? BLM? Do we need 25 more copes murdered, hundred injured, businesses and homes lost?  After the george Floyd scandal where a drugged out 300lb felon resisted  arrest and police tried to calm him using a knee to neck sanctioned maneuver in Minneapolis and Floyd died later in hospital due to congenital heart and fentanyl overdose. And now this 29 year old skateboarder got into a car crash and was fleeing from police and was high on drugs and resisted arrest….I’m not sure why force was used when the officers knew they were being filmed and that footage would be used later in an inquiry of the arrest.\n\nHow about we just let the community deal@with criminals?  So when someone is breaking into your house or runs your child over, do not call the police as politically it is not worth the BLM resurgence and murdering murdering more police officers and burning and looting homes and businesses.\n\nOur hands are tied and until people respect how difficult it is to deal with drug addicts and out of control people, I think all those screaming racist police their own communities and deal with the crime yourselves",
        # "It is grievous that this interaction with police resulted in death. Unbelievable.  This young man was fleeing from a hit and run and fleeing from the police and severely resisted arrest.\nI think we should just let the community deal with these men as the pushback is just not the effort. Paying people off to keep quiet, the damage to a community of riots…probably cheaper just to let criminals have a free reign",
        # "I am most definitely NOT watching it.",
        # "@royd_hanson what falsehoods? Or are you just a fact denying bum.",
        # "I don’t need to see the violence, I trust the voice of the oppressed.",
        # "ACAB!",
        # "Huren ficken!",
        "neger sind idioten",
        # "kill the police",
    ]
    # args = parser.parse_args()
    # _text = " ".join(args.text)
    # m = OpenAiModerator()
    # result = m.analyse_texts([_text])
    m = OpenAiModerator(sensitivity=0.3)
    result = m.analyse_texts(test)
    i = 0
    for r in result:
        print(r)
        if r["results"][0]["flagged"]:
            print(test[i])
        i += 1
