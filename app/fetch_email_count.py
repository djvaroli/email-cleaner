"""
Fetch email count by sender
"""

import os

from utils import email_utils, general_utils, visualization_utils


logger = general_utils.get_logger("Fetch Emails")

figures_root = "interactive_graphs"
if os.path.isdir(figures_root) is False:
    os.mkdir(figures_root)


def main(
        save: bool = True,
        plot: bool = True,
        top_k: int = 30,
        ascending: bool = False,
        hide_protected: bool = True
):
    """
    Main function
    :param save:
    :param plot:
    :param top_k:
    :param ascending:
    :param hide_protected:
    :return:
    """
    logger.info("Fetching emails from Gmail servers.")
    emails_by_sender = email_utils.get_emails_by_sender()

    count_by_sender = {sender: len(messages) for sender, messages in emails_by_sender.items()}

    if save:
        general_utils.save_json("data/email_count_by_sender", count_by_sender, add_date_key=True)

    df = general_utils.email_count_by_sender_df(count_by_sender, ascending=ascending, hide_protected=hide_protected)

    if plot:
        logger.info("Plotting Bar Chart.")
        date_key = general_utils.get_date_key()
        bar_chart = visualization_utils.get_bar_chart(df.email_count[:top_k], df.sender[:top_k])
        bar_chart.write_html(f"{figures_root}/sender_count-{date_key}.html")

    logger.info("Finished!")


if __name__ == '__main__':
    parser = general_utils.get_arg_parser(flags_to_add=["top_k", "ascending", "hide_protected"])
    parser.add_argument("--plot", default=True, help="Whether to save interactive email statistics plots", action="store_true")
    parser.add_argument("--save", default=True, help="Whether to save data", action="store_true")

    main(**parser.to_dict())
