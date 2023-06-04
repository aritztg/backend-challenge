from abc import ABC
from os import getenv

from slack_sdk import WebClient as SlackClient
from zenlog import log

UNDEFINED_GENERIC_ERROR = 'Undefined method in the inherited class'


class Channel(ABC):
    """Channel abstract class to define basic structure.

    To be followed by its implementations. Ensures `send()` mehod to be implemented.
    """

    def send(self, message):
        """This method will be called to pass `message` to endpoints. It must be implemented by inherited classes."""
        raise NotImplementedError(f'{UNDEFINED_GENERIC_ERROR} {self.__class__.__name__}')


class Slack(Channel):
    """Slack channel implementation

    Should initialise a Slack client handler and be ready to send incoming messages to some predefined Slack channel.
    """

    def __init__(self):
        self.channel = getenv('SLACK_CHANNEL')
        self.slack_client = SlackClient(token=getenv('SLACK_API_KEY'))

    def send(self, message):
        # self.slack_client.chat_postMessage(channel=f'#{self.slack_channel}', text=message)
        log.info(f'Sent to Slack: {message=}')


class Email(Channel):
    """Email (SMTP) channel implementation

    Should be able to connect to some SMTP server and send a message via email.
    """

    def __init__(self):
        self.imap_server = getenv('IMAP_SERVER')
        self.imap_port = getenv('IMAP_PORT')
        self.imap_tls = getenv('IMAP_TLS')
        # self.email_server_handler = SomeFakeLib(imap_server, imap_port, imap_tls)

    def send(self, message):
        # self.email_server_handler.send(message)
        log.info(f'Sent by email: {message=}')


class PubSub(Channel):
    """PubSub channel implementation

    Should be able to connect to some pubsub queue and push a message into it.
    """

    def __init__(self):
        self.project_id = getenv('PUBSUB_PROJECT_ID')
        self.subscription_id = getenv('PUBSUB_SUBSCRIPTION_ID')
        # self.subscription_handler = Google.PubSub.Subscription(project_id, subscription_id)

    def send(self, message):
        # subscription_handler.send(message)
        log.info(f'Pushed to pubsub: {message=}')
