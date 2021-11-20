from django.db import models
# from django.utils.timezone import get_current_timezone



class Video(models.Model):
	title = models.CharField(max_length=100)
	description = models.CharField(max_length=200)
	publishedAt = models.CharField(max_length=200)
	thumbnailsUrls = models.CharField(max_length=200)

	def __str__(self):
		return (f"title:{self.title}, publishedAt:{self.publishedAt}")