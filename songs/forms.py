from django import forms

class termForm(forms.Form):
    terms=[('short_term', 'short term'),
            ('medium_term', 'medium term'),
            ('long_term', 'long term')]

    term_length = forms.ChoiceField(choices=terms, widget=forms.RadioSelect)
