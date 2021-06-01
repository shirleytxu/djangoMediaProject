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
    # One user can create multiple Polls i.e. one-to-many relationship
    userPosted = models.ForeignKey(User, on_delete=models.CASCADE,
                                   related_name="userPostedPolls")

    # Date and Time - Creation of Poll
    pubDate = models.DateTimeField('date published')

    # List of Users that Up Voted this Poll
    # A Poll can have many users that upvote it and a user can upvote many polls
    # i.e. many-to-many relationship
    upVotes = models.ManyToManyField(User, related_name="userUpvotedPolls")

    # List of Users that Down Voted this Poll
    # A Poll can have many users that downvote it and a user can downvote many
    # Polls i.e. many-to-many relationship
    downVotes = models.ManyToManyField(User, related_name="userDownvotedPolls")

    def __str__(self):
        print(self.pk)
        print(self.pollText)
        print(self.upVotes)
        print(self.downVotes)
        return "poll %d, pollText:'%s'" % (self.pk, self.pollText)