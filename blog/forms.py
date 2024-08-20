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
    new_author = forms.CharField(max_length=100, required=False, label="New Author")
    new_category = forms.CharField(max_length=100, required=False, label="New Category")

    class Meta:
        model = Book
        fields = ['title', 'author', 'description', 'category', 'new_author', 'new_category']
        widgets = {
            'author': forms.Select(attrs={'class': 'mr-2'}),
            'new_author': forms.TextInput(attrs={'class': 'flex-grow-1'}),
            'category': forms.Select(attrs={'class': 'mr-2'}),
            'new_category': forms.TextInput(attrs={'class': 'flex-grow-1'}),
        }

    def save(self, commit=True):
        new_author_name = self.cleaned_data.get('new_author')
        if new_author_name:
            author, created = Author.objects.get_or_create(name=new_author_name)
            self.instance.author = author

        new_category_name = self.cleaned_data.get('new_category')
        if new_category_name:
            category, created = Category.objects.get_or_create(name=new_category_name)
            self.instance.category = category

        return super().save(commit=commit)


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





