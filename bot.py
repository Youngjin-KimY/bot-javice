import re
import requests
import urllib.parse

from flask import Flask, request
from slack_bolt import App, Say
from slack_bolt.adapter.flask import SlackRequestHandler

token = os.environ.get("SLACK_BOT_TOKEN")
signing_secret = os.environ.get("SLACK_SIGNING_SECRET")
naver_client_id = os.environ.get("NAVER_CLIENT_ID")
naver_client_secret = os.environ.get("NAVER_CLIENT_SECRET")
naver_recognition_lang_client_id = os.environ.get("NAVER_RECOGNITION_LANG_CLIENT_ID")
naver_recognition_lang_client_secret = os.environ.get("NAVER_RECOGNITION_LANG_CLIENT_SECRET")


app = Flask(__name__)
bolt_app = App(token=token, signing_secret=signing_secret)
handler = SlackRequestHandler(bolt_app)

@app.route("/javice/events", methods=["POST"])
def slack_events_check():
    # slack bot api가 확인하는 api route
    chk = handler.handle(request)
    return chk

@bolt_app.message("hello javice")
def greetings(payload: dict, say: Say):
    user = payload.get('user')
    say(f"Hi <@{user}>")

@bolt_app.message(re.compile("(hanna|한나)"))
def greetings(event:str, say: Say):
    print(event)
    say("한나님은 주인님의 완전 예쁜 여자친구이십니다.")

def make_headers(id : str, secret : str):
    return {
        "Content-Type": "application/x-www-form-urlencoded",
        "charset": "UTF-8",
        "X-Naver-Client-Id": id,
        "X-Naver-Client-Secret": secret
    }

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
    res = requests.post(url, data=payloads, headers=headers, timeout=5)
    result = dict(res.json())

    return result['langCode']

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
    res = requests.post(url, data = payloads, headers = headers, timeout = 5)
    res = dict(res.json())['message']['result']

    say("'"+res['translatedText'] + "' 입니다.")

@app.route("/")
def test():
    ### page test
    return "hello test"

if __name__ == '__main__':
    # start server : typing "python3 bot.py" in termial
    # ./ngrok http 5000
    app.run(debug=True, host="0.0.0.0")
