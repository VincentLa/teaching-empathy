from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


CHOICES_LIST = (("Very Liberal", "Very Liberal"),
                ("Slightly liberal", "Slightly Liberal"),
                ("Neutral", "Neutral"),
                ("Slightly Conservative", "Slightly Conservative"),
                ("Very Conservative", "Very Conservative"))


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


class ProfileForm(forms.Form):
    abortion_view = forms.ChoiceField(label = 'Abortion',
                                   choices=CHOICES_LIST)

    abortion_learn_more = forms.BooleanField(label = '', required = False,
                                             help_text = 'I want to learn more about the other side of abortion.')

    affirmative_view = forms.ChoiceField(label='Affirmative Action',
                                      choices=CHOICES_LIST)

    affirmative_learn_more = forms.BooleanField(label = '', required = False,
                                             help_text = 'I want to learn more about the other side of affirmative action.')

    education_view = forms.ChoiceField(label='Education',
                                      choices=CHOICES_LIST)

    education_learn_more = forms.BooleanField(label = '', required = False,
                                             help_text = 'I want to learn more about the other side of education.')

    healthcare_view = forms.ChoiceField(label='Healthcare',
                                       choices=CHOICES_LIST)

    healthcare_learn_more = forms.BooleanField(label = '', required = False,
                                             help_text = 'I want to learn more about the other side of healthcare.')

    immigration_view = forms.ChoiceField(label='Immigration',
                                       choices=CHOICES_LIST)

    immigration_learn_more = forms.BooleanField(label = '', required = False,
                                             help_text = 'I want to learn more about the other side of immigration.')


class ReportForm(forms.Form):

    why_report = forms.CharField(label = 'Why are you reporting this comment?',
                                 widget=forms.Textarea(attrs={'cols': 60, 'rows': 5}))

