import smopy
import matplotlib.pyplot as plt

extent = [0.006,0.02]
davis = [42.396667, -71.121667 ]
alewife = [42.395638, -71.141228]
porter = [42.388409, -71.118880 ]
harvard = [42.373322, -71.118713 ]


map = smopy.Map((davis[0]-extent[0], davis[1]-extent[1],davis[0]+extent[0], davis[1]+extent[1]),z=15)
ax = map.show_mpl(figsize=(12,8))



davisxy = map.to_pixels(davis)
ax.text(davisxy[0],davisxy[1],"Davis",fontsize=35)
ax.scatter(davisxy[0],davisxy[1],c="k",s=50)

alewifexy = map.to_pixels(alewife)
ax.text(alewifexy[0],alewifexy[1],"Alewife",fontsize=35)
ax.scatter(alewifexy[0],alewifexy[1],c="k",s=50)

porterxy = map.to_pixels(porter)
ax.text(porterxy[0],porterxy[1],"Porter",fontsize=35)
ax.scatter(porterxy[0],porterxy[1],c="k",s=50)



plt.show()