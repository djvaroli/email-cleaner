import os

from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv()

ACCOUNT_SID = os.environ["TWILIO_ACCOUNT_SID"]
AUTH_TOKEN = os.environ["TWILIO_AUTH_TOKEN"]
FROM_PHONE_NUMBER = os.environ["FROM_PHONE_NUMBER"]
DEFAULT_TO_NUMBER = os.environ["DEFAULT_NUMBER"]


def get_twilio_client() -> Client:
    """
    Returns an instance of twilio client
    :return:
    """
    return Client(ACCOUNT_SID, AUTH_TOKEN)


def send_sms(to: str, body: str):
    """
    Sends an sms using the twilio client
    :param to:
    :param body:
    :return:
    """
    client = get_twilio_client()
    message = client.messages.create(
        to=to,
        from_=FROM_PHONE_NUMBER,
        body=body
    )
    return message
