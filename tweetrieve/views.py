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

tweet_list = []


def home(request):

	template = loader.get_template('home.html')
	context = RequestContext(request, {})
	return HttpResponse(template.render(context))

def tweetsubmit(request):

	headers = {
           'X-App-Id': '37674edc3f8d743425ddd747fb6ccf5c',
           'X-Auth-Token': 'a974800a5567e2a22759c8176b3ddb80'
		}

	payload	= {
			'title': 'Test Membership through API 2',
			#'description': 'Testing API',
			'currency': 'INR',
			'base_price': '50',
			'quantity': '0',
			'start_date': '2013-12-31 23:00',
			'end_date': '2014-12-31 23:59',
			'timezone': 'Asia/Kolkata',
			'venue': 'Goa',
			#'redirect_url':,
			#'note':,
			#'file_upload_json':,
			#'cover_image_json':,
		}
	## Mandatory Fields - Title, Currency, Base Price
	## Events - Start Date, End Date, Timezone
	## Files - File Upload JSON
	1. Check for TCB
	2. If start or end date then start, end dates and timezone should exist


	r = requests.post('https://www.instamojo.com/api/1/offer/', headers=headers, data=payload)

	template = loader.get_template('create_offer.html')
	context = RequestContext(request, {
		'tweet': request.POST['tweet_text'],
		'api_response': r.text
	})
	return HttpResponse(template.render(context))

def formsubmit(request):
	tweet_list = []
	url = "https://api.twitter.com/1.1/search/tweets.json?q="+request.GET['handle']
	consumer = oauth.Consumer(key=CONSUMER_KEY,
							  secret=CONSUMER_SECRET)
	token = oauth.Token(key=OAUTH_TOKEN,
						secret=OAUTH_TOKEN_SECRET)
	client = oauth.Client(consumer, token)

	resp, content = client.request(
		url,
		method="GET"
	)

	content_dict = json.loads(content)

	headers = {
           'X-App-Id': '37674edc3f8d743425ddd747fb6ccf5c',
           'X-Auth-Token': 'a974800a5567e2a22759c8176b3ddb80'
		}
	
	#r = requests.post('https://www.instamojo.com/api/1/debug/', headers=headers)
	#print r.text
	
	status_list = content_dict['statuses']
	tweet_id = 0
	for status in status_list:
		new_tweet = Tweet(tweet_id = tweet_id, user_handle="Vishrut42", tweet_text=status['text'])
		tweet_list.append(new_tweet)
		tweet_id+=1
	
	template = loader.get_template('tweet_list.html')
	context = RequestContext(request, {
		'tweet_list': tweet_list,
		'handle': request.GET['handle'],
	})
	
	return HttpResponse(template.render(context))