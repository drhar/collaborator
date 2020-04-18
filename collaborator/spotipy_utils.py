from typing import List
import spotipy


def get_items_from_page(page: dict) -> List[dict]:
    """
    Returns a list of all the items from a Spotify results page.
    :param page: A Spotify page object.
    :return: A list of all the items from the page.
    """
    item_list = []
    print("Retrieving items from page")

    for i, item in enumerate(page["items"]):
        item_list.append(item)

    print("Found {} items".format(len(item_list)))

    return item_list


def get_all_paged_items(
    spotify_connection: spotipy.Spotify, first_page: dict
) -> List[dict]:
    """
    Gets everything wrapped in a Spotify paging object and puts it into an array.
    :param spotify_connection: A logged in connection to Spotify.
    :param first_page: The first Spotify paging object.
    :return: A list of all the items across all the linked paging objects.
    """
    # First, get the items from the first page.
    item_list = get_items_from_page(first_page)

    # Check whether there are any other pages and if so, add the items in them to the
    # list.
    current_page = first_page
    while current_page["next"]:
        current_page = spotify_connection.next(current_page)
        item_list.extend(get_items_from_page(current_page))

    return item_list
