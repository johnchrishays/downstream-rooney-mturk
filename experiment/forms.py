from django import forms
from django.utils.safestring import mark_safe


class ParamForm(forms.Form):
    CHOICES=[('select1', 'select 1'),
             ('select2', 'select 2')]

    like = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)
    n_x = forms.IntegerField(label='Number blue candidates (n_X)', initial="50")
    n_y = forms.IntegerField(label='Number red candidates (n_Y)', initial="50")
    k = forms.IntegerField(label='Number candidates to select (k)', initial="10")
    l = forms.IntegerField(label='Minimum number blue candidates to select (l)', initial="3")
    n_iterations = forms.IntegerField(label='Number of iterations (t_max)', initial="20")


class CandidateForm(forms.Form):
    checked = forms.BooleanField(required=False, label="",
                                 widget=forms.CheckboxInput)


class ConsentForm(forms.Form):
    CHOICES = [('Yes', 'Yes'),
               ('No', 'No')]
    over_18 = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect,
                                label="Are you at least 18 years old?")
    willing_to_participate = forms.ChoiceField(
        choices=CHOICES,
        widget=forms.RadioSelect,
        label="Would you like to participate in the study?")


class EndQuestionnaireForm(forms.Form):
    difference_red_blue = forms.CharField(widget=forms.Textarea,label=mark_safe("<br/>Did you notice a difference between the red and blue buttons? If yes, what was it?<br/>"))
    dominant_strategy = forms.CharField(widget=forms.Textarea,label=mark_safe("<br/>Did you change you strategy between the beginning and the end? If so, how?<br/>"))
    thoughts = forms.CharField(widget=forms.Textarea,label=mark_safe("<br/>Any comments, questions or thoughts?<br/>"))


