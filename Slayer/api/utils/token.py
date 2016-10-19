import jwt
from django.conf import settings

from main.models import MainUser, TokenLog
import time


def create_token(user):
    """
    Creates token string.
    :param user: User for which token should be created.
    :return: authentication token.
    """
    info = {
        'username': user.username,
        'timestamp': time.time()
    }
    token = jwt.encode(info, settings.JWT_KEY, settings.JWT_ALGORITHM)
    # save token to TokenLog
    TokenLog.objects.create(user=user, token=token)
    return token


def verify_token(token_string):
    """
    Verifies token string.

    :param token_string: Token string to verify.
    :return: {iin, tin} tuple, if token is valid; None - token is invalid.
    """
    try:
        result = jwt.decode(token_string, settings.JWT_KEY, settings.JWT_ALGORITHM)
        username = result['username']
        # Check if token exists in TokenLog and not deleted
        user = MainUser.objects.get(username=username)
        if user.is_active:
            token = user.tokens.get(token=token_string, deleted=False)
            # TODO(Askar) update token.session_id if timestamp < datetime.now() - 25 mins
            # return dictionary of values
            return token.full()
        return None            
    except Exception, e:
        print e  # TODO(askar): log this exception.
        return None
