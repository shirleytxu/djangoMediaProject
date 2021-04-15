from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Poll(models.Model):
    pollText = models.CharField(max_length=300)
    userPosted = models.ForeignKey(User, on_delete=models.CASCADE)
    pubDate = models.DateTimeField('date published')
    upVotes = models.IntegerField(default=0)
    downVotes = models.IntegerField(default=0)


