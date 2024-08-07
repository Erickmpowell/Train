import datetime

import time
import requests


def get_trains():
    """
    This is the API call to MBTA to get the train times
    inputs: none
    outputs: 2 arrays
      1. Times of arrival for each train
      2. Destination of each train
    """
    # Perhaps this URL? https://api-v3.mbta.com/predictions?filter[stop]=place-davis&filter[route]=Red&include=trip,vehicle
    api_address = (
        "https://api-v3.mbta.com/predictions"
        + "?filter[stop]=place-davis&filter[route]=Red&include=trip"
    )
    try:
        trips = requests.get(api_address, timeout=5).json()
    except requests.exceptions.Timeout:
        print("Timed Out")

    trip_ids_prediction = []
    arrival_times_prediction = []
    trip_ids_included = []
    direction_included = []

    datalength = len(trips["data"])
    for i in range(datalength):
        trip_ids_prediction.append(
            trips["data"][i]["relationships"]["trip"]["data"]["id"]
        )
        arrival_times_prediction.append(trips["data"][i]["attributes"]["arrival_time"])

        trip_ids_included.append(trips["included"][i]["id"])
        direction_included.append(trips["included"][i]["attributes"]["headsign"])

    matched = []
    for tripi in trip_ids_prediction:
        matched.append(trip_ids_included.index(tripi))

    dir_sort = [direction_included[i] for i in matched]

    return arrival_times_prediction, dir_sort


def get_trains_plus_position():
    """
    This is the API call to MBTA to get the train times
    inputs: none
    outputs: 2 arrays
      1. Times of arrival for each train
      2. Destination of each train
    """
    # Perhaps this URL? https://api-v3.mbta.com/predictions?filter[stop]=place-davis&filter[route]=Red&include=trip,vehicle
    api_address = (
        "https://api-v3.mbta.com/predictions"
        + "?filter[stop]=place-davis&filter[route]=Red&include=trip,vehicle"
    )
    try:
        trips = requests.get(api_address, timeout=5).json()
    except requests.exceptions.Timeout:
        print("Timed Out")

    trip_ids_prediction = []
    Vehicle_ids_prediction = []
    arrival_times_prediction = []

    trip_ids_trips = []
    direction_trips = []

    Vehicle_ids_vehicles = []
    position_vehicles = []

    datalength = len(trips["data"])
    for i in range(datalength):
        trip_ids_prediction.append(
            trips["data"][i]["relationships"]["trip"]["data"]["id"]
        )
        Vehicle_ids_prediction.append(
            trips["data"][i]["relationships"]["vehicle"]["data"]["id"]
        )
        arrival_times_prediction.append(trips["data"][i]["attributes"]["arrival_time"])

    for included_i in trips["included"]:
        if included_i["type"] == "trip":
            trip_ids_trips.append(included_i["id"])
            direction_trips.append(included_i["attributes"]["headsign"])

        if included_i["type"] == "vehicle":
            Vehicle_ids_vehicles.append(included_i["id"])
            position_vehicles.append(
                [
                    included_i["attributes"]["latitude"],
                    included_i["attributes"]["longitude"],
                ]
            )

    trip_match = []
    vehicle_match = []
    for tripi in trip_ids_prediction:
        trip_match.append(trip_ids_trips.index(tripi))
    for vehiclei in Vehicle_ids_prediction:
        vehicle_match.append(Vehicle_ids_vehicles.index(vehiclei))

    dir_sort = [direction_trips[i] for i in trip_match]
    position_sorted = [position_vehicles[i] for i in vehicle_match]

    return arrival_times_prediction, dir_sort, position_sorted


def simplify_data_plus_position(arrivals, directions, positions):
    """
    Takes the the output of the api and takes just the 2 trips that will be soonest for each train
    """
    now = datetime.datetime.now()

    alewife = {"ETA": [], "position": []}
    ashmont = {"ETA": [], "position": []}
    braintree = {"ETA": [], "position": []}
    dir_dict = {"Alewife": alewife, "Ashmont": ashmont, "Braintree": braintree}

    for i, arri in enumerate(arrivals):
        if (
            len(alewife["ETA"])
            == 2 & len(braintree["ETA"])
            == 2 & len(ashmont["ETA"])
            == 2
        ):
            break

        train = directions[i]
        position = positions[i]

        if len(dir_dict[train]["ETA"]) < 2:
            arrival_date, arrival_time = arri.split("T")
            arrival_time = list(map(int, arrival_time.split("-")[0].split(":")))

            diff = (
                (arrival_time[0] - now.hour) * 60
                + (arrival_time[1] - now.minute)
                + (arrival_time[2] - now.second) * 1 / 60
            )
            if diff < 1:
                diff = 0
            else:
                diff = int(diff)
            dir_dict[train]["ETA"].append(diff)
            dir_dict[train]["position"].append([position])

            print(
                directions[i], " is ", diff, " minutes away and at ", position
            )  # ,arrivalTimes_prediction[i] )

    return dir_dict


def simplify_data(arrivals, directions):
    """
    Takes the the output of the api and takes just the 2 trips that will be soonest for each train
    """
    now = datetime.datetime.now()

    alewife = []
    ashmont = []
    braintree = []
    dir_dict = {"Alewife": alewife, "Ashmont": ashmont, "Braintree": braintree}

    for i, arri in enumerate(arrivals):
        if len(alewife) == 2 & len(braintree) == 2 & len(ashmont) == 2:
            break

        train = directions[i]

        if len(dir_dict[train]) < 2:
            arrival_date, arrival_time = arri.split("T")
            arrival_time = list(map(int, arrival_time.split("-")[0].split(":")))

            diff = (
                (arrival_time[0] - now.hour) * 60
                + (arrival_time[1] - now.minute)
                + (arrival_time[2] - now.second) * 1 / 60
            )
            if diff < 1:
                diff = 0
            else:
                diff = int(diff)
            dir_dict[train].append(diff)

            print(
                directions[i], " is ", diff, " minutes away"
            )  # ,arrivalTimes_prediction[i] )
    return dir_dict


def text_gen(train_times):
    """
    Takes simplified train times and constructs
    the final string used for the widget
    """
    alltext = ""
    for train in ["Alewife", "Ashmont", "Braintree"]:
        traintext = (
            train
            + ":   "
            + str(train_times[train][0])
            + " , "
            + str(train_times[train][1])
            + " minutes away"
        )
        alltext = alltext + traintext + "\n\n"

    alltext = alltext[:-2]
    return alltext


def text_gen_plus_position(train_times):
    """
    Takes simplified train times and constructs
    the final string used for the widget
    """
    alltext = ""
    for train in ["Alewife", "Ashmont", "Braintree"]:
        traintext = (
            train
            + ":   "
            + str(train_times[train]["ETA"][0])
            + " , "
            + str(train_times[train]["ETA"][1])
            + " minutes away"
        )
        alltext = alltext + traintext + "\n\n"

    alltext = alltext[:-2]
    return alltext


def train_loop():
    """
    The main loop that is needed to update the widget.
    1. calls api
    2. simplifies api output
    3. constructs string

    returns just the final string
    """
    times, directions = get_trains()

    times_simple = simplify_data(times, directions)

    train_times_simple = text_gen(times_simple)

    return train_times_simple


def train_loop_plus_position():
    times, directions, positions = get_trains_plus_position()
    times_simple = simplify_data_plus_position(times, directions, positions)

    return times_simple

    train_times_simple = text_gen_plus_position(times_simple)
    print(train_times_simple)


train_loop()
train_loop_plus_position()
