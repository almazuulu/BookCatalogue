from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('user/activate/<slug:uidb64>/<slug:token>/', views.ActivateAccountView.as_view(), name='activate_account'),
    path('register', views.RegisterView.as_view(), name="register"),
    path('email_confirmation_sent/', views.EmailConfirmationSentView.as_view(), name='email_confirmation_sent'),
    # path("password_reset/", views.WebPasswordResetView.as_view(), name="password_reset"),
    # path("register_confirm/<token>/", views.register_confirm, name="register_confirm"),
]   