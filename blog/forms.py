from django import forms
from .models import Review, CustomUser
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['comment', 'rating']


class CreateCustomUser(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'age', 'email', 'gender']


class ChangeCustomUser(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'age', 'email', 'gender']


class LoginCustomUser(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'password']


class RegisterCustomUser(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.fields['username'].help_text = ""
        self.fields['password1'].help_text = ""
        self.fields['password2'].help_text = ""

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'age', 'gender']
