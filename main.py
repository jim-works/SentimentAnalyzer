import GetTweets as gt
import SentimentAnalyzer as sa
from wordcloud import WordCloud
from functools import reduce
import matplotlib.pyplot as plt
import sys
import getopt
import json

profanity_path = "profanity.json"
secrets_path = "secrets.json"
negative_dest = "negative.png"
neutral_dest = "neutral.png"
positive_dest = "positive.png"
query = '"State Farm" OR "StateFarm"'

profane_words = []


def init():
    global profanity_path
    global secrets_path
    global negative_dest
    global neutral_dest
    global positive_dest
    global query
    global profane_words

    if profanity_path not in (None, ""):
        f = open(profanity_path, 'r')
        profane_words = json.load(f)["words"]
        f.close()

    try:
        opts, args = getopt.getopt(
            sys.argv, "hs:p:q:c:", ["negative=", "neutral=", "positive=", "--help"])
    except getopt.GetoptError:
        print("main.py -q <query> -c <count=100> -s <secrets.json path> -p <profanity.json path> --negative <dest for negative.png> --neutral <dest for neutral.png> --positive <dest for positive.png>")
        exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print("main.py -q <query> -c <count=100> -s <secrets.json path> -p <profanity.json path> --negative <dest for negative.png> --neutral <dest for neutral.png> --positive <dest for positive.png>")
            exit()
        elif opt == "-s":
            self.secrets_path = arg
        elif opt == "-p":
            profanity_path = arg
        elif opt == "--negative":
            negative_dest = arg
        elif opt == "--neutral":
            neutral_dest = arg
        elif opt == "--positive":
            positive_dest = arg


def run():
    try:
        api = gt.login(secrets_path)
        print("logged in!")
    except:
        print("invalid credentials, check " + str(secrets_path))
        exit()
    result_dict = {'neg': [], 'neu': [], 'pos': []}
    common_words = [s.strip() for s in query.replace('"', '').split()]
    common_words.extend(["t.co", "https", "http", "com", "org", "net"])
    for tweet in gt.search(api, query, count=100).unnest_rt().to_text():
        sa.categorize(sa.filter(tweet,
                      common_words=common_words, force_lower=True, profane_words=profane_words), result_dict)

    for key in result_dict.keys():
        print(str(key) + ": " + str(len(result_dict[key])))

    if negative_dest not in (None, ""):
        wc = WordCloud(width=1200, height=600).generate(
            reduce(lambda a, b: a + b, result_dict['neg'], ""))
        wc.to_file(negative_dest)
        print("Saved negative wordcloud to: " + negative_dest)

    if neutral_dest not in (None, ""):
        wc = WordCloud(width=1200, height=600).generate(
            reduce(lambda a, b: a + b, result_dict['neu'], ""))
        wc.to_file(neutral_dest)
        print("Saved neutral wordcloud to: " + neutral_dest)

    if positive_dest not in (None, ""):
        wc = WordCloud(width=1200, height=600).generate(
            reduce(lambda a, b: a + b, result_dict['pos'], ""))
        wc.to_file(positive_dest)
        print("Saved positive wordcloud to: " + positive_dest)


init()
run()
