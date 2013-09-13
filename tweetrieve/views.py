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

messages = {
			'title': 'Title required, should not be empty', #not empty
			#'description': '',
			'currency': 'Currency required and must be INR or USD',# INR or USD
			'base_price': 'Base price must be a number. Should be at least USD 0.49 or INR 9', #must be number
			'quantity': 'Quantity must be a number', #must be number
			'start_date': 'Start date format should be YYYY-MM-DD hh:mm', #strptime
			'end_date': 'End date format should be be YYYY-MM-DD hh:mm', #strptime and > start
			#'timezone': 'Timezone format - Asia/Kolkata', #not empty
			'date_trio': 'For an event, start date, end date and timezone should occur together.'
			#'venue': '',
			#'redirect_url': '',
			#'note': '',
			#'file_upload_json': '',
			#'cover_image_json': '',
		}

def validate_title(title, offer_dict):
	title = title.strip()
	if len(title)>0 :
		return True
	else:
		return False

def validate_price(price, offer_dict):
	try:
		float(price)
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

validation_dict = {
			'title': validate_title,
			#'description': validate_description,
			'currency': validate_currency,
			'base_price': validate_price,
			'quantity': validate_quantity,
			'start_date': validate_date, 
			'end_date': validate_date, 
			#'timezone': validate_timezone,
			#'venue': validate_venue,
			#'redirect_url': validate_url,
			#'note': validate_note, 
			#'file_upload_json': validate_file_json,
			#'cover_image_json': validate_cover,
		}

def home(request):

	template = loader.get_template('home.html')
	context = RequestContext(request, {})
	return HttpResponse(template.render(context))

def tweetsubmit(request):
	tweet_text = request.POST['tweet_text'].encode('ascii','ignore')
	#tweet_text = """t-\nc-INRs\np-s0\ns-2013-12-12 23:xy\n"""
	regex = re.compile(r'[\r]')
	tweet_text = regex.sub('', tweet_text)
	
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
	
	error_messages = validate_offer(offer_dict)

	headers = {
           'X-App-Id': X_APP_ID,
           'X-Auth-Token': X_AUTH_TOKEN 
		}
	
	if len(error_messages) == 0:
		r = requests.post('https://www.instamojo.com/api/1/offer/', headers=headers, data=offer_dict)
		im_response = r.json()
		if im_response['success']:
			link = im_response['offer']['url']
			template = loader.get_template('create_offer.html')
			context = RequestContext(request, {
				'tweet': request.POST['tweet_text'],
				'link': link,
			})
			return HttpResponse(template.render(context))
		else:
			template = loader.get_template('create_offer.html')
			context = RequestContext(request, {
				'tweet': request.POST['tweet_text'],
				'remote_error': True,
				'response_object':r.text
			})
			return HttpResponse(template.render(context))

	else:
		template = loader.get_template('create_offer.html')
		context = RequestContext(request, {
			'tweet': request.POST['tweet_text'],
			'error_messages': error_messages
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
	
	status_list = content_dict['statuses']
	tweet_id = 0
	for status in status_list:
		#print status['text'].encode('utf-8')
		new_tweet = Tweet(tweet_id = tweet_id, user_handle="Vishrut42", tweet_text=status['text'])
		tweet_list.append(new_tweet)
		tweet_id+=1
	
	template = loader.get_template('tweet_list.html')
	context = RequestContext(request, {
		'tweet_list': tweet_list,
		'handle': request.GET['handle'],
	})
	
	return HttpResponse(template.render(context))

def validate_offer(offer_dict):
	error_messages = []
	if 'title' not in offer_dict:
		error_messages.append('Title required.')
	if 'currency' not in offer_dict:
		error_messages.append('Currency required.')
	if 'base_price' not in offer_dict:
		error_messages.append('Base price required.')
	
	if 'start_date' in offer_dict or 'end_date' in offer_dict:
		if ('start_date' not in offer_dict or
			'end_date' not in offer_dict or
			'timezone' not in offer_dict):
			error_messages.append(messages['date_trio'])

	for field in offer_dict:
		if field in validation_dict:
			if not validation_dict[field](offer_dict[field], offer_dict):
				error_messages.append(messages[field])

	return error_messages
