import csv
#import matplotlib.pyplot as plt
#import nltk 
from nltk.corpus import stopwords
import string
import pandas as pd
#from nltk.tokenize import WordPunctTokenizer
from bs4 import BeautifulSoup
import re
import io
import codecs
import json
from datetime import datetime
from pytz import timezone
import datetime
from datetime import timedelta
import sys
from sys import argv
import jsonpickle
import os
import tweepy


# Authenticating my account to access twitter’s API.
consumer_key = "ck186Ovisd90UwoJk2xBxaCWh"
consumer_secret = "k0f9167YEZM19td2W2ME18Bl859ZSgFjGxuz73aJQSaKrgl3Kz"
access_token = "975529263632912389-gOv572De8VjVW27PaQ9heD6okF1ZHOK "
access_token_secret = "9JDKZVjpC7CsAkNxZdPQWxOC3Qv19sHcizOzFTblYo6jB "

# Creating the authentication object
auth = tweepy.AppAuthHandler(consumer_key, consumer_secret)
# Setting your access token and secret
#auth.set_access_token(access_token, access_token_secret)
# Creating the API object while passing in auth information
api = tweepy.API(auth,wait_on_rate_limit=True, wait_on_rate_limit_notify=True) 

#Entering a search keyword related to Stocks and Tweets
searchQuery = 'AMZN AND stocks OR stock'
maxTweets = 10000000 # Some arbitrary large number
tweetsPerQry = 100  # this is the max the API permits
fName = 'tweets.json' # We'll store the tweets in a text file.
results = []

# If results from a specific ID onwards are reqd, set since_id to that ID.
# else default to no lower limit, go as far back as API allows
sinceId = None

# If results only below a specific ID are, set max_id to that ID.
# else default to no upper limit, start from the most recent tweet matching the search query.
max_id = -1000000

tweetCount = 0
print("Downloading max {0} tweets".format(maxTweets))

while tweetCount < maxTweets:
    try:
        if (max_id <= 0):
            if (not sinceId):
                new_tweets = api.search(q=searchQuery, count=tweetsPerQry,lang = "en" )
                #results.append(new_tweets)
            else:
                new_tweets = api.search(q=searchQuery, count=tweetsPerQry, lang = "en", since_id=sinceId)
                #results.append(new_tweets)
        else:
            if (not sinceId):
                new_tweets = api.search(q=searchQuery, count=tweetsPerQry, lang = "en",
                                            max_id=str(max_id - 1))
                #results.append(new_tweets)
            else:
                new_tweets = api.search(q=searchQuery, count=tweetsPerQry, lang = "en",
                                            max_id=str(max_id - 1),
                                            since_id=sinceId)
                #results.append(new_tweets)
        if not new_tweets:
            print("No more tweets found")
            break
        for tweet in new_tweets:
            #f.write(jsonpickle.encode(tweet._json, unpicklable=False) +'\n')
            results.append(tweet)
        tweetCount += len(new_tweets)
        print("Downloaded {0} tweets".format(tweetCount))
        max_id = new_tweets[-1].id
    except tweepy.TweepError as e:
        # Just exit if any error
        print("some error : " + str(e))
        break

print ("Downloaded {0} tweets, Saved to {1}".format(tweetCount, fName))

#Extracting elements from the tweet and populating data sets
def tweets_df(results):
    
    id_list = [tweet.id for tweet  in results]
    data_set = pd.DataFrame(id_list, columns = ["id"])
    clean_timestamp = []
  
   
    
    #Creating datafarmes for tweet fields.
   
   
    
    for tweet in results:
        timestamp = tweet.created_at
        #print(timestamp)
        offset_hours = -5 #######Change based on daylight savings#########################
        local_timestamp = timestamp + timedelta(hours=offset_hours)
        clean_timestamp.append(local_timestamp.strftime('%Y/%m/%d %H:%M:%S'))
        #clean_timestamp[i] = local_timestamp.strftime('%Y/%m/%d %H:%M:%S')
        
        
       
       
    #print(clean_timestamp)
    data_set["Date"]= [date for date in clean_timestamp]
    #data_set["Date"]= [tweet.created_at for tweet in results]
    data_set["source"] = [tweet.source for tweet in results]
    data_set["Author"] = [tweet.author.screen_name for tweet in results]
    data_set["Snippet"] = [tweet.text for tweet in results]
    if hasattr(tweet, 'retweet_count'):
        data_set["Twitter.Retweet"] = [tweet.retweet_count for tweet in results]
    else:
        data_set["Twitter.Retweet"] = 'NULL'
    data_set["Twitter.Followers"] = [tweet.author.followers_count for tweet in results]
    data_set["Twitter.Following"] = [tweet.author.friends_count for tweet in results]
    data_set["Hashtags"] = [tweet.entities.get('hashtags') for tweet in results]
    data_set["in_reply_to_screen_name"] = [tweet.in_reply_to_screen_name for tweet in results]
    data_set["in_reply_to_user_id"] = [tweet.in_reply_to_user_id for tweet in results]
    
    #if hasattr(tweet,'retweeted_status'):
       # data_set["retweeted_status1"] = [tweet.retweeted_status for tweet in results]
    #else:
        #print('Else')
        #data_set["retweeted_status"] = 'NULL'
        
    if hasattr(tweet, 'reply_count'):
        data_set["reply_count"] = [tweet.reply_count for tweet in results]
    else:
        data_set["reply_count"] = 'NULL'
        
   
        
    if hasattr(tweet, 'favorite_count'):
        data_set["favorite_count"] = [tweet.favorite_count for tweet in results]
    else:
        data_set["favorite_count"] = 'NULL'
    
    
   
   
    data_set["user_location"] = [tweet.author.location for tweet in results]
    data_set["user_verified"] = [tweet.author.verified for tweet in results]
   
    data_set["user_listed_count"] = [tweet.author.listed_count for tweet in results]
    data_set["user_favourites_count"] = [tweet.author.favourites_count for tweet in results]
    #data_set[""] = [tweet.author.statuses_count for tweet in results]
    data_set["user_geo_enabled"] = [tweet.author.geo_enabled for tweet in results]
    
    
    return data_set


#Getting the extracted tweets and removing fields from them.
data_set = tweets_df(results)


# Remove tweets with duplicate text

text = data_set["Snippet"]

for i in range(0,len(text)):
    txt = ' '.join(word for word in text[i] .split() if not word.startswith('https:'))
    data_set.set_value(i, 'text2', txt)
   #data_set.at[i] = ('text2', txt)
    
#data_set.drop_duplicates('text2', inplace=True)
data_set.reset_index(drop = True, inplace=True)
data_set.drop('Snippet', axis = 1, inplace = True)
data_set.rename(columns={'text2': 'Snippet'}, inplace=True)
#type(clean_timestamp)

data_set.to_csv(r'/home/nebuchednezzar/tweets.csv')
