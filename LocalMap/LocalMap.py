import tkinter as tk
import matplotlib
import numpy as np
import smopy

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

        fig, ax = plt.subplots(figsize=(20,10))
        ax.axis("off")
        extent = [0.006,0.02]
        davis = [42.396667, -71.121667 ]
        alewife = [42.395638, -71.141228]
        porter = [42.388409, -71.118880 ]

        m = smopy.Map((davis[0]-extent[0], davis[1]-extent[1],davis[0]+extent[0], davis[1]+extent[1]),z=15)
        m.show_mpl(ax = ax)
        
        davisxy = m.to_pixels(davis)
        ax.text(davisxy[0],davisxy[1],"Davis",fontsize=35)
        ax.scatter(davisxy[0],davisxy[1],c="k",s=50)

        alewifexy = m.to_pixels(alewife)
        ax.text(alewifexy[0],alewifexy[1],"Alewife",fontsize=35)
        ax.scatter(alewifexy[0],alewifexy[1],c="k",s=50)

        porterxy = m.to_pixels(porter)
        ax.text(porterxy[0],porterxy[1],"Porter",fontsize=35)
        ax.scatter(porterxy[0],porterxy[1],c="k",s=50)
                
        # davis = [-71.121667, 42.396667]
        # plt.scatter(davis[0],davis[1],c="k")
        # ax.text(davis[0],davis[1],"Davis")
        
        # alewife = [-71.141228,42.395638]
        # plt.scatter(alewife[0],alewife[1],c="k")
        # ax.text(alewife[0],alewife[1],"Alewife")
        
        # porter = [-71.118880, 42.388409]
        # plt.scatter(porter[0],porter[1],c="k")
        # ax.text(porter[0],porter[1],"Porter")
        
        # harvard = [-71.118713, 42.373322]
        # plt.scatter(harvard[0],harvard[1],c="k")
        # ax.text(harvard[0],harvard[1],"Harvard")
        
        canvas = FigureCanvasTkAgg(fig, self)
        directions, coordy, coordx = self.get_train_pos(ParentFrame)
        print(directions, coordx, coordy)
        self.plotme(canvas, ax, coordx, coordy,m)
        self.update_plot(canvas, ax, coordx, coordy,m,ParentFrame)
        plt.close()


    def plotme(self, canvas, ax, xs, ys,m):
        #ax.clear()
        xlim,ylim = ax.get_xlim(),ax.get_ylim()
        coordx, coordy = m.to_pixels(ys,xs)
        ax.set_ylim(ylim)
        ax.set_xlim(xlim)
        ax.scatter(coordx, coordy,c="r",s=75)

        canvas.draw()
        canvas.get_tk_widget().pack(padx=10, pady=10, anchor="w")


    def update_plot(self, canvas, ax, xs, ys,m,ParentFrame):
        directions, coordy, coordx = self.get_train_pos(ParentFrame)
        self.plotme(canvas, ax,coordx, coordy,m)
        #print("plot device: ", ys)
        self.after(5000, self.update_plot, canvas, ax, xs, ys,m,ParentFrame)

    def get_train_pos(self,ParentFrame):
        train_data = ParentFrame.local_trains
        
        directions = train_data.keys()
        coordinates = []
        num_trains = 0
        for direction_i in directions:
            coord_i = train_data[direction_i]["position"]
            print(type(train_data[direction_i]["position"]),train_data[direction_i]["position"])
            num_trains+=len(train_data[direction_i]["position"])
            coordinates.append(coord_i)
            
        print(np.array(coordinates))
        coordinates = np.array(coordinates,dtype=object).reshape(num_trains,2)
        coordx, coordy = coordinates[:,0],coordinates[:,1]
        print(coordinates,"\n")
        
        return directions, coordx, coordy
