from django.shortcuts import render

# Create your views here.
from pen_pal.models import User, Topic
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


def profile(request):

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        return

    # If this is a GET (or any other method) create the default form.
    else:
        form = ProfileForm()

    context = {
        'form': form,
    }

    return render(request, 'profile.html', context)
