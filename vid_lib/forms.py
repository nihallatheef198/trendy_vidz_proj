from . import models
from django import forms


class video_form(forms.ModelForm):
    class Meta:
        model = models.video
        fields = ['url']
        labels = {'url':'Youtube URL'}


class search_form(forms.Form):
    search_term = forms.CharField(label='Search for a video')
