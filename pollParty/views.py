from django.utils import timezone

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Poll


# Create your views here.

def index(request):
    if request.POST:
        if 'inputUsername' in request.POST.keys():
            user = authenticate(username=request.POST['inputUsername'],
                                password=request.POST['inputPassword'])
            if user is not None:
                login(request, user)
            else:
                pass
        elif 'logout' in request.POST.keys():
            logout(request)
    if request.user.is_authenticated:
        loggedIn = True
    else:
        loggedIn = False

    template = loader.get_template('pollParty/index.html')

    allPolls = Poll.objects.order_by('-pubDate')

    for poll in allPolls:
        poster = poll.userPosted
        poll.firstName = poster.first_name
        poll.lastName = poster.last_name

    context = {'allPolls': allPolls, 'loggedIn': loggedIn,
               'user': request.user, }
    return HttpResponse(template.render(context, request))


def createPoll(request):
    if request.POST:
        newPoll = Poll(pollQuestion=request.POST['newPostText'],
                       userPosted=request.POST['userPosting'],
                       pubDate=timezone.now(), )
        newPoll.save()

    template = loader.get_template('pollParty/createPoll.html')
    context = {}
    return HttpResponse(template.render(context, request))
