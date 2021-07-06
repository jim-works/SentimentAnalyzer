# mine
import GetTweets as gt

try:
    api = gt.login("secrets.json")
    print("logged in!")
except:
    print("invalid credentials")
    exit

for tweet in gt.search(api, "Dream", count=10):
    print("\nNEW TWEET:\n")
    print(tweet.text)
