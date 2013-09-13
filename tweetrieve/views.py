# Create your views here.
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django import forms
import json
import requests
import datetime
from models import Tweet
import oauth2 as oauth
import re

CONSUMER_KEY = "RA8zeFfkz1jpTy5I6P2g"
CONSUMER_SECRET = "IytfyvKxmPBnrRmqxt0NV0waoXUPq8rfUXD0tzg3HI"

OAUTH_TOKEN = "87239233-VSblo33EEkuQyNHgi11GRe0QqSHXPBM3X6tBRAWk"
OAUTH_TOKEN_SECRET = "xu05xY5WXxPoctvljLLbnoVSGSGfp0Yt241r6EVrd0"

X_APP_ID = "37674edc3f8d743425ddd747fb6ccf5c" 
X_AUTH_TOKEN = "a974800a5567e2a22759c8176b3ddb80"

INSTAMOJO_URL = "https://www.instamojo.com/api/1/offer/"
TWITTER_URL = "https://api.twitter.com/1.1/search/tweets.json?q="

# Field identifiers used in a tweet. New identifiers can be added as long as they are unique.
# Using short identifiers since only 140 chars per tweet.
translation_dict = {
			't': 'title',
			'd': 'description',
			'c': 'currency',
			'p': 'base_price',
			'q': 'quantity',
			's': 'start_date',
			'e': 'end_date',
			'z': 'timezone',
			'v': 'venue',
			'u': 'redirect_url',
			'n': 'note',
			'f': 'file_upload_json',
			'i': 'cover_image_json',
			'title': 'title',
			'currency': 'currency',
			'price': 'base_price',
		}

# Error messages to be displayed when validations fail.
messages = {
			'title': 'Title required, should not be empty',
			'currency': 'Currency required and must be INR or USD',
			'base_price': 'Base price must be a number. Should be at least USD 0.49 or INR 9',
			'quantity': 'Quantity must be a number',
			'start_date': 'Start date format should be YYYY-MM-DD hh:mm',
			'end_date': 'End date format should be be YYYY-MM-DD hh:mm',
			'date_trio': 'For an event, start date, end date and timezone should occur together.'
		}

# Validation functions
def validate_title(title, offer_dict):
	title = title.strip()
	if len(title)>0 :
		return True
	else:
		return False

def validate_price(price, offer_dict):
	try:
		price = float(price)
	except ValueError:
		return False
	if price==0:
		return True
	else:
		if offer_dict['currency']=='INR' and price>=9:
			return True
		if offer_dict['currency']=='USD' and price>=0.49:
			return True
	return False
	
def validate_quantity(quantity, offer_dict):
	try:
		qty = int(quantity)
	except ValueError:
		return False
	if qty>=0 :
		return True
	else:
		return False

def validate_currency(currency, offer_dict):
	if currency=='INR' or currency=='USD':
		return True
	return False

def validate_date(date_string, offer_dict):
	try:
		datetime.datetime.strptime(date_string, '%Y-%m-%d %H:%M')
	except ValueError:
		return False
	return True

# Make offer on Instamojo using the API. Returns the response JSON.
def send_offer(offer_dict):
	headers = {
           'X-App-Id': X_APP_ID,
           'X-Auth-Token': X_AUTH_TOKEN 
		}
	r = requests.post(INSTAMOJO_URL, headers=headers, data=offer_dict)
	im_response = r.json()
	return im_response

# This dictionary maps each field to a validation function
validation_dict = {
			'title': validate_title,
			'currency': validate_currency,
			'base_price': validate_price,
			'quantity': validate_quantity,
			'start_date': validate_date, 
			'end_date': validate_date, 
		}

def home(request):
	# Render template
	template = loader.get_template('tweet_list.html')
	context = RequestContext(request, {})
	return HttpResponse(template.render(context))

def create_offer(request):
	tweet_text = request.POST['tweet_text'].encode('ascii','ignore')
	
	# Remove carriage return escape sequence, substitute <br> tags
	regex = re.compile(r'[\r]')
	tweet_text = regex.sub('\n', tweet_text)
	regex = re.compile(r'[<br>]')
	tweet_text = regex.sub('\n', tweet_text)
	
	# offer_dict contains all the offer details
	param_list = tweet_text.split("\n")
	offer_dict = {}
	for param in param_list:
		pair = param.split('-', 1)
		if len(pair)==2:
			field = pair[0].strip().lower()
			value = pair[1].strip()
			if field in translation_dict:
				offer_key = translation_dict[field]
				offer_dict[offer_key] = value
	
	# Validate offer
	error_messages = validate_offer(offer_dict)
	
	if len(error_messages) == 0: # Validation successful
		im_response = send_offer(offer_dict)
		if im_response['success']: # Offer created successfully
			link = im_response['offer']['url']
			context = RequestContext(request, {
				'link': link,
			})
		else: # Server error
			context = RequestContext(request, {
				'remote_error': True,
				'response_object':r.text
			})
	else: # Validation failed
		context = RequestContext(request, {
			'error_messages': error_messages
		})

	# Render template
	template = loader.get_template('create_offer.html')
	return HttpResponse(template.render(context))

# Returns tweets of the user in a list
def get_tweets(url):
	consumer = oauth.Consumer(key=CONSUMER_KEY, secret=CONSUMER_SECRET)
	token = oauth.Token(key=OAUTH_TOKEN, secret=OAUTH_TOKEN_SECRET)
	client = oauth.Client(consumer, token)

	resp, content = client.request(url, method="GET")
	content_dict = json.loads(content)
	
	status_list = content_dict['statuses']

	return status_list

# Curates tweets and renders the template
def search_tweets(request):
	tweet_list = []

	url = TWITTER_URL+request.GET['handle']
	status_list = get_tweets(url)
	
	tweet_id = 0
	for status in status_list:
		regex = re.compile(r'[\n]')
		tweet_text = regex.sub('<br>', status['text'])
		new_tweet = Tweet(tweet_id = tweet_id, tweet_text=tweet_text)
		tweet_list.append(new_tweet)
		tweet_id+=1
	
	template = loader.get_template('tweet_list.html')
	context = RequestContext(request, {
		'tweet_list': tweet_list,
		'handle': request.GET['handle'],
	})
	
	return HttpResponse(template.render(context))

# Validates the offer, returns a list of error messages
def validate_offer(offer_dict):
	error_messages = []

	# Must-haves for creating an offer
	if 'title' not in offer_dict:
		error_messages.append('Title required.')
	if 'currency' not in offer_dict:
		error_messages.append('Currency required.')
	if 'base_price' not in offer_dict:
		error_messages.append('Base price required.')
	
	# Start date, end date and timezone should always occur together
	if 'start_date' in offer_dict or 'end_date' in offer_dict:
		if ('start_date' not in offer_dict or
			'end_date' not in offer_dict or
			'timezone' not in offer_dict):
			error_messages.append(messages['date_trio'])

	# Validate each field individually
	for field in offer_dict:
		if field in validation_dict:
			if not validation_dict[field](offer_dict[field], offer_dict):
				error_messages.append(messages[field])

	return error_messages
