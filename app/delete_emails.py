from tqdm import tqdm

from utils import email_utils, general_utils


def main(
        filepath: str
):
    """
    Main function
    :param filepath:
    :return:
    """
    senders = general_utils.load_json(filepath)

    query = {
        "sender": senders,
        "exclude_starred": True
    }
    messages = email_utils.get_emails_by_query(query)

    count = 0
    for message in tqdm(messages):
        message.trash()
        count += 1

    print(f"Moved {count} emails to trash.")


if __name__ == "__main__":
    parser = general_utils.get_arg_parser()
    parser.add_argument("--filepath", type=str, help="Path to file with list of senders")

    kwargs = vars(parser.parse_args())
    main(**kwargs)
