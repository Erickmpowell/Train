import tkinter as tk
from Train_data import text_gen_plus_position


class TextWidget(tk.Text):
    def __init__(self, ParentFrame):
        tk.Text.__init__(
            self, ParentFrame, font=("Seven Segment", 45), bg="black", fg="white"
        )
        self.pack(side="top")
        self._count = 0
        # The label acts as a title for each main frame.
        self.label = tk.Label(self, text="App_Name: Frame1", font=("Arial", 20))
        train_data = ParentFrame.local_trains
        train_text = text_gen_plus_position(train_data)
        self.insert(tk.END, train_text)
        self.label.pack(side="top")
        self.update_text(ParentFrame)

    def update_text(self, ParentFrame):
        self.delete("1.0", "end")
        train_data = ParentFrame.local_trains
        train_text = text_gen_plus_position(train_data)
        self.insert(tk.END, train_text)
        self._count += 1
        self.after(5000, self.update_text, ParentFrame)
