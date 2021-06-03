from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from .models import Poll
from django.views.generic import DetailView, CreateView
from datetime import datetime
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect


class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name", "password1",
                  "password2"]


def register(response):
    """
    register view-
    allows new users to register an account
    loads template registration/register.html
    """
    message = ""
    if response.method == "POST":
        form = RegisterForm(response.POST)
        if form.is_valid():
            # Registration form successful, redirects to home
            form.save()
            return redirect("/")
        else:
            # Registration form unsuccessful
            message = "Registration Form Failed. "

    else:
        form = RegisterForm()
    return render(response, "registration/register.html",
                  {"form": form, "message": message})


class PostDetailView(DetailView):
    """
    postdetailview view-
    allows users to view a post in an individual page
    loads template pollParty/pollDetails.html
        """
    model = Poll
    template_name = 'pollParty/pollDetails.html'

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        context['firstName'] = context['poll'].userPosted.first_name
        context['lastName'] = context['poll'].userPosted.last_name
        print(context)
        return context


class AddPostView(CreateView):
    """
    addpostview view-
    allows users to add their own posts
    loads template pollParty/createPoll.html
    """
    model = Poll
    template_name = 'pollParty/createPoll.html'
    fields = ['pollText']

    def form_valid(self, form):
        form.instance.userPosted = self.request.user
        form.instance.pubDate = datetime.now()
        return super(AddPostView, self).form_valid(form)


def upvote(request, pk):
    """
    upvote view-
    allows users to upvote posts
    displayed in pollParty/pollDetails.html
    """
    user = request.user
    poll = get_object_or_404(Poll, pk=pk)

    # Adds user to list of users that upvoted this post
    poll.upVotes.add(user)
    poll.save()
    # Refreshes page after upvote so data is immediately updated
    return HttpResponseRedirect(reverse('postDetails', args=(pk,)))


def downvote(request, pk):
    """
    downvote view-
    allows users to downvote posts
    displayed in pollParty/pollDetails.html
    """

    user = request.user
    poll = get_object_or_404(Poll, pk=pk)

    # Adds user to list of users that downvoted this post
    poll.downVotes.add(user)
    poll.save()
    # Refreshes page after downvote so data is immediately updated
    return HttpResponseRedirect(reverse('postDetails', args=(pk,)))


def deletepost(request, pk):
    """
    deletepost view-
    displays page after author of a post deletes their post
    loads template pollParty/deletePoll.html
    """

    user = request.user
    poll = get_object_or_404(Poll, pk=pk)
    if user == poll.userPosted:
        # Poll's author is user, can delete
        postToDelete = Poll.objects.get(pk=pk)
        postToDelete.delete()
        message = "Poll %d deleted successfully." % pk
    else:
        # Poll's author is not user, cannot delete - Prevents other users from
        # deleting a post that isn't theirs by entering a specific URL.
        message = "You do not have permission to delete."
    context = {'message': message}
    return render(request, 'pollParty/deletePoll.html', context)


def index(request):
    """
    index view- home page
    home page of pollParty, shows all existing polls from database
    loads template pollParty/index.html
    """

    if request.POST:
        # Handles Post Operation
        if 'inputUsername' in request.POST.keys():
            # Authenticates User
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

    for poll in allPolls:
        poster = poll.userPosted
        poll.firstName = poster.first_name
        poll.lastName = poster.last_name
    # Prepares Context for Template Rendering
    context = {'allPolls': allPolls, 'loggedIn': loggedIn,
               'user': request.user, }
    return HttpResponse(template.render(context, request))
