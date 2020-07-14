from django import forms
from .models import Post, Comment
from django_summernote.widgets import SummernoteWidget

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['author','title','text']

        widgets = {
            'title':forms.TextInput(attrs={'class':'textinputclass'}),
            'text':SummernoteWidget(),
        }

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('author','text')

#Might need to add aditional lines here from blog project?

#attrs={'class':'editable medium-editor-textarea postcontent'}
