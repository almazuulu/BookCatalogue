from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext as _

from .models import BookUser

class EmailAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(
        label="Email", 
        widget=forms.EmailInput(attrs={'autofocus': True})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(),
        label="Password"
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['password'].widget.attrs['class'] = 'form-control'


class RegistrationForm(forms.ModelForm):
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'}),
        label=_("Пароль")
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': _('Confirm Password')}),
        label=_("Подтверждение пароля")
    )

    class Meta:
        model = BookUser
        fields = ['email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
