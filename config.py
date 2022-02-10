import os

class config:
    naver_client_id = os.environ.get("NAVER_CLIENT_ID")
    naver_client_secret = os.environ.get("NAVER_CLIENT_SECRET")
    naver_recognition_lang_client_id = os.environ.get("NAVER_RECOGNITION_LANG_CLIENT_ID")
    naver_recognition_lang_client_secret = os.environ.get("NAVER_RECOGNITION_LANG_CLIENT_SECRET")

class DevelopmentConfig(config):
    DEBUG = True
    token = os.environ.get("DEV_SLACK_BOT_TOKEN")
    signing_secret = os.environ.get("DEV_SLACK_SIGNING_SECRET")


class ProductionConfig(config):
    DEBUG = False
    token = os.environ.get("SLACK_BOT_TOKEN")
    signing_secret = os.environ.get("SLACK_SIGNING_SECRET")

config_by_name = dict(
    dev=DevelopmentConfig,
    prod=ProductionConfig
)