from django.db import models


class User(models.Model):
    user_id = models.CharField(max_length=50, primary_key=True)
    screen_name = models.CharField(max_length=100)
    name = models.CharField(max_length=200)
    image_url = models.URLField()
    follower_count = models.PositiveIntegerField()
    following_count = models.PositiveIntegerField()
    status_count = models.PositiveIntegerField()
    favorite_count = models.PositiveIntegerField()
    time_zone = models.CharField(max_length=100)
    utc_offset = models.CharField(max_length=100)
    created_at = models.DateTimeField()
    description = models.TextField()
    url = models.URLField()
    location = models.CharField(max_length=200)
    lang = models.CharField(max_length=10)
    window_count = models.PositiveIntegerField()
    total_count = models.PositiveIntegerField()