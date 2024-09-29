import tkinter as tk
from DataFrame.Train_data import process_train_json,get_train_json
import datetime




class DataFrame(tk.Frame):
    def __init__(self, ParentFrame):
        tk.Frame.__init__(self, ParentFrame)

        # The label acts as a title for each main frame.
        self.label = tk.Label(self, text="App_Name: Frame2", font=("Arial", 20))

        self.label.pack(side="bottom")
        
        self.update_json = get_train_json
        self.process_json = process_train_json

        self.update_data(ParentFrame)
        #self.update_data(ParentFrame)

    # def update_local(self):
    #     return 1

    def update_global(self):
        return 2


    def update_data(self,ParentFrame):
        trains_json, success = self.update_json()
        
        current_time = datetime.datetime.now()
        
        if success:
            ParentFrame.trains_json = trains_json
            ParentFrame.last_update = current_time
            ParentFrame.local_trains = self.process_json(trains_json)
        
        else:
            
            if (ParentFrame - current_time) < datetime.timedelta(minutes=1):
                ParentFrame.local_trains = self.process_json(trains_json)

        self.after(5000, self.update_data,ParentFrame)

    '''
    def update_data(self, ParentFrame):
        ParentFrame.local_trains = self.update_local()
        ParentFrame.global_trains += self.update_global()
        self.after(5000, self.update_data, ParentFrame)
    '''