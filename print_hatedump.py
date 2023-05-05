from time import sleep
import os
from lovebot import HATE_DUMP

def print_hatedump():
    os.system('clear')
    while True:
        # Get all messages from file.
        f = open(HATE_DUMP, "r")
        # Read messages from file and remove the trailing '\n'.
        messages = [message[:-1] for message in f.readlines()]
        f.close()

        if not messages:
            print("[Lovebot]: Ich habe noch keine Hassbotschaft gefunden... \n")
            print(10)

        for message in messages:
            print("[Lovebot]: Diese Hassbotschaft habe ich heute gefunden: \n")
            print(1)
            print("'",message,"'\n")
            sleep(10)


if __name__ == '__main__':
    print_hatedump()