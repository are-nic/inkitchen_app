from django.contrib.auth import get_user_model

User = get_user_model()


class EmailAuthBackend:
    """
    Email Authentication Backend

    Позволяет пользователю входить в систему, используя пару электронной почты/пароля,
    а не с парой имени пользователя и пароля.
    """
    def authenticate(self, email=None, password=None):
        """ Аутентификация по email """
        try:
            user = User.objects.get(email=email)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        """ Получить объект Пользователя по user_id """
        try:
            return User.objects.get(pk=user_id)

        except User.DoesNotExist:
            return None
