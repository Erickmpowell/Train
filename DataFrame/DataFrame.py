import tkinter as tk
print("yopo")
from DataFrame.Train_data import train_loop




class DataFrame(tk.Frame):
    def __init__(self, ParentFrame):
        tk.Frame.__init__(self, ParentFrame)

        # The label acts as a title for each main frame.
        self.label = tk.Label(self, text="App_Name: Frame2", font=("Arial", 20))

        self.label.pack(side="bottom")

        self.update_local = train_loop

        self.update_data(ParentFrame)

    # def update_local(self):
    #     return 1

    def update_global(self):
        return 2

    def update_data(self, ParentFrame):
        ParentFrame.local_trains = self.update_local()
        ParentFrame.global_trains += self.update_global()
        self.after(5000, self.update_data, ParentFrame)
