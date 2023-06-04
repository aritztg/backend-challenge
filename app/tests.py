# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
import logging
from os import getenv
from unittest import TestCase

from dotenv import load_dotenv
from fastapi.testclient import TestClient

from app.backend import INPUT_PATH, app

# Load env variables from `.env`.
load_dotenv()

# Mute existing app logger (because of zenlog).
logger = logging.getLogger('pythonConfig')
logger.handlers = []

# TestClient to be used for web app tests.
client = TestClient(app)


# Set some useful constants.
VALID_TOKEN = getenv('VALID_CSRF_TOKEN')
INVALID_TOKEN = '123def'

VALID_TOPIC = 'sales'
UNKNOWN_TOPIC = 'delivery'
DESCRIPTION = 'Hi there!'

VALID_MESSAGE = {
    'topic': VALID_TOPIC,
    'description': DESCRIPTION
}

VALID_MESSAGE_WRONG_TOPIC = {
    'topic': UNKNOWN_TOPIC,
    'description': DESCRIPTION
}

INVALID_MESSAGE = {
    'wrong_topic_fieldname': VALID_TOPIC,
    'description': DESCRIPTION
}


class BackendAppTests(TestCase):

    def test_invalid_topic(self):
        response = client.post(INPUT_PATH, params={'csrf_token': VALID_TOKEN}, json=VALID_MESSAGE)
        assert response.status_code == 200

    def test_malformed_input(self):
        # Wrong schema.
        response = client.post(INPUT_PATH, params={'csrf_token': VALID_TOKEN}, json=INVALID_MESSAGE)
        assert response.status_code == 422

        # No topic.
        response = client.post(INPUT_PATH, params={'csrf_token': VALID_TOKEN}, json={'description': DESCRIPTION})
        assert response.status_code == 422

        # No description.
        response = client.post(INPUT_PATH, params={'csrf_token': VALID_TOKEN}, json={'topic': VALID_TOPIC})
        assert response.status_code == 422

    def test_unknown_topic(self):
        response = client.post(INPUT_PATH, params={'csrf_token': VALID_TOKEN}, json=VALID_MESSAGE_WRONG_TOPIC)

        assert response.status_code == 400
        assert response.json() == {'detail': f'Malformed. Invalid topic "{UNKNOWN_TOPIC}".'}

    def test_empty_description(self):
        message_empty_description = {'topic': VALID_TOPIC, 'description': ''}
        response = client.post(INPUT_PATH, params={'csrf_token': VALID_TOKEN}, json=message_empty_description)

        assert response.status_code == 400
        assert response.json() == {'detail': 'Malformed. No description.'}


class BackendSecurityTests(TestCase):

    def test_no_token(self):
        response = client.post(INPUT_PATH, json={'topic': VALID_MESSAGE})
        assert response.status_code == 422

    def test_wrong_token(self):
        response = client.post(INPUT_PATH, params={'csrf_token': INVALID_TOKEN}, json={'topic': VALID_MESSAGE})

        assert response.status_code == 403
        assert response.json() == {'detail': 'Unauthorised. Invalid CSRF Token.'}
