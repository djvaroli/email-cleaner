from typing import List, Dict
import re

from simplegmail import Gmail
from simplegmail.message import Message
from simplegmail.query import construct_query

from . import general_utils


PROTECTED_EMAIL_RULES = general_utils.load_json("protected_email_rules", backup=[])


def get_gmail_client(client_secret_file: str = "credentials.json", **kwargs) -> Gmail:
    """
    Returns an instance of simplegmail.Gmail
    :return:
    """
    return Gmail(client_secret_file=client_secret_file, **kwargs)


def get_emails_by_sender(**kwargs) -> Dict[str, List[Message]]:
    """
    Returns a dictionary, where the keys are the names of the recipients and the values
    are lists of email objects
    :return:
    """
    gmail = get_gmail_client()
    messages = gmail.get_messages(**kwargs)
    sender_emails_map = dict()

    for message in messages:
        sender = message.sender
        if sender_emails_map.get(sender):
            sender_emails_map[sender].append(message)
        else:
            sender_emails_map[message.sender] = [message]

    return sender_emails_map


def get_starred_messages():
    """
    Returns the starred messages
    :return:
    """
    gmail = get_gmail_client()
    return gmail.get_starred_messages()


def is_email_protected(email: str, protected_email_rules: List[str] = None):
    """
    Checks whether an email matches one or more of the protected email rules
    :param email:
    :param protected_email_rules:
    :return:
    """
    if protected_email_rules is None:
        protected_email_rules = PROTECTED_EMAIL_RULES

    for rule in protected_email_rules:
        if rule in email:
            return True
    return False


def get_emails_matching_query(query: dict) -> List[Message]:
    """
    Returns a list of simplegmail.message.Message objects that match a specific query
    :param query:
    :return:
    """
    gmail = get_gmail_client()
    return gmail.get_messages(query=construct_query(query))


def get_emails_with_labels(labels: List[str]):
    """
    Returns emails matching specified labels
    :param labels:
    :return:
    """
    query = {
        "labels": labels
    }
    return get_emails_matching_query(query)


def get_emails_from_senders(senders: List[str]):
    """
    Returns a list of emails that match the specified senders
    :param senders:
    :return:
    """
    if len(senders) == 0:
        return []

    query = {
        'sender': senders
    }
    return get_emails_matching_query(query)


def email_from_sender(sender: str):
    """
    Takes as input A Message.sender and returns just the email
    :param sender:
    :return:
    """
    pattern = re.compile(r"\<(.*)\>")
    try:
        return re.findall(pattern, sender)[0]
    except IndexError:
        return sender
