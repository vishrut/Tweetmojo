from django.db import models


class Tweet(models.Model):
	user_handle = models.CharField()
	tweet_text = models.TextField()
	tweet_id = models.IntegerField()