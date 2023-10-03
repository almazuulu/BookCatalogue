from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from .models import BookUser
from django.utils.translation import gettext as _



from django import forms
from django.contrib.auth import authenticate

class LoginForm(forms.Form):
    username_or_email = forms.CharField(label="Имя пользователя или Email")
    password = forms.CharField(widget=forms.PasswordInput, label="Пароль")

    def clean(self):
        cleaned_data = super().clean()
        username_or_email = cleaned_data.get("username_or_email")
        password = cleaned_data.get("password")

        if username_or_email and password:
            user = authenticate(username=username_or_email, password=password)
            if user is None:
                try:
                    user = BookUser.objects.get(email=username_or_email)
                    user = authenticate(username=user.username, password=password)
                except BookUser.DoesNotExist:
                    user = None

            if user is None:
                raise forms.ValidationError("Неверное имя пользователя или пароль.")

            cleaned_data["user"] = user

        return cleaned_data


class RegistrationForm(forms.ModelForm):
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'}),
        label="Пароль"
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}),
        label="Подтверждение пароля"
    )

    class Meta:
        model = BookUser
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
