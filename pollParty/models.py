from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    bio = models.TextField()

    def __str__(self):
        return str(self.user)


class Poll(models.Model):
    # Model for Poll

    # Text Description for each Poll
    pollText = models.CharField(max_length=300)

    # User that Created Poll
    userPosted = models.ForeignKey(User, on_delete=models.CASCADE)

    # Date and Time - Creation of Poll
    pubDate = models.DateTimeField('date published')

    # Number of Up Votes for the Poll
    upVotes = models.IntegerField(default=0)

    # Number of Down Votes for the Poll
    downVotes = models.IntegerField(default=0)
