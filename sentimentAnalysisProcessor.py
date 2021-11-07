import tweepy
from textblob import TextBlob

from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk

nltk.download('vader_lexicon')

#Removing the secrets
consumer_key = "#################"
consumer_secret = "###############"
access_token = "###############"
access_token_secret = "###############"


class scraping:
    def __init__(self):
        self.auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        self.auth.set_access_token(access_token, access_token_secret)
        self.api = tweepy.API(self.auth, wait_on_rate_limit=True)
        self.TwitterClient=tweepy.Client(bearer_token="###############", wait_on_rate_limit=True)

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
    if whole == 0:
        return 0
    return 100 * float(part)/float(whole)


def maximum(a, b, c):
    if (a > b) and (a > c):
        largest = a
        strr = "positive"
    elif (b > a) and (b > c):
        largest = b
        strr = "negative"
    else:
        largest = c
        strr = "neutral"
    return strr, largest


def tweetAnalyse(screenName, tweetCount):
    handle_name = screenName
    count_tweets = tweetCount
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


    raw_tweets = scrap_tweet.recent_tweets(handle_name, count_tweets)
    for tweet in raw_tweets:
        tweet_txt = tweet._json['full_text']
        tweet_list.append(tweet_txt)
        analysis = TextBlob(tweet_txt)

        replies=scrap_tweet.replyScraper(tweet._json['id_str'], 30)
        for reply in replies:
            noOfTweet += 1
            key_list.append(handle_name)
            reply_txt = reply['data']['text']
            reply_list.append(reply_txt)
            score = SentimentIntensityAnalyzer().polarity_scores(reply_txt)
            neg = score['neg']
            # neu = score['neu']
            pos = score['pos']
            # comp = score['compound']
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
    positive = format(positive, '.1f')
    negative = format(negative, '.1f')
    neutral = format(neutral, '.1f')
    strr, value = maximum(positive,negative,neutral)
    if strr == 'neutral':
        message = "There is neutral reaction to @"+handle_name+"'s latest "+count_tweets+" tweets."
    else:
        message = "There is a "+value+"% of "+strr+" reactions to @"+handle_name+"'s latest "+count_tweets+" tweets."
    return message
