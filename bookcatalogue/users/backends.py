from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            # Пытаемся найти пользователя по email
            user = UserModel.objects.get(email=username)
        except UserModel.DoesNotExist:
            # Если не удалось, пытаемся найти пользователя по username
            return super().authenticate(request, username=username, password=password, **kwargs)
        else:
            # Проверяем пароль пользователя
            if user.check_password(password) and self.user_can_authenticate(user):
                return user

    def get_user(self, user_id):
        UserModel = get_user_model()
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None