import tweepy
import json


def login(secret_path):
    secrets = json.load(open(secret_path, "r"))

    # Authenticate to Twitter
    auth = tweepy.OAuthHandler(secrets["api_key"], secrets["api_secret"])
    auth.set_access_token(secrets["access_token"], secrets["access_secret"])

    # Create API object
    api = tweepy.API(auth, wait_on_rate_limit=True,
                     wait_on_rate_limit_notify=True)
    api.verify_credentials()
    return api


def search(api, query, count=None, lang=None):
    return api.search(q=query, count=count, lang=lang)
