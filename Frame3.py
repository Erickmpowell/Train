import tkinter as tk
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg



class Frame3(tk.Frame):
    def __init__(self, ParentFrame):
        tk.Frame.__init__(self, ParentFrame)

        #The label acts as a title for each main frame.
        self.label = tk.Label(self, 
                              text='App_Name: Frame3',
                              font=('Arial', 20))

        self.label.pack(side="bottom")

        self.plotme()

    def plotme(self):
        fig = plt.figure(1)
        fig.add_subplot(111).plot([1,2,3,4],[2,3,4,3])
        #plt.plot([1,2,3,4],[2,3,4,3])   
        canvas = FigureCanvasTkAgg(fig, self)
        canvas.draw()
        canvas.get_tk_widget().pack(padx=10, pady=10, anchor='w')
        #canvas._tkcanvas.pack(padx=10, pady=10, anchor='w')

        plt.close()
        #fig.close()



    def make_plot(self, ParentFrame):
        fig = plt.figure(1)
        fig.add_subplot(111).plot([1,2,3,4],[2,3,4,3])
        #plt.plot([1,2,3,4],[2,3,4,3])   
        canvas = FigureCanvasTkAgg(fig, ParentFrame)
        
        #canvas._tkcanvas.pack(fill=tk.BOTH, expand=1)
        fig.close()