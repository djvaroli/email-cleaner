from tqdm import tqdm

from app.utils import email_utils, general_utils

logger = general_utils.get_logger("Delete Emails")


def main(
        filepath: str,
        ascending: bool = False,
        hide_protected: bool = True,
        top_k: int = 30
):
    """
    Main function
    :param filepath:
    :param ascending:
    :param hide_protected:
    :param top_k
    :return:
    """

    logger.info("Fetching Emails.")
    count_by_sender = general_utils.load_json(filepath)
    df = general_utils.email_count_by_sender_df(count_by_sender, ascending=ascending, hide_protected=hide_protected)

    senders = df.email[:top_k].values.tolist()

    query = {
        "sender": senders,
        "exclude_starred": True
    }
    messages = email_utils.get_emails_by_query(query)

    count = 0
    for message in tqdm(messages):
        message.trash()
        count += 1

    logger.info(f"Moved {count} emails to trash.")


if __name__ == "__main__":
    parser = general_utils.get_arg_parser(flags_to_add=["top_k", "ascending", "hide_protected"])
    parser.add_argument("--filepath", type=str, help="Path to file with list of senders")

    main(**parser.to_dict())
