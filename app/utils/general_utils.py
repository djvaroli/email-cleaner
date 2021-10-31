import json
import os
from typing import List
from argparse import ArgumentParser
import logging

from datetime import datetime as dt
import pandas as pd

from utils import email_utils


def email_count_by_sender_df(
        email_count_by_sender: dict = None,
        path_to_file: str = None,
        ascending: bool = False,
        hide_protected: bool = False
) -> pd.DataFrame:
    """
    Returns a df of email counts by sender
    :param email_count_by_sender
    :param path_to_file:
    :param ascending:
    :param hide_protected
    :return:
    """

    if not email_count_by_sender and not path_to_file:
        raise Exception("Must specify file or provide data to function")

    if email_count_by_sender is None:
        email_count_by_sender = load_json(path_to_file)

    df_dict = {
        "sender": [],
        "email_count": []
    }

    for k, v in email_count_by_sender.items():
        df_dict["sender"].append(k)
        df_dict["email_count"].append(v)

    df = pd.DataFrame(df_dict)
    df = df.sort_values("email_count", ascending=ascending)

    if hide_protected:
        df["is_protected"] = df.sender.apply(email_utils.is_email_protected).astype("uint")
        df = df[df.is_protected == 0]
        df = df.drop(columns=["is_protected"])

    return df


def get_date_key():
    """
    Returns properly formatted date key
    :return:
    """
    return dt.now().strftime("%dT%H-%M")


def get_arg_parser():
    """
    Returns an instance of ArgumentParser
    :return:
    """
    return ArgumentParser()


def get_logger(name: str, level=logging.INFO, format_: str = None):
    """
    Returns a formatted logger
    :param name:
    :param level:
    :param format_:
    :return:
    """
    logger = logging.getLogger(name)
    console_handler = logging.StreamHandler()

    if format_ is None:
        format_ = '%(asctime)s - %(name)s - %(message)s'

    formatter = logging.Formatter(format_)
    logger.setLevel(level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    return logger


def save_json(fp: str, obj, mode: str = "w+", add_date_key: bool = False) -> str:
    """
    Saves a specified file in json format
    :param fp:
    :param obj: object to save
    :param mode:
    :param add_date_key: whether to add a date key at the end of the file name
    :return:
    """
    if fp.endswith(".json"):
        fn, extension = fp.split(".")
    else:
        fn, extension = fp, "json"

    path = os.path.dirname(fn)
    if os.path.isdir(path) is False:
        os.makedirs(path)

    if add_date_key:
        fn = f"{fn}-{get_date_key()}"

    fp = f"{fn}.{extension}"
    with open(fp, mode) as f:
        json.dump(obj, f)

    return fp


def load_json(fp: str, mode: str = "r+"):
    """
    Loads json file and returns data
    :param fp:
    :param mode:
    :return:
    """
    if "json" not in fp:
        fp = f"{fp}.json"

    with open(fp, mode) as f:
        data = json.load(f)

    return data
