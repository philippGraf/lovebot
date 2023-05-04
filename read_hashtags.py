from time import sleep
import os
import random

HASHTAG_FILE = "hashtags.txt"


def read_hashtag_from_terminal(filename, doublecheck=False):
    os.system("clear")
    while True:
        print("[Lovebot]: Bitte Hashtag eingeben.\n")
        data = input("Eingabe (Bestätige mit Enter): #")
        if data == "exit":
            sleep(1)
            print("[Lovebot]: Ich beende das Programm...")
            sleep(1)
            break
        save = True
        if doublecheck:
            save = False
            while True:
                sleep(1)
                print(
                    "\n[Lovebot]: Soll ich diesen Hashtag speichern?\n\n",
                    "#" + data,
                    "\n",
                )
                print("[Lovebot]: Ja = 'j', Nein = 'n'\n")

                check = input("Eingabe (Bestätige mit Enter): ")
                if check == "n":
                    break
                elif check == "j":
                    save = True
                    break
                else:
                    sleep(1)
                    print("\n[Lovebot]: Diese Eingabe verstehe ich nicht...")

        if not save:
            sleep(1)
            os.system("clear")
            continue

        sleep(1)
        print("\n[Lovebot]: Vielen Dank! Ich speichere deinen Hashtag...\n")
        sleep(1)
        for i in range(0, 100, 5):
            print(f"[Lovebot]: Hashtag speichern [{i} %]", end="\r")
            sleep(random.random() * 0.3)
        print("[Lovebot]: Hashtag speichern [100 %]\n")
        sleep(1)
        f = open(filename, "a")
        f.write(data + "\n")
        f.close()
        print("[Lovebot]: Ich habe deinen Hashtag gespeichert!\n")
        sleep(5)
        os.system("clear")


if __name__ == "__main__":
    read_hashtag_from_terminal(HASHTAG_FILE)
