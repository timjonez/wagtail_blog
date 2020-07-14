from django import forms
from .models import Prayer

class PrayerForm(forms.ModelForm):

    class Meta:
        model = Prayer
        fields = ['title','content']

        widgets = {
            'title':forms.TextInput(attrs={'class':'textinputclass'}),
            'text':forms.Textarea(attrs={'class':'editable medium-editor-textarea postcontent'})
        }
