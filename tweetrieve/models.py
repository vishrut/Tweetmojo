from django.db import models


class Tweet(models.Model):
	user_handle = models.CharField(max_length=200)
	tweet_text = models.CharField(max_length=200)
	tweet_id = models.IntegerField()