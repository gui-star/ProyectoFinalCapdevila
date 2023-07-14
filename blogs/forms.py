from django import forms
from .models import *
from django.core.validators import MinValueValidator, MaxValueValidator

class RatingForm(forms.Form):
    RATING_CHOICES = [(str(i), str(i)) for i in range(11)]
    rating = forms.ChoiceField(choices=RATING_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}), required=True)

    
class CreateBlogForm(forms.ModelForm):
    rating = forms.FloatField(min_value=0.1, max_value=10)
    class Meta:
        model = Blog
        fields = ['title', 'subtitle', 'body', 'image', 'rating']
        
        
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']