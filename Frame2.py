import tkinter as tk


class Frame2(tk.Frame):
    def __init__(self, ParentFrame):
        tk.Frame.__init__(self, ParentFrame)

        # The label acts as a title for each main frame.
        self.label = tk.Label(self, text="App_Name: Frame2", font=("Arial", 20))

        self.label.pack(side="bottom")
