from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    GENDER_CHOICES = (
        ("Male", "Male"),
        ("Female", "Female"),
    )
    POLITICAL_CHOICES = (
        ("Democrat", "Democrat"),
        ("Republican", "Republican"),
        ("Libertarian", "Libertarian"),
        ("Green Party", "Green Party"),
        ("Other", "Other"),
    )
    first_name = forms.CharField(max_length=30, required=True, help_text='First Name.')
    last_name = forms.CharField(max_length=30, required=True, help_text='Last Name.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    age = forms.IntegerField()
    gender = forms.ChoiceField(choices=GENDER_CHOICES)
    political_status = forms.ChoiceField(choices=POLITICAL_CHOICES)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'age', 'gender', 'political_status', 'password1', 'password2', )