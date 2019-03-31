from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic

# Create your views here.
from pen_pal.models import User, Topic

def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_users = User.objects.all().count()
    num_topics = Topic.objects.all().count()
    
    # Users by Gender (gender = 'Male')
    num_males = User.objects.filter(gender='Male').count()
    num_females = User.objects.filter(gender='Female').count()
    
    context = {
        'num_users': num_users,
        'num_topics': num_topics,
        'num_males': num_males,
        'num_females': num_females,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)


def topics(request):
    """View function for topics page of site."""
    
    context = {
        'abortion': 'abortion',
        'affirmative_action': 'affirmative_action',
        'education': 'education',
        'healthcare': 'healthcare',
        'immigration': 'immigration',
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'topics.html', context=context)


class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'