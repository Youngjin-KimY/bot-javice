import os
import re
import requests
import urllib.parse

from flask import Flask, request
from slack_bolt import App, Say
from slack_bolt.adapter.flask import SlackRequestHandler

from config import config_by_name
from preprocessing import *

app_config = config_by_name[os.environ.get("JAVICE_ENV")]

token = app_config.token
signing_secret = app_config.signing_secret
naver_client_id = app_config.naver_client_id
naver_client_secret = app_config.naver_client_secret
naver_recognition_lang_client_id = app_config.naver_recognition_lang_client_id
naver_recognition_lang_client_secret = app_config.naver_recognition_lang_client_secret

app = Flask(__name__)

bolt_app = App(token=token, signing_secret=signing_secret)
handler = SlackRequestHandler(bolt_app)

@app.route("/javice/events", methods=["POST"])
def slack_events_check():
    # slack bot api가 확인하는 api route
    chk = handler.handle(request)
    return chk

@bolt_app.message("hello")
def greetings(payload: dict, say: Say):
    user = payload.get('user')
    say(f"Hi <@{user}>")

@bolt_app.message(re.compile("(hanna|한나)"))
def greetings(event:str, say: Say):
    print(event)
    say("한나님은 주인님의 완전 예쁜 여자친구이십니다.")

def do_lang_recognition(text : str):
    # curl "https://openapi.naver.com/v1/papago/detectLangs" \
    # - d "query=만나서 반갑습니다." \
    # - H "Content-Type: application/x-www-form-urlencoded; charset=UTF-8" \
    # - H "X-Naver-Client-Id: uLr6vM2Wc7WLizR2DlIv" \
    # - H "X-Naver-Client-Secret: R6lkPF9m2z" - v
    url = 'https://openapi.naver.com/v1/papago/detectLangs'
    headers = make_headers(naver_recognition_lang_client_id, naver_recognition_lang_client_secret)
    payloads = {
        "query": text,
    }
    payloads = urllib.parse.urlencode(payloads)

    ret_langcode = ''
    try:
        res = requests.post(url, data=payloads, headers=headers, timeout=5)
        result = dict(res.json())
        print(result)
        ret_langcode = result['langCode']
    except Exception:
        Say("error: "+result)

    return ret_langcode

@bolt_app.message(re.compile("(번|words)"))
def do_translation(event : dict, say: Say):
    text = str(event['text']).split(" ")[0]

    recognition_lang = do_lang_recognition(text)

    url = 'https://openapi.naver.com/v1/papago/n2mt'
    headers = make_headers(naver_client_id, naver_client_secret)

    payloads = {
        "source" : recognition_lang,
        "target": "ko",
        "text" : text
    }
    payloads = urllib.parse.urlencode(payloads)
    # print(payloads)
    try:
        res = requests.post(url, data = payloads, headers = headers, timeout = 5)
        res = dict(res.json())['message']['result']
        say("'"+res['translatedText'] + "' 입니다.")
    except KeyError:
        # print(res.json())
        say("error" + str(res.json()['errMessage']))
@app.route("/")
def test():
    ### page test
    return "hello test"

def createApp():
    app.run(debug=app_config.DEBUG, host="0.0.0.0")