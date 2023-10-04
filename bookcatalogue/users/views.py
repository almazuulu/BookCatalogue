from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from django.core.mail import send_mail
from django.shortcuts import redirect, render   
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views import View
from django.views.generic import TemplateView

# Локальные импорты
from .forms import EmailAuthenticationForm, RegistrationForm
from .models import BookUser


class EmailLoginView(LoginView):
    form_class = EmailAuthenticationForm
    template_name = 'users/login.html'
    
class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('login')

class RegisterView(View):
    def get(self, request):
        form = RegistrationForm()
        return render(request, 'users/register.html', {'form': form})

    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = form.cleaned_data['email']  # Используйте email как значение для username
            user.set_password(form.cleaned_data['password1'])  # Установите пароль
            user.is_active = False
            user.save()

            # Generate email confirmation token
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            mail_subject = 'Activate your account.'
            message = render_to_string('users/active_email.html', {
                'user': user,
                'domain': request.META['HTTP_HOST'],
                'uid': uid,
                'token': token,
            })

            send_mail(mail_subject, message, settings.EMAIL_FROM, [user.email])

            return redirect('email_confirmation_sent')
        return render(request, 'users/register.html', {'form': form})


class EmailConfirmationSentView(TemplateView):
    template_name = 'users/email_confirmation_sent.html'


class ActivateAccountView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = BookUser.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, BookUser.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return render(request, 'users/activation_successful.html')
        else:
            return render(request, 'users/activation_failed.html')