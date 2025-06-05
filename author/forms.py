from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm
from .models import AuthorProfile


class RegisterForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'id' : 'required'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'id' : 'required'}))
    confirm_pasword = forms.CharField(required=True)
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password','confirm_pasword']

    # def clean_password2(self):
    #     password = self.cleaned_data.get('password')
    #     password2 = self.cleaned_data.get('password2')

    #     if password != password2:
    #         raise forms.ValidationError("Password and conform password didn't match") # 2 ta password match na korla exception throw korbo
        
    # def clean(self):
    #     data = super().clean()
    #     password = data.get("password")
    #     password2 = data.get("password2")

    #     if password and len(password) <8:
    #         raise forms.ValidationError("Minimum 8 digits is required")

class ChangeUserForm(UserChangeForm):
    password = None
    # profile_picture = forms.ImageField()
    class Meta:
        model = User
        fields = ['first_name', 'last_name',]

class AuthorProfileForm(forms.ModelForm):
    class Meta:
        model = AuthorProfile
        fields = ['bio', 'profile_picture', 'twitter_link', 'facebook_link', 'instagram_link']