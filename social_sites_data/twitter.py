import tweepy
import pandas as pd
from Credentials.credentials import *
from var import limit

def get_twitter_text(s):
    print("1")
    auth = tweepy.OAuthHandler(api_key, api_key_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    keywords = s+'-filter:retweets'
    print("2")
    # keywords='(ukraine OR russia) until:2022-03-05 since:2015-08-09'
    tweets=tweepy.Cursor(api.search_tweets,q=keywords,lang="en",tweet_mode="extended").items(limit)
    columns = ['Tweet']
    data = []
    print("3")
    for tweet in tweets:
        data.append([ tweet.full_text])
    df = pd.DataFrame(data, columns=columns)
    # print(df)
    return df
