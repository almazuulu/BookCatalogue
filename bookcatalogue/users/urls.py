from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('login/', views.EmailLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('user/activate/<slug:uidb64>/<slug:token>/', views.ActivateAccountView.as_view(), name='activate_account'),
    path('register', views.RegisterView.as_view(), name="register"),
    path('email_confirmation_sent/', views.EmailConfirmationSentView.as_view(), name='email_confirmation_sent'),
]   