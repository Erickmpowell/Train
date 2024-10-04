import tkinter as tk
from DataFrame.Train_data import text_gen,stale_update_text
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
        lastupdate = ParentFrame.last_update
        train_text += "\n\nLast Update: "+lastupdate.strftime("%m/%d/%Y, %H:%M:%S")
        self.insert(tk.END, train_text)
        #self.label.pack(side="top")
        self.update_text(ParentFrame)

    def update_text(self, ParentFrame):
        
        self.delete("1.0", "end")
        
        lastupdate = ParentFrame.last_update
        last_update_txt = "\n\nLast Update: "+lastupdate.strftime("%m/%d/%Y, %H:%M:%S")
        if ParentFrame.stale_update:
            stale_update_message = stale_update_text()
            final_text = stale_update_message+last_update_txt
        else:
            
            train_data = ParentFrame.local_trains
            train_text = text_gen(train_data)
            final_text =train_text +last_update_txt 
        self.insert(tk.END, final_text)
        self._count += 1
        self.after(5000, self.update_text, ParentFrame)

        
