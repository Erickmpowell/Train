import requests
import datetime
import tkinter as tk
import time

key = "282c97aea67046e4a847e745fde9d329"


def get_trains():

    trips = requests.get("https://api-v3.mbta.com/predictions?filter[stop]=place-davis&filter[route]=Red&include=trip").json()


    tripIDs_prediction = []
    arrivalTimes_prediction = []
    tripIDs_included = []
    direction_included = []

    datalength = len(trips["data"])
    for i in range(datalength):
        tripIDs_prediction.append(trips["data"][i]["relationships"]["trip"]["data"]["id"])
        arrivalTimes_prediction.append(trips["data"][i]["attributes"]["arrival_time"])


        tripIDs_included.append(trips["included"][i]["id"])
        direction_included.append(trips["included"][i]["attributes"]["headsign"])

    matched = []
    for tripi in tripIDs_prediction:
        matched.append(tripIDs_included.index(tripi))

    dir_sort = [direction_included[i] for i in matched]

    return arrivalTimes_prediction, dir_sort


def simplify_data(arrivals, directions):
    now = datetime.datetime.now()

    alewife = []
    ashmont = []
    braintree = []
    dir_dict = {"Alewife":alewife,"Ashmont":ashmont,"Braintree":braintree}
    
    for i,arri in enumerate(arrivals):
        if len(alewife)==2 & len(braintree)==2 & len(ashmont)==2:
            break

        train = directions[i]

        if len(dir_dict[train])<2:

            arrival_date,arrival_time = arri.split("T")
            arrival_time = list(map(int,arrival_time.split("-")[0].split(":")))

            diff = (arrival_time[0] -now.hour)*60 + (arrival_time[1]-now.minute)  + (arrival_time[2]-now.second)*1/60#+ int((arrival_time[2]-now.second)>0)
            if diff<1:
                diff = 0
            else:
                diff = int(diff)
            dir_dict[train].append(diff)

            print( directions[i]," is ",diff, " minutes away")#,arrivalTimes_prediction[i] )
    return dir_dict


def text_gen(data):
    alltext = ""
    for train in ["Alewife","Ashmont","Braintree"]:
        traintext = train + ":   " + str(data[train][0])+ " , " + str(data[train][1]) + " minutes away"
        alltext = alltext + traintext + "\n\n"

    alltext = alltext[:-2]
    return alltext
#print(alewife,ashmont,braintree)

arr, direction = get_trains()

data = simplify_data(arr,direction)

print(data)



def loop():
    arr, direction = get_trains()

    data = simplify_data(arr,direction)

    texts = text_gen(data)

    return texts




root = tk.Tk()
root.title("MBTA prediction")
root.minsize(625,225)
root.geometry("1000x600+50+50")
text = tk.Text(root,font=("Helvetica", 45),bg="black",fg="white")
text.pack()

while(True):

    text.delete("1.0", "end")
    new_text = loop()
    text.insert(tk.END,new_text)
    text.update()
    time.sleep(5)