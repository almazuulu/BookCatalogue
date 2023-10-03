from django.views import View
from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.conf import settings
from django.utils.encoding import force_str
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from .forms import RegistrationForm, LoginForm
from .models import BookUser
from django.contrib.auth.views import LoginView

from django.contrib.auth.views import LoginView
from django.contrib.auth import views as auth_views
from django.views import generic
from django.urls import reverse_lazy

class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'users/login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data["user"]
            login(request, user)
            return redirect('home')
        return render(request, 'users/login.html', {'form': form})

class EmailLoginView(LoginView):
    template_name = 'your_app/login.html'  # Specify your login template
    authentication_form = LoginForm

    def form_valid(self, form):
        remember_me = form.cleaned_data.get('remember_me')
        if not remember_me:
            self.request.session.set_expiry(0)

        # Access the authenticated user and their email
        if self.request.user.is_authenticated:
            user = self.request.user
            email = user.email
            # You can now use 'user' and 'email' as needed in your view

        return super().form_valid(form)


class RegisterView(View):
    def get(self, request):
        form = RegistrationForm()
        return render(request, 'users/register.html', {'form': form})

    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Deactivate account till it is confirmed
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