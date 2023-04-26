# lovebot
This is a little Art project. A little robot connecting to instagram and scanning posts for hate speech using the the moderation endpoint of chatgpt.

# How to set things up

First you need an instagram account. To enable the lovebot to login to your account write  your instagram credentials

INSTA_USER

INSTA_PWD

into the .env file. Moreover you need to connect to the moderation endpoint of openai. This is an public api, where you need to create an chatGPT account with an corresponding API Key 

OPENAI_API_KEY

which you should store in the .env file.

This is all you have to set up. Finally, as usual:
Create a virtual environment
```
python3 -m venv venv
```
activate it
```
source venv/bin/activate
```
and install the requirements
```
pip install -r requirements.txt
```
Then you may run lovebot inside the virtual environment
```
python lovebot.py
```

