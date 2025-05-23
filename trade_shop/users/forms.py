from django import forms


class UserLoginForm(forms.Form):
    username = forms.CharField(label='Логин',
                               widget=forms.TextInput())
    password = forms.CharField(label='Пароль',
                               widget=forms.PasswordInput())