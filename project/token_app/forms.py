from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Crypto
from .models import Review

class RegisterUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
    
    def __init__(self, *args, **kwargs):
        super(RegisterUserForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class':'form-control', 'placeholder': 'Enter username....'})
        self.fields['password1'].widget.attrs.update({'class':'form-control'})
        self.fields['password2'].widget.attrs.update({'class':'form-control'})

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('exchange', 'rating', 'comment')

    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)
        self.fields['exchange'].widget.attrs.update({'class':'form-control', 'placeholder': 'Enter username....'})
        self.fields['rating'].widget.attrs.update({'class':'form-control'})
        self.fields['comment'].widget.attrs.update({'class':'form-control'})

class CryptoForm(forms.ModelForm):
    class Meta:
        model = Crypto
        fields = ['exchange', 'coin', 'price', 'alerts']