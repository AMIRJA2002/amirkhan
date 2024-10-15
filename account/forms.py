from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    full_name = forms.CharField(label='نام و نام خانوادگی', max_length=100)

    class Meta:
        model = CustomUser
        fields = ('full_name', 'phone_number', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.full_name = self.cleaned_data['full_name']
        if commit:
            user.save()
        return user

    phone_number = forms.CharField(
        label='شماره تلفن'
    )

class CustomAuthenticationForm(AuthenticationForm):
    phone_number = forms.CharField(label='شماره تلفن')
    password = forms.CharField(label='رمز عبور', widget=forms.PasswordInput)
