from dotenv import load_dotenv
import os
from instagrapi import Client
import json
from openai_moderation import OpenAiModerator
from time import sleep
from argparse import ArgumentParser
from numpy import Inf
from collections import deque
from random import choice
import pandas as pd
from utils import login_user

def main(args):
    """the chat bot loop"""
    # load credentials and log in on instagram
    client = login_user()
    # -----------------------------------------------------
    # runtime arguments
    N_MEDIA = args.n_media
    if args.n_runs is None:
        N_RUNS = Inf
    else:
        N_RUNS = abs(args.n_runs)
    RUN = True
    i = 0
    # ------------------------------------------------------
    # load the hatespeach detector
    detector = OpenAiModerator()
    # --------------------------------------------------------
    # load the config with hashtags and possible answers per hashtag etc ....
    love_config = json.load(open("lovebot_config.json", "r"))
    # media_id buffer
    media_buffer = deque(maxlen = 1000)
    ANALYSE_MEDIA = True
    while RUN:
        for hashtag in love_config["hashtags"]:
            print("**************************************************")
            print("analysing hashtag: ", hashtag)
            print("**************************************************")
            print(f"Getting {N_MEDIA} posts..." )
            medias = client.hashtag_medias_recent(hashtag, amount=N_MEDIA) # here it would be also possible to sample from related hashtags and to scan them also
            # sleep(args.sleep)
            for media in medias:
                media_id = client.media_id(media.pk)
                try:
                    media_buffer.index(media.pk)
                    ANALYSE_MEDIA = False
                except ValueError as e:
                    media_buffer.append(media.pk)
                if ANALYSE_MEDIA:
                    comm_obs = client.media_comments(media_id=media_id,amount= 10)
                    comments = list(pd.Series([comm.text for comm in comm_obs]).drop_duplicates().values()) # dropping dulpicates!!!!
                    analysis = detector.analyse_texts(comments)
                    any_hate = any([x['results'][0]['flagged'] for x in analysis])
                    # sleep(args.sleep)
                    for j, x in enumerate(analysis):
                        if x['results'][0]['flagged']:
                            print("writing possible hate comment to hate_dump.txt...:")
                            print("--------------------------------------------------")
                            print(comments[j])
                            print("--------------------------------------------------")
                            print("--------------------------------------------------")
                            with open('hate_dump.txt',"a") as file:
                                file.write("hashtag: " +  hashtag + ": " + comments[j] + "\n")
                    if any_hate:
                        comment  = choice(love_config["hashtags"][hashtag]['answers'])
                        print(f"replying to media with id {media_id}, since hate speech was found in comments.\nThe reply is:\n{comment} ")
                        client.media_comment(media_id=media_id, text=comment)
                
                ANALYSE_MEDIA = True
                media
            

                            

        i+=1
        if i>= N_RUNS:
            RUN = False





if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--n_runs",type=int, default=None)
    parser.add_argument("--n_media",type=int, default=10)
    parser.add_argument("--sleep",type=int, default=5)
    args  = parser.parse_args()
    main(args)

