from django import forms
from django.template.defaultfilters import slugify
from .models import Review, Book, Author, Category


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['comment', 'rating']

    def __init__(self, *args, **kwargs):
        initial_rating = kwargs.pop('initial_rating', None)
        super().__init__(*args, **kwargs)

        if initial_rating is not None:
            self.fields['rating'].initial = initial_rating


class EditReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating']


class AddBookForm(forms.ModelForm):
    new_author = forms.CharField(required=False, label="New Author")
    new_category = forms.CharField(required=False, label="New Category")

    class Meta:
        model = Book
        fields = ['title', 'author', 'new_author', 'category', 'new_category', 'description']
        widgets = {
            'author': forms.Select(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        slug = cleaned_data.get('slug')

        if not slug and title:
            cleaned_data['slug'] = slugify(title)

        return cleaned_data

    def save(self, commit=True):
        new_author_name = self.cleaned_data.get('new_author')
        if new_author_name:
            author, created = Author.objects.get_or_create(name=new_author_name)
            self.instance.author = author

        new_category_name = self.cleaned_data.get('new_category')
        if new_category_name:
            category, created = Category.objects.get_or_create(name=new_category_name)
            self.instance.category = category

        # Handle slug
        if not self.instance.slug:
            self.instance.slug = slugify(self.instance.title)

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





