from django import forms
from .models import Review, Book, Author, Category


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['comment', 'rating']


class EditReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating']


class AddBookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'description', 'category']


class BookFilterForm(forms.Form):
    author = forms.ModelChoiceField(queryset=Author.objects.all(), required=False, label='Author')
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=False, label='Category')
    min_rating = forms.FloatField(
        required=False,
        label='Min Rating',
        widget=forms.NumberInput(attrs={'step': '0.1'})
    )
    max_rating = forms.FloatField(
        required=False,
        label='Max Rating',
        widget=forms.NumberInput(attrs={'step': '0.1'})
    )





