# Generated by Django 3.1.6 on 2021-06-01 00:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('pollParty', '0002_profile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='poll',
            name='downVotes',
        ),
        migrations.AddField(
            model_name='poll',
            name='downVotes',
            field=models.ManyToManyField(related_name='userDownvotedPolls', to=settings.AUTH_USER_MODEL),
        ),
        migrations.RemoveField(
            model_name='poll',
            name='upVotes',
        ),
        migrations.AddField(
            model_name='poll',
            name='upVotes',
            field=models.ManyToManyField(related_name='userUpvotedPolls', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='poll',
            name='userPosted',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='userPostedPolls', to=settings.AUTH_USER_MODEL),
        ),
    ]
