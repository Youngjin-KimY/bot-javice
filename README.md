# _**javice in Slack**_

_this is personal slack bot, especially helping me find meanings of English and Mandarine words. and I will add several functions._

## Tech

---
_python3(=3.8.9)_

_flask(=2.0.2)_

_slack-sdk(=3.11.2)_

_slack-bolt(=1.10.0)_

_docker(=20.10.11)_

_ngrok(2.3.40)_

---

## How to start

---

## _**setting env**_
1. it is bad idea that token is on the code
   1. recommendation : token **must** be saved as **ENV**
      1. prod / dev flag : this code is divided as `prod` or `dev`
         1. you can understand if you check `config.py` file
      2. slack token
         1. `SLACK_BOT_TOKEN`
         2. `SLACK_SIGNING_SECRET`
      3. naver token
         1. `NAVER_CLIENT_ID`
         2. `NAVER_CLIENT_SECRET`
            1. above two tokens for Language translation api
         3. `NAVER_RECOGNITION_LANG_CLIENT_ID`
         4. `NAVER_RECOGNITION_LANG_CLIENT_SECRET`
            1. above two tokens for Language detection api
   

### **_not using docker_**

1. start server
   1. typing "python3 bot.py" in termial
   ```buildoutcfg
        python3 bot.py
   ```
   1. ternaling
   ```
      ./ngrok http {FLAKS PORT}
    ```


### **_using docker_**

1. need to set environment variables in server
   1. slack tokens and papago api tokens
2. build docker image
   1. ```buildoutcfg 
      docker build 
      --build-arg SLACK_BOT_TOKEN=$SLACK_BOT_TOKEN 
      --build-arg SLACK_SIGNING_SECRET=$SLACK_SIGNING_SECRET 
      --build-arg DEV_SLACK_BOT_TOKEN=$DEV_SLACK_BOT_TOKEN 
      --build-arg DEV_SLACK_SIGNING_SECRET=$DEV_SLACK_SIGNING_SECRET 
      --build-arg NAVER_CLIENT_ID=$NAVER_CLIENT_ID 
      --build-arg NAVER_CLIENT_SECRET=$NAVER_CLIENT_SECRET 
      --build-arg NAVER_RECOGNITION_LANG_CLIENT_ID=$NAVER_RECOGNITION_LANG_CLIENT_ID 
      --build-arg NAVER_RECOGNITION_LANG_CLIENT_SECRET=$NAVER_RECOGNITION_LANG_CLIENT_SECRET 
      --build-arg JAVICE_ENV=$JAVICE_ENV -t dev-bot-javice .
      ```
      
   1. ```buildoutcfg
      docker run -p {SERVER PORT}}:{FLASK SERVER PORT IN DOCKER CONTAINER}} bot-javice 
      # ex. -p 8000:5000 (from container 5000 to server 8000)
      ```

4. start ternaling
   1. ```buildoutcfg
      ./ngrok http {SERVERPORT} 
      # ex. ./ngrok http 8000  
      ``` 

---

## Function

___
_easy conversation_

_easy translation(using free papago api)_
___

## To be added

---
_packed by docker_

_translating sentence(now only translating words)_

---

## External API I use

---
_Naver Papago translation api_ [link](https://developers.naver.com/docs/papago/papago-nmt-overview.md) 

_Naver Papago detectLang api_ [link](https://developers.naver.com/docs/papago/papago-detectlangs-overview.md#언어-감지)

---