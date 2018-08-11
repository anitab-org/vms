from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six


class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        """
        generates token for email confirmation url

        :param timestamp: to check the token expiry
        :param user: for whom token is generated
        :return: token
        """
        return (
            six.text_type(user.pk) + six.text_type(timestamp) +
            six.text_type(user.username)
        )


account_activation_token = TokenGenerator()

