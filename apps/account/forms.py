from django import forms
from django.core.validators import ValidationError
from django.contrib.auth.models import User


class UserRegistrationForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label="Username")
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control'}), label="Email")
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'place-holder': 'your password'}), label="Password1")
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'place-holder': 'your password'}),
        label="Confirm Password")

    def clean_email(self):
        email = self.cleaned_data['email']
        user = User.objects.filter(email=email).exists()

        if user:
            raise ValidationError("Email already registered")
        return email

    def clean_username(self):
        username = self.cleaned_data['username']
        user = User.objects.filter(username=username).exists()

        if user:
            raise ValidationError("Username already registered")
        return username

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
