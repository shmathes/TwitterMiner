import tweepy
import sys
import datetime
from tweepy import API
from pymongo import MongoClient
import json


auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

api = tweepy.API(auth)


trends = api.trends_place(23424977)
usTrends = trends[0]['trends']

trend_topic = []
for i in range(len(usTrends)):
	trend_topic.append(usTrends[i]['name'])
	
print(trend_topic)

class MyStreamListener(tweepy.StreamListener):

	def __init__(self, api=None):
		self.api = api or API()
		self.tweet = []
		
	def on_connect(self):
		print("Success!")
		
	def on_status(self, status):
		tweets = {}
		
		if status.user.location is None and status.coordinates is None:
			return
		
		self.tweet.append([status.text, status.user.screen_name, status.user.location, status.coordinates, status.created_at.strftime("%d/%m/%y")])	
		tweets['text'] = status.text
		tweets['screen_name'] = status.user.screen_name
		tweets['location'] = status.user.location
		tweets['coordinates'] = status.coordinates
		tweets['created_at'] = status.created_at.strftime("%d/%m/%y")
		
		print(self.tweet)
		
	def on_error(self, status_code):
		if status_code == 420:
			return False
            #returning False in on_data disconnects the stream
            #return False

if __name__ == "__main__":
	myStreamListener = MyStreamListener()
	myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)
	region = [-88.51, 36.51, -81.91, 41.72]
	myStream.filter(track=trend_topic, locations = region)
