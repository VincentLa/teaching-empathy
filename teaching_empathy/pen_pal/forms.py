from django import forms


class ProfileForm(forms.Form):
    abortion_view = forms.ChoiceField(label = 'Abortion',
                                   choices=((1, "Very Liberal"),
                                        (2, "Slightly liberal"),
                                        (3, "Ambivalent"),
                                        (4, "Slightly Conservative"),
                                        (5, "Very Conservative")))


