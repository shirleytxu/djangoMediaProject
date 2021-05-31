from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Poll
from django.views.generic import DetailView, CreateView

class postDetailView(DetailView):
    model = Poll
    template_name = 'pollParty/postDetails.html'

class AddPostView(CreateView):
    model = Poll
    template_name = 'createPoll.html'
    fields = '__all__'

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

def createPoll(request):
     
    """createPoll view- page for user user to create a new poll
    loads template pollParty/createPoll.html (simple line of text for now)
    """

    if request.POST:
        newPoll = Poll(pollQuestion=request.POST['newPostText'],
                       userPosted=request.POST['userPosting'],
                       pubDate=timezone.now(), )
        newPoll.save()

    # Loads Template
    template = loader.get_template('pollParty/createPoll.html')

    # Prepares Context
    context = {}      # empty for now
    return HttpResponse(template.render(context, request))



# password = make_password(the password input value from the form)
# def user

"""def myView(request):
    # Just from URL (Get, no data)
    def get(self, request):
        if request.method =="GET":
        # User logged in

        # User not logged in

    # Came from a <form> (POST< with data)
    def post(self, request):
        if request.method == "POST":
        # User logged in

        # user not logged in

"""