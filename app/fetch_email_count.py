"""
Fetch email count by sender and if instructed plot and save the results.
"""

import os

from utils import email_utils, general_utils, visualization_utils

logger = general_utils.get_logger("Fetch Emails")

figures_root = "interactive_graphs"
if os.path.isdir(figures_root) is False:
    os.mkdir(figures_root)


data_root = "data"
if os.path.isdir(data_root) is False:
    os.mkdir(data_root)


def main(
        save_data: bool = True,
        plot: bool = True,
        top_k: int = 30,
        ascending: bool = False,
        load_from_path: str = None
):
    """
    Main function that fetches the email count by sender data (unless load_from_path is specified)
    and if instructed plots a histogram of email count by sender.

    :param save_data: whether to save the data generated after running the script
    :param plot: whether to plot the data generated after running the scrpt
    :param top_k: how many top senders to include in the final plots
    :param ascending: whether to sort senders by count in ascending order
    :param load_from_path: path to an existing data file (i.e. if only the plots are of interest)
    :return:
    """

    if load_from_path is not None:
        count_by_sender = general_utils.load_json(load_from_path)
    else:
        logger.info("Fetching emails from Gmail servers.")
        emails_by_sender = email_utils.get_emails_by_sender()
        count_by_sender = {sender: len(messages) for sender, messages in emails_by_sender.items()}

        if save_data:
            general_utils.save_json(f"{data_root}/email_count_by_sender", count_by_sender, add_date_key=True)

    email_count_df = general_utils.key_value_to_df(count_by_sender, "sender", "email_count")
    email_count_df = email_count_df.sort_values("email_count", ascending=ascending)
    email_count_df["email"] = email_count_df["sender"].apply(email_utils.email_from_sender)

    if plot:
        logger.info("Plotting Bar Chart.")
        date_key = general_utils.get_date_key()
        bar_chart = visualization_utils.get_bar_chart(email_count_df.email_count[:top_k], email_count_df.sender[:top_k])
        bar_chart.write_html(f"{figures_root}/sender_count-{date_key}.html")

    logger.info("Finished!")


if __name__ == '__main__':
    parser = general_utils.get_arg_parser(flags_to_add=["top_k", "ascending"])
    parser.add_argument("--plot", default=True, help="Whether to save interactive email statistics plots", action="store_true")
    parser.add_argument("--save_data", default=True, help="Whether to save data", action="store_true")
    parser.add_argument("--load_from_path", required=False, type=str)

    main(**parser.to_dict())
