import tkinter as tk
from DataFrame.Train_data import text_gen
import datetime

class TextWidget(tk.Text):
    def __init__(self, ParentFrame):
        tk.Text.__init__(
            self, ParentFrame, font=("Seven Segment", 45), bg="black", fg="white"
        )
        self.pack(side="top")
        self._count = 0
        # The label acts as a title for each main frame.
        #self.label = tk.Label(self, text="App_Name: Frame1", font=("Arial", 20))
        train_data = ParentFrame.local_trains
        train_text = text_gen(train_data)
        today = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        train_text += "\n\nLast Update: "+today
        self.insert(tk.END, train_text)
        #self.label.pack(side="top")
        self.update_text(ParentFrame)

    def update_text(self, ParentFrame):
        self.delete("1.0", "end")
        train_data = ParentFrame.local_trains
        train_text = text_gen(train_data)
        today = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        train_text += "\n\nLast Update: "+today
        self.insert(tk.END, train_text)
        self._count += 1
        self.after(10000, self.update_text, ParentFrame)
