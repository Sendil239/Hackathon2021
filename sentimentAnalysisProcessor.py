import tweepy
import json
import os
import pandas as pd
import re
from textblob import TextBlob

from wordcloud import WordCloud, STOPWORDS
from PIL import Image
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from langdetect import detect
from nltk.stem import SnowballStemmer
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from sklearn.feature_extraction.text import CountVectorizer
import nltk

nltk.download('vader_lexicon')

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

    def replyScraper(self,tweet_id,reply_count):
        tweet_fieldsList=["id","in_reply_to_user_id","created_at","lang"]
        user_fieldslist=["verified"]
        expansions_list=["author_id","entities.mentions.username"]
    
        all_replies=tweepy.Paginator(self.TwitterClient.search_recent_tweets,query="conversation_id:"+tweet_id,tweet_fields=tweet_fieldsList,expansions=expansions_list,user_fields=user_fieldslist).flatten(limit=reply_count)
        return all_replies
    
    def get_reply_info(self,reply_id):
        reply_withInfo=self.api.get_status(reply_id,include_entities=True)
        return reply_withInfo
    
    def recent_tweets(self, userid, cnt):
        return self.api.user_timeline(screen_name=userid, count=cnt, include_rts = False, tweet_mode = 'extended')

def percentage(part,whole):
    return 100 * float(part)/float(whole)

dir_path = os.path.dirname(os.path.realpath(__file__))
path = dir_path + "\\keyword.json"
with open(path,encoding="utf-8") as json_file:
    data = json.load(json_file)


keyword_dir=f"keyword_cryptocurrency_en"
if not os.path.exists(keyword_dir):
    os.makedirs(keyword_dir)
    print("Created Directory : ", keyword_dir)

handle_name = "elonmusk"
count_tweets = 40
tweet_list = []
reply_list = []
key_list = []
positive = 0
negative = 0
neutral = 0
polarity = 0
tweet_list = []
neutral_list = []
negative_list = []
positive_list = []
noOfTweet = 0
scrap_tweet = scraping()

for keys in data["crypto"]:
    #raw_tweets = scrap_tweet.tweetScraper(10, keys, "en")
    raw_tweets = scrap_tweet.recent_tweets(handle_name, count_tweets)
    for tweet in raw_tweets:
        noOfTweet = 0
        tweet_txt = tweet._json['full_text']
        tweet_list.append(tweet_txt)
        analysis = TextBlob(tweet_txt)

        replies=scrap_tweet.replyScraper(tweet._json['id_str'],30)
        for reply in replies:
            noOfTweet += 1
            key_list.append(handle_name)
            reply_txt = reply['data']['text']
            reply_list.append(reply_txt)
            score = SentimentIntensityAnalyzer().polarity_scores(reply_txt)
            neg = score['neg']
            neu = score['neu']
            pos = score['pos']
            comp = score['compound']
            polarity += analysis.sentiment.polarity
            
            if neg > pos:
                negative_list.append(reply_txt)
                negative += 1
            elif pos > neg:
                positive_list.append(reply_txt)
                positive += 1
            
            elif pos == neg:
                neutral_list.append(reply_txt)
                neutral += 1

positive = percentage(positive, noOfTweet)
negative = percentage(negative, noOfTweet)
neutral = percentage(neutral, noOfTweet)
polarity = percentage(polarity, noOfTweet)
positive = format(positive, '.1f')
negative = format(negative, '.1f')
neutral = format(neutral, '.1f')

df = pd.DataFrame({'keyword': key_list, 'tweets': reply_list})
df.to_csv(keyword_dir+'\\keyword_cryptocurrency_en.csv', index=False)

print("total number: ",len(reply_list))
print("positive number: ",len(positive_list))
print("negative number: ", len(negative_list))
print("neutral number: ",len(neutral_list))