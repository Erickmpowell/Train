import tkinter as tk
from Train_data import train_loop



class TextWidget(tk.Text):
    def __init__(self, ParentFrame):
        tk.Text.__init__(self, ParentFrame,font=("Helvetica", 45),bg="black",fg="white")

        self._count=0
        #The label acts as a title for each main frame.
        self.label = tk.Label(self, 
                              text='App_Name: Frame1',
                              font=('Arial', 20))
        train_text = train_loop()
        self.insert(tk.END,train_text)
        self.label.pack(side="bottom")
        self.update()

    def update(self):
        self.delete("1.0","end")
        train_text = train_loop()
        self.insert(tk.END,train_text)
        self._count +=1
        self.after(10000,self.update)

