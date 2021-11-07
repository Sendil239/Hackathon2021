import tweepy
import json
import os
import pandas as pd
import re

consumer_key = "HhggF0UYL0UT9lxGc0FA5akMk"
consumer_secret = "32Oc2yV5qPRJtoG3mOcAIs2KHBOIpMY5VueqBhpVXrGvaBn4GO"
access_token = "1432530918032482310-A4iQvZbrcDs96oiLpJ2L7bdyaioZ6Y"
access_token_secret = "sqpgVhphGM6a2juQL2yAo50I8V4ZF7bBrgo7aWhIngPlK"


class scraping:
    def __init__(self):
        self.auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        self.auth.set_access_token(access_token, access_token_secret)
        self.api = tweepy.API(self.auth, wait_on_rate_limit=True)
        self.TwitterClient=tweepy.Client(bearer_token="AAAAAAAAAAAAAAAAAAAAAEG0TgEAAAAAatuaMPjd6D7YMUMsW7SKrrEViYg%3DEunhlvaHunj6zkYxzZAABhqsQtThR74am7zHnNruLNmhcqVSKF", wait_on_rate_limit=True)

    def tweetScraper(self, tweet_count,keyword_value,tweet_lang):
        return tweepy.Cursor(self.api.search_tweets,q=keyword_value+" -filter:retweets",lang=tweet_lang,count=tweet_count,tweet_mode='extended').items(tweet_count)


dir_path = os.path.dirname(os.path.realpath(__file__))
path = dir_path + "\\keyword.json"
with open(path,encoding="utf-8") as json_file:
    data = json.load(json_file)

scrap_tweet = scraping()
key_list = []
tweet_list = []
keyword_dir=f"keyword_cryptocurrency_en"
if not os.path.exists(keyword_dir):
    os.makedirs(keyword_dir)
    print("Created Directory : ", keyword_dir)

for keys in data["crypto"]:
    raw_tweets = scrap_tweet.tweetScraper(10, keys, "en")

    for tweet in raw_tweets:
        text = re.sub(r"[^a-zA-Z0-9]"," ",tweet._json['full_text'])
        key_list.append(keys)
        tweet_list.append(text)

df = pd.DataFrame({'keyword': key_list, 'tweets': tweet_list})
df.to_csv(keyword_dir+'\\keyword_cryptocurrency_en.csv', index=False)
    
