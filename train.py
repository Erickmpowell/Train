"""
The point of the script is to display the upcoming train times for davis station.

It is done by calling the MBTA api, organizing this data, and then displaying the result.

"""

import datetime
import tkinter as tk
import time
import requests
import matplotlib

matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def get_trains():
    """
    This is the API call to MBTA to get the train times
    inputs: none
    outputs: 2 arrays
      1. Times of arrival for each train
      2. Destination of each train
    """

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


# print(alewife,ashmont,braintree)

arr, direction = get_trains()

data = simplify_data(arr, direction)

print(data)


def loop():
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


class update_train(tk.Text):
    def __init__(self, *args, **kwargs):
        tk.Text.__init__(self, *args, **kwargs)
        self._count = 0

    def update(self):
        self.delete("1.0", "end")
        updated_text = loop()
        self.insert(tk.END, updated_text)
        self._count += 1
        self.after(5000, self.update)


root = tk.Tk()

mywidget = update_train(root, font=("Helvetica", 45), bg="black", fg="white")
mywidget.pack()
mywidget.update()


root.minsize(625, 225)
root.title("MBTA prediction")
root.geometry("1000x600+50+50")


print("Main loop")
root.mainloop()
print("STOP FIGHTING")
time.sleep(2)

fig = plt.figure(1)

plt.plot([1, 2, 3, 4], [2, 3, 4, 3])
canvas = FigureCanvasTkAgg(fig, master=root)
plot_widget = canvas.get_tk_widget()
fig.canvas.draw()
plot_widget.grid(row=0, column=0)


text = tk.Text(root, font=("Helvetica", 45), bg="black", fg="white")
text.pack()


while True:
    text.delete("1.0", "end")
    new_text = loop()
    text.insert(tk.END, new_text)
    text.update()
    time.sleep(5)
