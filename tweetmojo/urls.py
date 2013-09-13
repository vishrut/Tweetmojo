from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'tweetrieve.views.home', name='home'),
    url(r'^tweetrieve/', include('tweetrieve.urls')),
)
