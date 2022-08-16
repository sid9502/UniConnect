from django import forms 
from .models import post,comment 

class PostForm(forms.ModelForm):
    content=forms.CharField(

        label='',
        widget=forms.Textarea(attrs={
            'rows':'3',
             
            'placeholder':'Your experience...'
             
        })
    )
    image=forms.ImageField(required=False)
    class Meta:
        model=post 
        fields=['content','image']

class CommentForm(forms.ModelForm):
    comment=forms.CharField(

        label='',
        widget=forms.Textarea(attrs={
            'rows':'3',
            'placeholder':'Your comment...'
             
        })
    )
    class Meta:
        model=comment
        fields=['comment']