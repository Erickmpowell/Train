import tkinter as tk

# importing frames that we will create soon!
#from TextWidget.TextWidget import TextWidget


#from DataFrame.DataFrame import DataFrame
#from DataFrame.Train_data import get_train_json,process_train_json
#from DataFrame.Train_data import text_gen,stale_update_text
import time
import datetime



class Main(tk.Tk):
    """
    Main function used for the tkinter project
    This is the "root" of the whole project and is the main window
    It creates teh window and all the subframes along with data pulling
    """

    def __init__(self):
        tk.Tk.__init__(self)

        # Sets the screen size of the GUI
        # print(self.global_trains)
        # print(dir(self))
        self.width = 1200
        self.height = 800
        self.geometry(str(self.width) + "x" + str(self.height) + "+0+0")

        self.title("project_title")

        # The container is a frame that contains the projects's frames
        container = tk.Frame(
            self,
            height=self.height,
            width=self.width,
        )
        
        ### Get first api call
        
        api_call,success = None, False
        while not(success): 
            api_call,success = get_train_json()
        print(api_call)
        First_trains = process_train_json(api_call)

        
        container.__setattr__("local_trains", First_trains)
        container.__setattr__("global_trains", 0)
        container.__setattr__("trains_json",api_call)
        container.__setattr__("last_update",datetime.datetime.now())
        container.__setattr__("stale_update",False)
        container.__setattr__("iters",0)
            
        
        # Pack the container to the root
        container.pack(side="top", fill="both", expand=True)

        # Fixes pack location of the container using grid
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Create empty dictionary of frames
        self.frames = {}

        # Use container as master frame for imported frames
        t0 = time.time()

        t1 = time.time()
        print("working on widget:" )
        self.frames[TextWidget] = TextWidget(container)
        self.frames[TextWidget].grid(row=0, column=0, sticky="nsew")
        print("Time elapsed:",t1-t0)
        t0=t1


        # The start page is raised to the top at the beginning.
        print("showing text widget")
        self.show_textwidget( )
    
    def show_textwidget(self):
        frame = self.frames[TextWidget]
        print("raising widget")
        frame.tkraise()

class TextWidget(tk.Text):
    def __init__(self, ParentFrame):
        tk.Text.__init__(
            self, ParentFrame, font=("Seven Segment", 45), bg="black", fg="white"
        )
        self.pack(side="top")
        self._count = 0
        
        api_call,success = None, False
        while not(success): 
            api_call,success = get_train_json()
            last_update_time = datetime.datetime.now()
        print(api_call)
        trains_update = process_train_json(api_call)
        train_update_text = text_gen(trains_update)
        final_text = train_update_text +"\n\nLast Update: "+last_update_time.strftime("%m/%d/%Y, %H:%M:%S")
        
        self.insert(tk.END, final_text)
        #self.label.pack(side="top")
        self.update_text(ParentFrame, last_update_time, train_update_text)
        print("done initializing widget")

    def update_text(self, ParentFrame,last_update_time, trains_update_text):
        print("starting update")
        self.delete("1.0", "end")

        api_call,success = get_train_json()
        #print(api_call) datetime.datetime.now()
        if success:
            trains_update = process_train_json(api_call)
            train_update_text = text_gen(trains_update)
            last_update_time = datetime.datetime.now()        
            last_update_txt =  "\n\nLast Update: "+last_update_time.strftime("%m/%d/%Y, %H:%M:%S")
            print(trains_update_text)
            final_text =train_update_text +last_update_txt
        else:
            last_update_txt = "\n\nLast Update: "+last_update_time.strftime("%m/%d/%Y, %H:%M:%S")
            final_text =trains_update_text + "\n\nLast Update: "+last_update_time.strftime("%m/%d/%Y, %H:%M:%S")   
        # if ParentFrame.stale_update:
        #     print("still stale")
        #     stale_update_message = stale_update_text()
        #     final_text = stale_update_message+last_update_txt
        
            
        self.insert(tk.END, final_text)
        self._count += 1
        print("after update")
        self.after(5000, self.update_text, ParentFrame,last_update_time, trains_update_text)

import datetime
import requests
import json
import time


def get_train_json():
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
        + "?filter[stop]=place-portr&filter[route]=Red&include=trip,vehicle"
    )

    current_time = datetime.datetime.now()
    try:
        trip_request = requests.get(api_address, timeout=5)
        trips_json = trip_request.json()
        success = True

    except requests.exceptions.RequestException as error:
        print("Ooops exception happened")
        trips_json = None
        success = False
        with open("error.txt", "w") as error_file:
            error_file.write("Time:")
            error_file.write(current_time.strftime("%m/%d/%Y, %H:%M:%S"))
            error_file.write("\n\n")
            error_file.write(error.response.text)

    with open("api_log.txt", "w") as api_log:
        api_log.write("Time:")
        api_log.write(current_time.strftime("%m/%d/%Y, %H:%M:%S"))
        api_log.write("\n\n")
        formatted_train_string = json.dumps(trip_request.text, indent=2)
        api_log.write(formatted_train_string)

    return trips_json, success


def process_train_json(train_json):
    trip_ids_prediction = []
    Vehicle_ids_prediction = []
    arrival_times_prediction = []

    trip_ids_trips = []
    direction_trips = []

    Vehicle_ids_vehicles = []
    position_vehicles = []
    #print(train_json)
    
    if "included" not in train_json.keys():
        return simplify_data([], [],[])
    
    
    datalength = len(train_json["data"])
    
    for i in range(datalength):
        #train color
        trip_ids_prediction.append(
            train_json["data"][i]["relationships"]["trip"]["data"]["id"]
        )
        #unique trip number
        Vehicle_ids_prediction.append(
            train_json["data"][i]["relationships"]["vehicle"]["data"]["id"]
        )
        
        #arrival time
        arrival_times_prediction.append(
            train_json["data"][i]["attributes"]["arrival_time"]
        )

    for included_i in train_json["included"]:
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

    dir_dict = simplify_data(arrival_times_prediction, dir_sort, position_sorted)

    return dir_dict


def simplify_data(arrivals, directions, positions):
    """
    Takes the the output of the api and takes just the 2 trips that will be soonest for each train
    """
    now = datetime.datetime.now()

    alewife = {"ETA": [], "position": []}
    ashmont = {"ETA": [], "position": []}
    braintree = {"ETA": [], "position": []}
    dir_dict = {"Alewife": alewife, "Ashmont": ashmont, "Braintree": braintree}
    if arrivals == []:
        return dir_dict
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

    return dir_dict


def text_gen(train_times):
    """
    Takes simplified train times and constructs
    the final string used for the widget
    """
    alltext = ""
    for train in ["Alewife", "Ashmont", "Braintree"]:
        if len(train_times[train]["ETA"]) > 0:
            traintext = train + ":   " + str(train_times[train]["ETA"][0])
            if len(train_times[train]["ETA"]) > 1:
                traintext += " , " + str(train_times[train]["ETA"][1])
            traintext += " minutes away"
        else:
            traintext = train + ":\tNo Train :("
        alltext = alltext + traintext + "\n\n"

    alltext = alltext[:-2]
    return alltext

def stale_update_text():
    alltext = ""
    for train in ["Alewife", "Ashmont", "Braintree"]:
        stale_train_txt = train + ":\t" + "No data :(" + "\n\n"
        alltext+=stale_train_txt
    return alltext

def main():
    app = Main()
    app.mainloop()


if __name__ == "__main__":
    main()
