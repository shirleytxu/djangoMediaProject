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

class PostDetailView(DetailView):
    model = Poll
    template_name = 'pollParty/pollDetails.html'

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        context['firstName'] = context['poll'].userPosted.first_name
        context['lastName'] = context['poll'].userPosted.last_name
        print(context)
        return context


class AddPostView(CreateView):
    model = Poll
    template_name = 'pollParty/createPoll.html'
    fields = ['pollText']

    def form_valid(self, form):
        form.instance.userPosted = self.request.user
        form.instance.pubDate = datetime.now()
        return super(AddPostView, self).form_valid(form)


def upvote(request, pk):
    user = request.user
    poll = get_object_or_404(Poll, pk=pk)

    poll.upVotes.add(user)
    poll.save()
    return HttpResponseRedirect(reverse('postDetails', args=(pk,)))


def downvote(request, pk):
    user = request.user
    poll = get_object_or_404(Poll, pk=pk)

    poll.downVotes.add(user)
    poll.save()
    return HttpResponseRedirect(reverse('postDetails', args=(pk,)))


def deletepost(request, pk):
    user = request.user
    poll = get_object_or_404(Poll, pk=pk)
    if user == poll.userPosted:
        postToDelete = Poll.objects.get(pk=pk)
        postToDelete.delete()
        message = "Poll %d deleted successfully." % pk
    else:
        message = "You do not have permission to delete."
    context = {'message': message}
    return render(request, 'pollParty/deletePoll.html', context)


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
