from django import forms

class termForm(forms.Form):
    terms=[('short_term', 'short term'),
            ('medium_term', 'medium term'),
            ('long_term', 'long term')]

    username = forms.CharField(label='username',max_length=100)
    term_length = forms.ChoiceField(choices=terms, widget=forms.RadioSelect)
