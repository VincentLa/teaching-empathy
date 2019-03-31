from django import forms

CHOICES_LIST = (("Very Liberal", "Very Liberal"),
                                        ("Slightly liberal", "Slightly liberal"),
                                        ("Neutral", "Neutral"),
                                        ("Slightly Conservative", "Slightly Conservative"),
                                        ("Very Conservative", "Very Conservative"))


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




