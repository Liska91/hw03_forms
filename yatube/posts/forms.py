from django import forms
from django.contrib.auth import get_user_model
from django.forms import ModelForm

from .models import Post

User = get_user_model()


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ('group', 'text',)
        group = forms.ModelChoiceField(queryset=Post.objects.all(),
                                       required=False, to_field_name='group')
        widgets = {
            'text': forms.Textarea(),
        }

        labels = {
            'group': 'Группа',
            'text': 'Текст'
        }
