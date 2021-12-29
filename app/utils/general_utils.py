import json
import os
from typing import List, Any
from argparse import ArgumentParser
import logging

from datetime import datetime as dt

import pandas as pd


class ArgParser(ArgumentParser):
    def __init__(self, **kwargs):
        super(ArgParser, self).__init__(**kwargs)

    def add_common_args(self, flags: List[str]):
        """
        Convenience function to add commonly used args to the parser
        :param flags:
        :return:
        """
        for flag in flags:
            if flag == "top_k":
                self.add_argument("--top_k", default=30, type=int, help="Number of senders to show in plots.")

            if flag == "ascending":
                self.add_argument("--ascending", help="Whether to display bottom senders", action="store_true", default=False)

            if flag == "hide_protected":
                self.add_argument("--hide_protected", help="Whether to hide protected emails", action="store_true", default=True)

    def to_dict(self):
        """
        Returns dictionary representation of self
        :return:
        """

        return vars(self.parse_args())


def key_value_to_df(
        dict_: dict,
        keys_column: str,
        values_column: str
) -> pd.DataFrame:
    """
    Converts a dictionary to a pandas DataFrame with 2 columns, where the columns correspond to keys and values.
    :param dict_:
    :param keys_column:
    :param values_column
    :return:
    """

    columns = (keys_column, values_column)
    df_dict = {column: list() for column in columns}

    for k, v in dict_.items():
        df_dict[keys_column].append(k)
        df_dict[values_column].append(v)

    return pd.DataFrame(df_dict)


def get_date_key():
    """
    Returns properly formatted date key
    :return:
    """
    return dt.now().strftime("%dT%H-%M")


def get_arg_parser(flags_to_add: List[str] = None) -> ArgParser:
    """
    Returns an instance of ArgumentParser
    :param flags_to_add:
    :return:
    """
    parser = ArgParser()
    if flags_to_add is not None:
        parser.add_common_args(flags_to_add)

    return parser


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


def load_json(fp: str, mode: str = "r+", backup: Any = None):
    """
    Loads json file and returns data
    :param fp:
    :param mode:
    :param backup: The object to return in case loading of the file fails
    :return:
    """
    if "json" not in fp:
        fp = f"{fp}.json"

    try:
        with open(fp, mode) as f:
            data = json.load(f)
    except Exception:
        if backup is not None:
            data = backup

    return data


def merge_dicts_with_int_values(dict1: dict, dict2: dict):
    """
    Given two dictionaries, where the values are integers combines them by adding
    the values for the same keys
    :param dict1:
    :param dict2"
    :return:
    """
    result = dict1.copy()
    for key, value in dict2.items():
        if result.get(key) is not None:
            result[key] += value
        else:
            result[key] = value

    return result