from abc import ABC
from os import getenv

from slack_sdk import WebClient as SlackClient
from zenlog import log

UNDEFINED_GENERIC_ERROR = 'Undefined method in the inherited class'


class Channel(ABC):

    def send(self, message):
        raise NotImplementedError(f'{UNDEFINED_GENERIC_ERROR} {self.__class__.__name__}')


class Slack(Channel):

    def __init__(self):
        self.channel = getenv('SLACK_CHANNEL')
        self.slack_client = SlackClient(token=getenv('SLACK_API_KEY'))

    def send(self, message):
        # self.slack_client.chat_postMessage(channel=f'#{self.slack_channel}', text=message)
        log.info(f'Sent to Slack: {message=}')


class Email(Channel):

    def __init__(self):
        self.imap_server = getenv('IMAP_SERVER')
        self.imap_port = getenv('IMAP_PORT')
        self.imap_tls = getenv('IMAP_TLS')
        # self.email_server_handler = SomeFakeLib(imap_server, imap_port, imap_tls)

    def send(self, message):
        # self.email_server_handler.send(message)
        log.info(f'Sent by email: {message=}')


class PubSub(Channel):

    def __init__(self):
        self.project_id = getenv('PUBSUB_PROJECT_ID')
        self.subscription_id = getenv('PUBSUB_SUBSCRIPTION_ID')
        # self.subscription_handler = Google.PubSub.Subscription(project_id, subscription_id)

    def send(self, message):
        # subscription_handler.send(message)
        log.info(f'Pushed to pubsub: {message=}')
