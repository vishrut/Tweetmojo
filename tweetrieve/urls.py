from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'views/search_tweets', 'tweetrieve.views.search_tweets', name='search_tweets'),
	url(r'views/create_offer', 'tweetrieve.views.create_offer', name='create_offer'),
)