from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from .forms import SignUpForm


# Create your views here.
from pen_pal.models import UserProfile, Topic, UserTopic, Matches, ConversationText
from django.contrib.auth.models import User
from pen_pal.forms import ProfileForm

CONVO_PHASE_DICT = {
    0: 'No messages yet',
    1: 'Icebreaker Phase',
    2: 'Guided Question Phase',
    3: 'Unstructured Discussion Phase',
    4: 'Free Chat Phase'
}

def index(request):
    """View function for home page of site."""
    # Check that a user if actually Logged In
    if not request.user.is_anonymous:
        if Matches.objects.filter(user1_id=request.user).exists():
            messages.info(request, 'You have a new match!')

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

            messages.success(request, 'You have successfully created a new profile!')

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


def notifications(request):
    """View function for Notifications page of site."""
    
    # Dummy data for now, copy of topics, to fill in
    context = {
        'abortion': 'abortion',
        'affirmative_action': 'affirmative_action',
        'education': 'education',
        'healthcare': 'healthcare',
        'immigration': 'immigration',
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'notifications.html', context=context)


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
                    existing_obj = UserTopic.objects.filter(user_id=request.user,
                                                            topic_id=topic_id)[0]
                    existing_obj.view = form.cleaned_data[var_names[0]]
                    existing_obj.interest_other_side = form.cleaned_data[var_names[1]]
                    existing_obj.save()

            # if not, then write new line to the table
            else:
                for topic_id, var_names in topic_dict.items():
                    user_topic_temp = UserTopic()
                    user_topic_temp.user_id = User.objects.get(username=request.user)
                    user_topic_temp.topic_id = Topic.objects.get(id=topic_id)
                    user_topic_temp.view = form.cleaned_data[var_names[0]]
                    user_topic_temp.progress = 0
                    user_topic_temp.interest_other_side = form.cleaned_data[var_names[1]]
                    user_topic_temp.save()


            # matching algorithm
            user_ranks = _get_user_ranks(request.user.id)

            # iterate through all users to find opposite views
            matched_topics = []
            final_match = None

            # going through each user, from least to most matches
            for user in user_ranks:

                # going through each topic
                for topic_id, var_names in topic_dict.items():
                    views = UserTopic.objects.filter(user_id=user,
                                                    topic_id=topic_id)[0]
                    if views.interest_other_side == False:
                        continue
                    topic_view_user = form.cleaned_data[var_names[0]]
                    topic_view_match = views.view
                    topic_view = (topic_view_user + topic_view_match).lower()
                    if 'liberal' in topic_view and 'conservative' in topic_view:
                        matched_topics.append(topic_id)

                # if there's any matched topic, then break and create a match
                if matched_topics:
                    final_match = user
                    break

            # save new match
            if final_match is not None:
                new_match = Matches()
                new_match.user1_id = User.objects.get(username = request.user)
                new_match.user2_id = User.objects.get(id = user)
                new_match.topic1_id = Topic.objects.get(id = matched_topics[0])
                if len(matched_topics) > 1:
                    new_match.topic2_id = Topic.objects.get(id=matched_topics[1])
                if len(matched_topics) > 2:
                    new_match.topic3_id = Topic.objects.get(id=matched_topics[2])

                new_match.conversation_phase = 0
                new_match.save()

            return redirect('/')

    else:

        initial_dict = {}

        if UserTopic.objects.filter(user_id=request.user).exists():
            for topic_id, var_names in topic_dict.items():
                existing_obj = UserTopic.objects.filter(user_id=request.user,
                                                        topic_id=topic_id)[0]
                initial_dict[var_names[0]] = existing_obj.view
                initial_dict[var_names[1]] = existing_obj.interest_other_side
        else:
            for topic_id, var_names in topic_dict.items():
                initial_dict[var_names[0]] = 'Neutral'
                initial_dict[var_names[1]] = True

        form = ProfileForm(initial = initial_dict)

        context = {
            'form': form,
        }

        return render(request, 'profile.html', context)


def allconversations(request):
    """View function for Notifications page of site."""

    allconvos = Matches.objects.filter(user1_id = request.user) | Matches.objects.filter(user2_id = request.user)

    convos = []

    for match in allconvos:
        convo_dict = {}

        users = [match.user1_id, match.user2_id]
        user_match = [x for x in users if x != request.user][0]
        convo_dict['user'] = str(user_match)
        convo_dict['id'] = match.id

        matched_topics = [match.topic1_id, match.topic2_id, match.topic3_id]
        matched_topics = [str(x) for x in matched_topics if x is not None]
        matched_topic_str = ', '.join(matched_topics)

        convo_dict['matched_topics'] = matched_topic_str
        convo_dict['phase'] = CONVO_PHASE_DICT.get(match.conversation_phase)

        convos.append(convo_dict)

    # Dummy data for now, copy of topics, to fill in
    context = {
        'convos': convos
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'allconversations.html', context=context)


def conversation(request, pk):

    # get matched topics
    curr_match = Matches.objects.filter(id = pk)[0]
    users = [curr_match.user1_id, curr_match.user2_id]

    if request.user not in users:
        return redirect('/')

    user_match = [x for x in users if x != request.user][0]
    matched_topics = [curr_match.topic1_id, curr_match.topic2_id, curr_match.topic3_id]
    matched_topics = [str(x) for x in matched_topics if x is not None]
    matched_topic_str = ', '.join(matched_topics)

    # post request for new message
    if request.method == 'POST':
        new_convo = ConversationText()
        new_convo.match_id = Matches.objects.get(id=pk)
        new_convo.user_id = User.objects.get(username=request.user)
        new_convo.response = request.POST['message']
        new_convo.save()

        if curr_match.conversation_phase == 0:
            curr_match.conversation_phase = 1
            curr_match.save()

        return redirect('/pen_pal/conversation/{}'.format(pk))

    # request to show current text
    else:
        conversation_texts = ConversationText.objects.filter(match_id = curr_match).values_list('user_id', 'response', 'convo_time')
        convo_texts_dicts = [{'user': _get_username_from_userid(x),
                             'message_text': y,
                              'message_time': z} for x,y,z in sorted(conversation_texts, key = lambda x: x[2])]
        convo_phase = CONVO_PHASE_DICT[curr_match.conversation_phase if curr_match.conversation_phase != 0 else 1]

        context = {
            'chat_messages': convo_texts_dicts,
            'user_match' : user_match,
            'matched_topic_str': matched_topic_str,
            'phase': convo_phase
        }

        return render(request, 'conversation.html', context)


# helper function
# https://stackoverflow.com/questions/2567801/display-user-name-in-reference-to-user-id-in-django-template
def _get_username_from_userid(user_id):
    try:
        return User.objects.get(id=user_id).username
    except User.DoesNotExist:
        return 'Unknown'


def _get_user_ranks(curr_user_id):
    # get counts for number of matches
    all_users = User.objects.all().values_list('id', flat=True)
    all_users = [x for x in all_users if x != curr_user_id]

    match_count = {}

    # get the match count for all users, sorta waste of time
    for user in all_users:
        match_count1 = Matches.objects.filter(user1_id=user).count()
        match_count2 = Matches.objects.filter(user2_id=user).count()
        match_count[user] = match_count1 + match_count2

    user_ranks = sorted(match_count, key=match_count.get)
    return user_ranks
