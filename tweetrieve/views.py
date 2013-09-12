# Create your views here.
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django import forms
import json
import requests
from models import Tweet
import oauth2 as oauth

CONSUMER_KEY = "RA8zeFfkz1jpTy5I6P2g"
CONSUMER_SECRET = "IytfyvKxmPBnrRmqxt0NV0waoXUPq8rfUXD0tzg3HI"

OAUTH_TOKEN = "87239233-VSblo33EEkuQyNHgi11GRe0QqSHXPBM3X6tBRAWk"
OAUTH_TOKEN_SECRET = "xu05xY5WXxPoctvljLLbnoVSGSGfp0Yt241r6EVrd0"

def home(request):

	template = loader.get_template('home.html')
	context = RequestContext(request, {
	})
	return HttpResponse(template.render(context))

def formsubmit(request):
	url = "https://api.twitter.com/1.1/search/tweets.json?q=Vishrut42"
	consumer = oauth.Consumer(key=CONSUMER_KEY,
							  secret=CONSUMER_SECRET)
	token = oauth.Token(key=OAUTH_TOKEN,
						secret=OAUTH_TOKEN_SECRET)
	client = oauth.Client(consumer, token)

	resp, content = client.request(
		url,
		method="GET"
	)

	#print "RESPONSE-------------------"
	#print resp
	content_dict = json.loads(content)
	#print "CONTENT--------------------"
	#print json.dumps(content_dict, sort_keys=True, indent=4, separators=(',', ': '))

	status_list = content_dict['statuses']
	for status in status_list:
		print status['text'].encode('utf-8')
	
	tweet_list = []

	for tweet_num in range (0, 3):
		new_tweet = Tweet(user_handle="vishrut", tweet_text="my tweet")
		tweet_list.append(new_tweet)
	
	template = loader.get_template('tweet_list.html')
	context = RequestContext(request, {
		'tweet_list': tweet_list,
		'handle': request.GET['handle'],
	})
	
	return HttpResponse(template.render(context))