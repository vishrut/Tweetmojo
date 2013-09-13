from django.db import models

class Tweet(models.Model):
	tweet_text = models.TextField()
	tweet_id = models.IntegerField()