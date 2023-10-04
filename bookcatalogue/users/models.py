from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils.translation import gettext as _  # Для многоязычности

class BookUser(AbstractUser):
    email = models.EmailField(unique=True)
    favorites = models.ManyToManyField('book.Book', related_name='users_favorited')
    
    # Use email for authentication instead of usernames
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    # Переопределение связанных полей
    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        help_text=_(
            'Группы к которым этот пользователь принадлежит. Пользователь получит все разрешения'
        ),
        related_name="custom_user_set",
        related_query_name="user",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        help_text=_('Конкретные разрешения'),
        related_name="custom_user_set",
        related_query_name="user",
    )
