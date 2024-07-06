import tkinter as tk
#importing frames that we will create soon!
from TextWidget.TextWidget import TextWidget
from Frame2 import Frame2
from Frame3 import Frame3
import time

class Main(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self) 

        #Sets the screen size of the GUI
        self.width= 1200
        self.height= 800
        self.geometry(str(self.width) + 'x' + str(self.height) + '+0+0')

        self.title('project_title')

        #The container is a frame that contains the projects's frames
        container = tk.Frame(self, 
                                height=self.height, 
                                width=self.width)

        #Pack the container to the root
        container.pack(side="top", fill="both", expand=True)

        #Fixes pack location of the container using grid
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        #Create empty dictionary of frames
        self.frames = {}

        #Use container as master frame for imported frames 
        for Frame in (TextWidget, Frame2, Frame3):
            self.frames[Frame] = Frame(container)
            print("working on:\t",Frame)
            self.frames[Frame].grid(row=0, column=0, sticky="nsew")  
        #Define buttons to switch GUI pages
        self.frame1_btn = tk.Button(self, 
                                        text='Frame1', 
                                        width=10, 
                                        font=('Arial', 10),
                                        command=self.show_textwidget)
        self.frame1_btn.place(relx=0.75, 
                                rely=0.1, 
                                anchor='center')

        self.frame2_btn = tk.Button(self, 
                                    text='Frame2', 
                                    width=10, 
                                    font=('Arial', 10),
                                    command=self.show_frame2)
        self.frame2_btn.place(relx=0.85, 
                                rely=0.2, 
                                anchor='center')

        self.frame3_btn = tk.Button(self, 
                                    text='Frame3', 
                                    width=10, 
                                    font=('Arial', 10),
                                    command=self.show_frame3)
        self.frame3_btn.place(relx=0.95, 
                                rely=0.3, 
                                anchor='center')

        #The start page is raised to the top at the beginning.
        self.show_textwidget()

    #Raises the selected frame to the top.
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

if __name__ == '__main__':
    main()