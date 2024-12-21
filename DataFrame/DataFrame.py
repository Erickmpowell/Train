"""Module to control all the data that gets transfered between frames"""

import datetime
import tkinter as tk
from DataFrame.Train_data import process_train_json, get_train_json


class DataFrame(tk.Frame):
    """The class that updates the train data and then updates the parent frame"""

    def __init__(self, ParentFrame):
        tk.Frame.__init__(self, ParentFrame)

        # The label acts as a title for each main frame.
        self.label = tk.Label(self, text="App_Name: Frame2", font=("Arial", 20))

        self.label.pack(side="bottom")

        self.update_json = get_train_json
        self.process_json = process_train_json

        self.update_data(ParentFrame)
        # self.update_data(ParentFrame)

    # def update_local(self):
    #     return 1

    def update_global(self):
        return 2

    def update_data(self, ParentFrame):
        ParentFrame.iters+=1
        print("Iterations: ",ParentFrame.iters)
        trains_json, success = self.update_json()

        
        if "included" not in trains_json.keys():
            success= False 
            ParentFrame.stale_update = True
            
        current_time = datetime.datetime.now()

        if success:
            ParentFrame.trains_json = trains_json
            ParentFrame.last_update = current_time
            ParentFrame.stale_update = False
            ParentFrame.local_trains = self.process_json(trains_json)
        '''
        else:
            if (current_time - ParentFrame.last_update) < datetime.timedelta(seconds=10):
                ParentFrame.local_trains = self.process_json(trains_json)
            else:
                ParentFrame.stale_update = True
        '''

        self.after(5000, self.update_data, ParentFrame)
