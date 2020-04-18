import requests
from datetime import datetime, timedelta
from collaborator.songkick_utils import songkick_api_key


def search_songkick_locations(
    location_name: str = "", location_latitude: str = "", location_longitude: str = ""
) -> list:
    """
    Search for locations that songkick groups gigs into. This can be done by either name
    or lat & long. If the search returns no results, returnas an empty list. If the
    request fails, a requests.exceptions.RequestException is raised
    :param location_name: The name of a location to search for as a string.
    :param location_latitude: The  latitude of a location to search as a string. Use
                              decimal degrees positive = north and east.
    :param location_longitude: The  longitude of a location to search as a string. Use
                               decimal degrees positive = north and east.
    :return: A list of locations that could match the one requested ordered from best to
             worst match. Each location is a dictionary with two keys; "city" is the
             city that matches the location, "metroArea" is the songkick location
             that includes this city. A maximum of 10 results will be returned.
    """
    max_locations_returned = 10
    if location_name:
        request = (
            "https://api.songkick.com/api/3.0/search/locations.json?"
            "query={}&apikey={}&per_page={}".format(
                location_name, songkick_api_key(), max_locations_returned
            )
        )
    elif location_latitude and location_longitude:
        request = (
            "https://api.songkick.com/api/3.0/search/locations.json?"
            "location=geo:{},{}&apikey={}&per_page={}".format(
                location_latitude,
                location_longitude,
                songkick_api_key(),
                max_locations_returned,
            )
        )
    else:
        raise RuntimeError("Must provide either a location name or lat and long.")

    response = requests.get(request).json()

    return response["resultsPage"]["results"]["location"]


def get_events_for_location(
    location_id: str, start_date: datetime = None, end_date: datetime = None
) -> list:
    """
    Search songkick for the event calendar for a particular location. Raises a
    requests.exceptions.RequestException if there was an error searching for the API.
    :param location_id: The ID of the songkick metro area to return events for as a
                        string.
    :param start_date: A datetime.datetime object for the earliest event to search for.
                       Defaults to now.
    :param end_date: A datetime.datetime object for the latest event to search for.
                     Defaults to 12 weeks after start_date.
    :return: A list of SongkickEvent objects occurring in the location over the
             specified period of time. Empty list if no events found.
    """
    # API calls return results in pages, with a maximum of 50 results per page.
    results_per_page = 50

    if not start_date:
        start_date = datetime.now()
    if not end_date:
        end_date = start_date + timedelta(weeks=12)
    min_date = start_date.strftime("%Y-%m-%d")
    max_date = end_date.strftime("%Y-%m-%d")

    request = (
        "https://api.songkick.com/api/3.0/metro_areas/{}/calendar.json?"
        "min_date={}&max_date={}&per_page={}&apikey={}".format(
            location_id, min_date, max_date, results_per_page, songkick_api_key()
        )
    )

    response = requests.get(request).json()
    event_list = [
        SongkickEvent(event_json=event)
        for event in response["resultsPage"]["results"]["event"]
    ]

    # If there are any other pages of results, get them now.
    num_pages = (
        response["resultsPage"]["totalEntries"] + results_per_page - 1
    ) // results_per_page
    for additional_page in range(1, num_pages):
        response = requests.get(request, params={"page": additional_page})
        event_list.extend(
            [
                SongkickEvent(event_json=event)
                for event in response["resultsPage"]["results"]["event"]
            ]
        )

    return event_list


class SongkickEvent(object):
    def __init__(self, event_json: dict):
        """
        A songkick event object. Represents an event at a venue (e.g. including all acts
        on a night).
        :param event_json: A dictionary of the JSON songkick Event object.
        """
        self.event_json = event_json
        # The Songkick ID of the event
        self.id = str(event_json["id"])
        # The type of the event. 'Concert' or 'Festival'
        self.type = event_json["type"]
        # The URI of the event on Songkick
        self.type = event_json["uri"]
        # A textual representation of the event
        self.display_name = event_json["displayName"]
        # A datetime.datetime object representing the start time for this event
        self.start = datetime.strptime(
            event_json["start"]["datetime"], format="%Y-%m-%dT%H:%M:%S%z"
        )
        # A list of the artists performing at the event
        self.artists = [
            performance["artist"]["displayName"]
            for performance in event_json["performance"]
        ]
        # The name of the venue hosting the event
        self.venue = event_json["venue"]["displayName"]
        # The status of the event. 'ok', 'cancelled' or 'postponed'
        self.status = event_json["status"]
