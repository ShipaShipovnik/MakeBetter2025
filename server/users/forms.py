from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User
from django import forms


class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        label="Почта",
        required=False,  # Почта не обязательна
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Почта'})
    )
    name = forms.CharField(
        label="Имя",
        max_length=255,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Имя'})
    )
    login = forms.CharField(
        label="Логин",
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Логин'})
    )
    agreement = forms.BooleanField(
        label="Согласие на обработку персональных данных",
        required=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    password1 = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Пароль'})
    )
    password2 = forms.CharField(
        label="Подтверждение пароля",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Повторите пароль'})
    )

    class Meta:
        model = User
        fields = ['name', 'email','login', 'password1', 'password2', 'agreement']


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Логин",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Логин'})
    )
    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Пароль'})
    )
