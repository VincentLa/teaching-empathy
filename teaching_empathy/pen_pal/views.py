from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth import login, authenticate
from .forms import SignUpForm


# Create your views here.
from pen_pal.models import User, Topic, UserTopic
from pen_pal.forms import ProfileForm

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


def SignUp(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


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


def profile(request):

    # TODO: dummy userid
    user_id_temp = 1

    # dictionary with variable names
    topic_dict = {
        1: ['abortion_view', 'abortion_learn_more'],
        2: ['affirmative_view', 'affirmative_learn_more'],
        3: ['education_view', 'education_learn_more'],
        4: ['healthcare_view', 'healthcare_learn_more'],
        5: ['immigration_view', 'immigration_learn_more']
    }

    # If this is a POST request then process the Form data
    if request.method == 'POST':
        form = ProfileForm(request.POST)

        if form.is_valid():
            user_object = User.objects.get(id=user_id_temp)

            # if user is already there, then update
            if UserTopic.objects.filter(user_id=user_object).exists():
                for topic_id, var_names in topic_dict.items():
                    topic_object = Topic.objects.get(id=topic_id)
                    existing_obj = UserTopic.objects.filter(user_id=user_object,
                                                            topic_id=topic_object)[0]
                    existing_obj.view = form.cleaned_data[var_names[0]]
                    existing_obj.interest_other_side = form.cleaned_data[var_names[1]]
                    existing_obj.save()

            # if not, then write new line to the table
            else:
                for topic_id, var_names in topic_dict.items():
                    user_topic_temp = UserTopic()
                    user_topic_temp.user_id = user_object
                    user_topic_temp.topic_id = Topic.objects.get(id=topic_id)
                    user_topic_temp.view = form.cleaned_data[var_names[0]]
                    user_topic_temp.progress = 0
                    user_topic_temp.interest_other_side = form.cleaned_data[var_names[1]]
                    user_topic_temp.save()

            # IMPLEMENT MATCHING ALGORITHM HERE
            return

    else:
        form = ProfileForm()

        context = {
            'form': form,
        }

        return render(request, 'profile.html', context)

def conversation(request, pk):

    if request.method == 'POST':
        return

    else:
        context = {
            'chat_messages': [{'user': 'james', 'message_text': 'test'},
                              {'user': 'nathan', 'message_text': 'hello'}],
            'first_message_id' : 0
        }

        return render(request, 'conversation.html', context)
