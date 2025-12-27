from django import forms
from .models import BlogPost

class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'text']
        labels = {'title': '文章标题', 'text': '文章内容'}
        widgets = {'text': forms.Textarea(attrs={'cols': 80})}