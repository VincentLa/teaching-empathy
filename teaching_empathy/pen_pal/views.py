import datetime

from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from .forms import SignUpForm


# Create your views here.
from pen_pal.models import UserProfile, Topic, UserTopic, Matches, ConversationText, Question
from django.contrib.auth.models import User
from pen_pal.forms import ProfileForm

def index(request):
    """View function for home page of site."""
    # Check that a user if actually Logged In
    # Taking this out for now
    # if not request.user.is_anonymous:
    #     if Matches.objects.filter(user1_id=request.user).exists():
    #         messages.info(request, 'You have a new match!')

    _ = _update_notifications(request)

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

    allmatches = Matches.objects.filter(user1_id = request.user) | Matches.objects.filter(user2_id = request.user)

    allmatches_unseen = allmatches.filter(seen = False)

    match_list = allmatches_unseen.values_list('user1_id', 'user2_id', 'match_time', 'id')
    userid_list = [_get_username_from_userid(x[0]) if x[0] != request.user
                   else _get_username_from_userid(x[1]) for x in match_list]
    match_times = [x[2] for x in match_list]
    match_ids = [x[3] for x in match_list]
    match_zip = list(zip(userid_list, match_times, match_ids))

    match_dicts = [{
        'notification_str': 'You matched with {} on {}.'.format(x[0], x[1].strftime("%Y-%m-%d %H:%M")),
        'time': x[1],
        'match_id': x[2]
    } for x in match_zip]

    allconvos = ConversationText.objects.exclude(user_id = request.user).filter(seen = False,
                                                                       match_id__in = allmatches.values_list('id'))

    convolist = allconvos.values_list('user_id', 'convo_time', 'match_id')
    convo_dicts = [{
        'notification_str': '{} posted a message in your conversation on {}.'.format(_get_username_from_userid(x[0]), x[1].strftime("%Y-%m-%d %H:%M")),
        'time': x[1],
        'match_id': x[2]
    } for x in convolist]

    notification_dicts = match_dicts + convo_dicts
    notification_dicts = sorted(notification_dicts, key = lambda x: x['time'], reverse = True)

    # Dummy data for now, copy of topics, to fill in
    context = {
        'notification_dicts': notification_dicts
    }

    allmatches.update(seen = True)
    allconvos.update(seen = True)

    _ = _update_notifications(request)

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

                new_match.conversation_phase = -1
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
        if match.conversation_phase == -1:
            convo_dict['phase'] = 'No Messages'
        elif match.conversation_phase == 0:
            convo_dict['phase'] = 'Icebreaker Phase'
        elif match.conversation_phase == 4:
            convo_dict['phase'] = 'Free Chat Phase'
        else:
            convo_dict['phase'] = matched_topics[match.conversation_phase - 1]

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

    # hacky way to restrict non-users from seeing private conversations
    if request.user not in users:
        return redirect('/')

    # get the user you matched with
    user_match = [x for x in users if x != request.user][0]

    # get your matched topics
    matched_topics_ids = [curr_match.topic1_id, curr_match.topic2_id, curr_match.topic3_id]
    matched_topics = [str(x) for x in matched_topics_ids if x is not None]
    matched_topic_str = ', '.join(matched_topics)

    # extremely hacky...
    convo_phase = curr_match.conversation_phase
    try:
        topic_id = matched_topics_ids[convo_phase - 1]
        topic = matched_topics[convo_phase - 1]
    except:
        topic_id = 4
        topic = ''
    all_questions = Question.objects.filter(topic_id=topic_id)

    # post request for new message
    if request.method == 'POST':
        new_convo = ConversationText()
        new_convo.match_id = Matches.objects.get(id=pk)
        new_convo.user_id = User.objects.get(username=request.user)
        new_convo.response = request.POST['message']
        new_convo.seen = False

        if curr_match.question_idx < len(all_questions):
            curr_question_id = all_questions[curr_match.question_idx]

            # if you haven't answered the question yet
            if not ConversationText.objects.filter(user_id = request.user,
                                               question_id = curr_question_id):
                new_convo.question_id = curr_question_id

                if ConversationText.objects.filter(user_id=user_match,
                                                   question_id=curr_question_id):
                    curr_match.question_idx += 1
                    curr_match.save()

            else:
                messages.info(request, 'You have already posted a response, and you cannot post another message until your pen pal responds to the question!')
                return redirect('/pen_pal/conversation/{}'.format(pk))

        # change not yet started to icebreaker phase
        if curr_match.conversation_phase == -1:
            curr_match.conversation_phase = 0
            curr_match.save()

        new_convo.save()
        return redirect('/pen_pal/conversation/{}'.format(pk))

    # request to show current text
    else:
        conversation_texts = ConversationText.objects.filter(match_id = curr_match).values_list('user_id', 'response', 'convo_time')
        convo_texts_dicts = [{'user': _get_username_from_userid(x),
                             'message_text': y,
                              'message_time': z} for x,y,z in sorted(conversation_texts, key = lambda x: x[2])]

        convo_guide = ''
        if convo_phase in [1,2,3]:
            convo_phase = 'discussion on {}'.format(topic)
            if curr_match.question_idx < len(all_questions):
                convo_guide = 'Guided Question: ' + str(all_questions[curr_match.question_idx])
            else:
                convo_guide = 'You have finished the guided questions! Now you can debate freely about the topic.'
        elif convo_phase == -1:
            convo_phase = 'No Messages'
        elif convo_phase == 0:
            convo_phase = 'Icebreaker Phase'
        else:
            convo_phase = 'Free Chat Phase'

        skip_user = curr_match.user1_skip if curr_match.user1_id == request.user else curr_match.user2_skip
        skip_pal = curr_match.user1_skip if curr_match.user1_id != request.user else curr_match.user2_skip

        context = {
            'chat_messages': convo_texts_dicts,
            'user_match' : user_match,
            'matched_topic_str': matched_topic_str,
            'phase': convo_phase,
            'conversation_guide': convo_guide,
            'pk': pk,
            'skip_user': skip_user,
            'skip_pal': skip_pal
        }

        return render(request, 'conversation.html', context)


def end_phase(request, pk):
    # function to end the phase of the conversation and move to the next one
    curr_match = Matches.objects.filter(id = pk)[0]
    if (request.user == curr_match.user1_id and curr_match.user2_skip == True
    ) or (request.user == curr_match.user2_id and curr_match.user1_skip == True):
        curr_match.user2_skip = False
        curr_match.user1_skip = False
        curr_match.conversation_phase += 1
    else:
        if request.user == curr_match.user1_id:
            curr_match.user1_skip = True
        else:
            curr_match.user2_skip = True
    curr_match.save()

    return redirect('/pen_pal/conversation/{}'.format(pk))

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

def _update_notifications(request):
    if not request.user.is_anonymous:
        allmatches = Matches.objects.filter(user1_id=request.user) | Matches.objects.filter(user2_id=request.user)
        allmatches_unseen = allmatches.filter(seen = False)

        match_ids = allmatches.values_list('id')
        notification_count = allmatches_unseen.count() + \
                             ConversationText.objects.exclude(user_id=request.user).filter(seen=False,
                                                                                           match_id__in=match_ids).count()
        request.session['notifications'] = notification_count
    else:
        request.session['notifications'] = 0
