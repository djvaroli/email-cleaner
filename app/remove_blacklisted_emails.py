"""
Fetches emails from gmail servers that have the 'blacklisted_senders' label,
identifies the senders from those emails and moves all emails, from said list of senders, to trash.
"""
import os

from utils import email_utils, sms_utils, general_utils

logger = general_utils.get_logger("Remove Blacklisted Emails")


data_root = "data"
if os.path.isdir(data_root) is False:
    os.mkdir(data_root)


def main():
    """
    Main script function
    :return:
    """

    sms_utils.send_sms(sms_utils.DEFAULT_TO_NUMBER, "Beginning email cleanup!")
    blacklisted_emails = email_utils.get_emails_with_labels(["blacklisted_senders"])

    blacklisted_senders = set()
    for email in blacklisted_emails:
        sender = email_utils.email_from_sender(email.sender)
        blacklisted_senders.add(sender)

    # fetch all emails from the blacklisted senders
    messages_to_trash = email_utils.get_emails_from_senders(list(blacklisted_senders))

    stats = {}
    for message in messages_to_trash:
        sender = message.sender
        if not stats.get(sender):
            stats[sender] = 1
        else:
            stats[sender] += 1

        message.trash()

    sms_utils.send_sms(sms_utils.DEFAULT_TO_NUMBER, "Clean-up completed!")

    path_to_global_stats = f"{data_root}/global_cleanup_stats.json"
    if os.path.isfile(path_to_global_stats):
        global_stats = general_utils.load_json(path_to_global_stats)
        global_stats = general_utils.merge_dicts_with_int_values(global_stats, stats)
    else:
        global_stats = stats

    general_utils.save_json(path_to_global_stats, global_stats)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.error(e)
        sms_utils.send_sms(sms_utils.DEFAULT_TO_NUMBER, "Something went wrong!")

