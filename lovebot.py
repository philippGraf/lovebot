from dotenv import load_dotenv
import os
from instagrapi import Client
import json
from openai_moderation import OpenAiModerator
from hashtag_optimizer import HashtagOptimizer
from time import sleep
from argparse import ArgumentParser
from numpy import Inf
from collections import deque
import random
import pandas as pd
from utils import login_user
import os
from read_hashtags import HASHTAG_FILE
from read_messages import MESSAGE_FILE
from chat_gpt import LoveSpeech

HATE_DUMP = "hate_dump.txt"


if not os.path.exists(os.path.join(os.path.dirname(__file__), HATE_DUMP)):
    open(HATE_DUMP, "w+")

if not os.path.exists(os.path.join(os.path.dirname(__file__), HASHTAG_FILE)):
    open(HASHTAG_FILE, "w+")
    f = open(HASHTAG_FILE, "a")
    f.write("politik" + "\n")
    f.close()
if not os.path.exists(os.path.join(os.path.dirname(__file__), MESSAGE_FILE)):
    open(MESSAGE_FILE, "w+")
    f = open(MESSAGE_FILE, "a")
    f.write("Make Love not Hate!" + "\n")
    f.close()


def main(args):
    """the chat bot loop"""
    # load credentials and log in on instagram
    # client = login_user()
    if args.comment_chat_gpt:
        lovespeech = LoveSpeech()
    load_dotenv()
    USERNAME = os.getenv("INSTA_USER")
    PASSWORD = os.getenv("INSTA_PWD")
    client = Client()
    # adds a random delay between 2 and 4 seconds after each request
    client.delay_range = [2,4]
    client.login(USERNAME, PASSWORD)
    # -----------------------------------------------------
    # runtime arguments
    N_MEDIA = args.n_media
    if args.n_runs is None:
        N_RUNS = Inf
    else:
        N_RUNS = abs(args.n_runs)
    RUN = True
    loop_counter = 0
    comment = "make love" if not args.comment else args.comment
    # ------------------------------------------------------
    # load the hatespeach detector
    detector = OpenAiModerator(debug=args.debug)
    # ------------------------------------------------------
    # load the hashtag optimizer
    hashtag_optimizer = HashtagOptimizer()
    # ------------------------------------------------------

    selected_hashtag = args.hashtag

    # media_id buffer
    media_buffer = deque(maxlen=1000)
    ANALYSE_MEDIA = True
    top = True
    while RUN:
        # We read hashtags and messages inside the main loop
        # because other processes are adding both continuously.

        # Get Hashtag
        if not selected_hashtag:
            f = open(HASHTAG_FILE, "r")
            # Read hashtags from file and remove the trailing '\n'.
            all_hashtags = [hashtag[:-1] for hashtag in f.readlines()]
            f.close()
            # Let the hashtag optimizer select a hashtag.
            selected_hashtag = hashtag_optimizer.select_hashtag(all_hashtags)

        # Get all messages from file.
        f = open(MESSAGE_FILE, "r")
        # Read messages from file and remove the trailing '\n'.
        messages = [message[:-1] for message in f.readlines()]
        f.close()

        os.system("clear")
        print("[Lovebot]: Ich analysiere den Hashtag: ", "#" + selected_hashtag, "\n")
        sleep(1)
        if top:
            print(f"[Lovebot]: Ich durchsuche {N_MEDIA} beliebte Beiträge...\n")
            medias = client.hashtag_medias_top(selected_hashtag, amount=N_MEDIA)
        else:
            print(f"[Lovebot]: Ich durchsuche {N_MEDIA} aktuelle Beiträge...\n")
            medias = client.hashtag_medias_recent(
                selected_hashtag, amount=N_MEDIA
            )  # here it would be also possible to sample from related hashtags and to scan them also
        top = not top
        for media in medias:
            ANALYSE_MEDIA = True
            media_id = client.media_id(media.pk)
            try:
                media_buffer.index(media.pk)
                ANALYSE_MEDIA = False
            except ValueError as e:
                media_buffer.append(media.pk)
            if ANALYSE_MEDIA:
                comm_obs = client.media_comments(media_id=media_id, amount=100)
                sleep(args.sleep)
                comments = list(
                    pd.Series([comm.text for comm in comm_obs], dtype=str)
                    .drop_duplicates()
                    .values
                )  # dropping dulpicates!!!!

                # Analyse the received comments...
                analysis = detector.analyse_texts(comments)

                number_of_hate_comments = 0
                latest_hate_comment = None
                for j, x in enumerate(analysis):
                    if x["results"][0]["flagged"]:
                        number_of_hate_comments += 1
                        print("[Lovebot]: Ich habe potenzielle Hassrede gefunden: \n")
                        print("'", comments[j], "'\n")
                        latest_hate_comment = comments[j]
                        sleep(1)
                        print(
                            "[Lovebot]: Ich speichere potenzielle Hassrede unter ",
                            HATE_DUMP,
                            "...\n",
                        )
                        sleep(1)
                        with open(HATE_DUMP, "a") as file:
                            file.write(
                                "Hashtag: "
                                + selected_hashtag
                                + ": "
                                + comments[j]
                                + "\n"
                            )
                            file.close()

                # Here, we just comment on the post instead of replying to the actual hate comment.
                # Is this behaviour correct?
                if number_of_hate_comments > 0:
                    love_message = random.choice(messages)
                    if args.comment_chat_gpt:
                        if args.comment_chat_gpt:
                            love_message = lovespeech.reply(latest_hate_comment)

                    print(
                        "[Lovebot]: Ich sende eine Liebesbotschaft unter dem Beitrag,\n",
                        "           bei dem ich potenzielle Hassrede gefunden habe.\n",
                    )
                    sleep(1)
                    print("[Lovebot]: Ich sende die folgende Liebesbotschaft:\n")
                    sleep(1)
                    print("'", love_message, "'\n")
                    for perc in range(0, 100, 5):
                        print(f"[Lovebot]: Liebesbotschaft senden [{perc} %]", end="\r")
                        sleep(random.random() * 0.3)
                    client.media_comment(media_id=media_id, text=love_message)
                    print("[Lovebot]: Liebesbotschaft senden [100 %]\n")
                    sleep(1)
                else:
                    print("[Lovebot]: Ich habe keine Hassrede gefunden...\n")
                    sleep(1)

                print("[Lovebot]: Ich aktualisiere den Hashtag-Optimierer...\n")
                hashtag_optimizer.update(
                    all_hashtags, selected_hashtag, number_of_hate_comments
                )
                sleep(1)

        loop_counter += 1
        if loop_counter >= N_RUNS:
            RUN = False


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--n_runs", type=int, default=None)
    parser.add_argument("--n_media", type=int, default=10)
    parser.add_argument("--sleep", type=int, default=5)
    parser.add_argument("--hashtag", type=str, default=None)
    parser.add_argument("--debug", action="store_true")
    parser.add_argument("--comment", type=str, default=None)
    parser.add_argument("--comment_chat_gpt", action="store_true")
    args = parser.parse_args()
    main(args)
    # while True:
    #     try:
    #         main(args)
    #     except Exception as e:
    #         print(e)
    #         sleep(30)
