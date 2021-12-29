"""
Fetches emails from gmail servers that have the 'blacklisted_senders' label,
identifies the senders from those emails and moves all emails, from said list of senders, to trash.
"""
import os

from app.utils import email_utils, sms_utils, general_utils

logger = general_utils.get_logger("Remove Blacklisted Emails")


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

    stats_message = "\n\nClean-up completed!\n\n"
    for key, value in stats.items():
        stats_message += f"{key} - {value}\n"

    sms_utils.send_sms(sms_utils.DEFAULT_TO_NUMBER, stats_message)

    path_to_global_stats = "data/global_cleanup_stats.json"
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

