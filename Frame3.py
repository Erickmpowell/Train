import tkinter as tk
import matplotlib
import numpy as np

matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class Frame3(tk.Frame):
    def __init__(self, ParentFrame):
        """tk.Frame.__init__(self, ParentFrame)

        #The label acts as a title for each main frame.
        self.label = tk.Label(self,
                              text='App_Name: Frame3',
                              font=('Arial', 20))

        self.label.pack(side="bottom")
        xs,ys = np.array([1,2,3,4]),np.array([2,3,3,4])
        self.plotme(xs,ys)
        #self.update_plot(xs,ys+1)

        """

        tk.Frame.__init__(self, ParentFrame)

        # The label acts as a title for each main frame.
        self.label = tk.Label(self, text="App_Name: Frame3", font=("Arial", 20))

        self.label.pack(side="bottom")
        xs, ys = np.array([1, 2, 3, 4]), np.array([2, 3, 3, 4])

        fig, ax = plt.subplots()

        canvas = FigureCanvasTkAgg(fig, self)
        self.plotme2(canvas, ax, xs, ys)
        self.update_plot(canvas, ax, xs, ys)
        plt.close()

    def close_plot(self):
        plt.close()

    def plotme2(self, canvas, ax, xs, ys):
        ax.clear()
        ax.plot(xs, ys)

        canvas.draw()
        canvas.get_tk_widget().pack(padx=10, pady=10, anchor="w")
        # canvas._tkcanvas.pack(padx=10, pady=10, anchor='w')

        # plt.close()
        # fig.close()

    def update_plot(self, canvas, ax, xs, ys):
        ys = ys + 1
        self.plotme2(canvas, ax, xs, ys)
        print("plot device: ", ys)
        self.after(2000, self.update_plot, canvas, ax, xs, ys)

    def plotme(self, xs, ys):
        fig = plt.figure(1)
        fig.add_subplot(111).plot(xs, ys)
        # plt.plot([1,2,3,4],[2,3,4,3])
        canvas = FigureCanvasTkAgg(fig, self)
        canvas.draw()
        canvas.get_tk_widget().pack(padx=10, pady=10, anchor="w")
        # canvas._tkcanvas.pack(padx=10, pady=10, anchor='w')

        plt.close()
        # fig.close()
