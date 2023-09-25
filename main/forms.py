from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CreateUserForm(UserCreationForm):
    MALE = 'M'
    FEMALE = 'F'
    SEX_CHOICES = [
        (MALE, 'Male'),
        (FEMALE, 'Female'),
    ]
    #username = forms.CharField(widget=forms)
    sex = forms.ChoiceField(choices = SEX_CHOICES, widget=forms.RadioSelect)
    age = forms.IntegerField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'sex', 'age']
# class SearchForm(forms.Form):
#     search = forms.CharField()