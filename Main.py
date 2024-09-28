import tkinter as tk

# importing frames that we will create soon!
from TextWidget.TextWidget import TextWidget
from Frame2 import Frame2
from LocalMap.LocalMap import Frame3
from DataFrame.DataFrame import DataFrame
from DataFrame.Train_data import train_loop
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
        container.__setattr__("local_trains", train_loop())
        container.__setattr__("global_trains", 0)
        container.__setattr__("trains_json",0)
        container.__setattr__("last_update",datetime.datetime.now())
            
        print(type(container))
        # Pack the container to the root
        container.pack(side="top", fill="both", expand=True)

        # Fixes pack location of the container using grid
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Create empty dictionary of frames
        self.frames = {}

        # Use container as master frame for imported frames
        t0 = time.time()
        for Frame in (TextWidget, Frame2, Frame3, DataFrame):
            t1 = time.time()
            print("working on:\t", Frame)
            self.frames[Frame] = Frame(container)
            self.frames[Frame].grid(row=0, column=0, sticky="nsew")
            print("Time elapsed:",t1-t0)
            t0=t1
            
        # Define buttons to switch GUI pages
        self.frame1_btn = tk.Button(
            self, text="Frame1", font=("Arial", 10), command=self.show_textwidget
        )
        self.frame1_btn.place(relx=0, rely=1, relwidth=1 / 3, anchor="sw")

        self.frame2_btn = tk.Button(
            self, text="Frame2", font=("Arial", 10), command=self.show_frame2
        )
        self.frame2_btn.place(relx=1 / 3, rely=1, relwidth=1 / 3, anchor="sw")

        self.frame3_btn = tk.Button(
            self, text="Frame3", width=10, font=("Arial", 10), command=self.show_frame3
        )
        self.frame3_btn.place(relx=2 / 3, rely=1, relwidth=1 / 3, anchor="sw")

        # The start page is raised to the top at the beginning.
        self.show_textwidget()

    # Raises the selected frame to the top.
    def show_textwidget(self):
        frame = self.frames[TextWidget]
        frame.tkraise()

    def show_frame2(self):
        frame = self.frames[Frame2]
        frame.tkraise()

    def show_frame3(self):
        frame = self.frames[Frame3]
        frame.tkraise()


def main():
    app = Main()
    app.mainloop()


if __name__ == "__main__":
    main()
