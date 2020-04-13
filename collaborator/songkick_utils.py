# -*- coding: utf-8 -*-
import os


def songkick_api_key():
    """
    We use an environment variable called SONGKICK_API_KEY to store the songkick developer API key. Use this function
    to access the value.
    :return: The songkick api key as a string
    """
    api_key = os.getenv("SONGKICK_API_KEY")
    if api_key is None:
        raise RuntimeError("No songkick API key provided. Set the SONGKICK_API_KEY environment variable")

    return api_key
