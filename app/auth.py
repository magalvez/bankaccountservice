"""
JWT Authentication User Token
"""
import logging
import pytz

from app import app

from datetime import datetime

from flask_jwt import JWT

from default_config import JWT_AUTH_URL_RULE, SECRET_KEY

app.config["JWT_AUTH_URL_RULE"] = JWT_AUTH_URL_RULE
app.config['JWT_SECRET_KEY'] = SECRET_KEY
jwt = JWT(app)


@jwt.authentication_handler
def authenticate(username, password):
    """
    Method in charge of consulting user information
    :param username: String, User Name: 'jzambrano@lendingfront.com'
    :param password: String, Password: 'dkljjk3j34'
    :return: User, returns user information
    """
    logging.info('Authentication user token started')

    user_response = {
        'user': {'id': 0}
    }

    return user_response['user']


@jwt.user_handler
def load_user(payload):
    """
    Load token information
    :param payload: Dict, User information. Ie,
    {
        'client_id': 23,
        'user_id': 1960,
        'email': 'jzambrano@lendingfront.com'
        ....
    }
    :return: User, Ie,
        {
        'client_id': 23,
        'user_id': 1960,
        'email': 'jzambrano@lendingfront.com',
        .....
        'token': 'ajfsdkljf23kj23klj32kl243h32'
    }
    """

    payload["user_token"] = jwt.encode_callback(payload)
    return payload


@jwt.payload_handler
def make_payload(user):
    """
    Generate user token
    :param user: User object
    :return payload: token generated. String, Ie. 'ajfsdkljf23kj23klj32kl243h32'
    """

    payload = {
        "user_id": user['user_id'],
        "expiration_date": (
            datetime.utcnow() + app.config["JWT_EXPIRATION_DELTA"]
        ).strftime("%m/%d/%Y"),
        "expire_date": (datetime.now(pytz.timezone('America/Bogota')) + app.config["JWT_EXPIRATION_DELTA"]).strftime('%m/%d/%Y %H:%M:%S'),
        "exp": (datetime.now(pytz.timezone('America/Bogota')) + app.config["JWT_EXPIRATION_DELTA"]).timestamp()
    }

    return payload


@jwt.response_handler
def make_response(payload):
    """
    Response for successful authentication
    :return payload: string, JWT token. Ie, "12345.sadfgh.12345"
    :return dict: http respone. Ie, {
        "name": "John Doe",
        "token": "12345.sadfgh.12345",
    }
    """

    user = jwt.decode_callback(payload)

    return {
        "user_id": user['user_id'],
        "token": payload,
    }
