import hmac

from section_7.starter_code.models.user import UserModel


def authenticate(username, password):
    """
    Function that get called when a user calls the /auth endpoint
    with their username and password
    :param username:
    :param password:
    :return:
    """
    user = UserModel.find_by_username(username)
    if user and hmac.compare_digest(user.password, password):
        return user

def identity(payload):
    user_id = payload['identity']
    return UserModel.find_by_id(user_id)


