from django.db import models

class Tweet(models.Model):
	user_name = models.TextField()
	screen_name = models.TextField()
	tweet_text = models.TextField()
	tweet_id = models.IntegerField()