from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Poll
from django.views.generic import DetailView, CreateView
from datetime import datetime

class PostDetailView(DetailView):
    model = Poll
    template_name = 'pollParty/pollDetails.html'


class AddPostView(CreateView):
    model = Poll
    template_name = 'pollParty/createPoll.html'
    fields = ['pollText']

    def form_valid(self, form):
        form.instance.userPosted = self.request.user
        form.instance.pubDate = datetime.now()
        return super(AddPostView, self).form_valid(form)


def index(request):
    """
    index view- home page of pollParty
    shows all existing polls from database
    loads template pollParty/index.html
    """

    if request.POST:
        # Handles Post Operation
        if 'inputUsername' in request.POST.keys():
            # Authenticate User
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

    # Loads Template
    template = loader.get_template('pollParty/index.html')

    # Loads Data from Database
    allPolls = Poll.objects.order_by('-pubDate')

    # for
    for poll in allPolls:
        poster = poll.userPosted
        poll.firstName = poster.first_name
        poll.lastName = poster.last_name

    # Prepares Context for Template Rendering
    context = {'allPolls': allPolls, 'loggedIn': loggedIn,
               'user': request.user, }
    return HttpResponse(template.render(context, request))
