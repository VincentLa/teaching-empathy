from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth import login, authenticate
from .forms import SignUpForm


# Create your views here.
from pen_pal.models import UserProfile, Topic, UserTopic, Conversation, Matches
from django.contrib.auth.models import User
from pen_pal.forms import ProfileForm

def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_users = UserProfile.objects.all().count()
    num_topics = Topic.objects.all().count()
    
    # Users by Gender (gender = 'Male')
    num_males = UserProfile.objects.filter(gender='Male').count()
    num_females = UserProfile.objects.filter(gender='Female').count()
    
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
            # django stuff
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)

            user_profile = UserProfile()
            user_profile.user_id = User.objects.get(username=request.user)
            user_profile.first_name = form.cleaned_data.get('first_name')
            user_profile.last_name = form.cleaned_data.get('last_name')
            user_profile.email = form.cleaned_data.get('email')
            user_profile.age = form.cleaned_data.get('age')
            user_profile.gender = form.cleaned_data.get('gender')
            user_profile.political_status = form.cleaned_data.get('political_status')
            user_profile.save()

            return redirect('/pen_pal/profile')
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
            # if user is already there, then update
            if UserTopic.objects.filter(user_id=request.user).exists():
                for topic_id, var_names in topic_dict.items():
                    topic_object = Topic.objects.get(id=topic_id)
                    existing_obj = UserTopic.objects.filter(user_id=request.user,
                                                            topic_id=topic_object)[0]
                    existing_obj.view = form.cleaned_data[var_names[0]]
                    existing_obj.interest_other_side = form.cleaned_data[var_names[1]]
                    existing_obj.save()

            # if not, then write new line to the table
            else:
                print(request.user)
                for topic_id, var_names in topic_dict.items():
                    user_topic_temp = UserTopic()
                    user_topic_temp.user_id = User.objects.get(username=request.user)
                    print("*" * 10)
                    print(user_topic_temp.user_id)
                    user_topic_temp.topic_id = Topic.objects.get(id=topic_id)
                    user_topic_temp.view = form.cleaned_data[var_names[0]]
                    user_topic_temp.progress = 0
                    user_topic_temp.interest_other_side = form.cleaned_data[var_names[1]]
                    user_topic_temp.save()

            # TODO: IMPLEMENT MATCHING ALGORITHM HERE
            return redirect('/')

    else:
        form = ProfileForm()

        context = {
            'form': form,
        }

        return render(request, 'profile.html', context)

def conversation(request, pk):
    curr_match = Matches.objects.filter(id = pk)[0]
    users = [curr_match.user1_id, curr_match.user2_id]
    user_match = [x for x in users if x != request.user][0]
    matched_topics = [curr_match.topic1_id, curr_match.topic2_id, curr_match.topic3_id]
    matched_topics = [str(x) for x in matched_topics if x is not None]
    matched_topic_str = ', '.join(matched_topics)

    if request.method == 'POST':
        return

    else:
        context = {
            'chat_messages': [{'user': 'james', 'message_text': 'test'},
                              {'user': 'nathan', 'message_text': 'hello'}],
            'user_match' : user_match,
            'matched_topic_str': matched_topic_str
        }

        return render(request, 'conversation.html', context)
