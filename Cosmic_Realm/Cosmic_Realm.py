#━━━━━━━━━━#   IMPORTS   #━━━━━━━━━━#

from CR_Interface import import_interface, root, canvas, bottom_bar_setup, detect_clicked_ufo
from CR_Classes import Space
from CR_Variables import starting_ufos
  
#━━━━━━━━━━#   INTERFACE   #━━━━━━━━━━#

space = Space(root, canvas)
import_interface(space)
root.bind("<Configure>", space.resolution_values)

bg_previews = bottom_bar_setup()
space.change_bg("bgs/bg1.png", 1, bg_previews)

for startufo in range(starting_ufos):
    space.add_ufo(False)

space.move_all_ufos() #Disable to make UFOs stand.
#space.add_ufo_timer() #Disable not to have UFOs being spawned every add_ufo_time seconds.
#space.check_ufo_number(3) #Disable not to have UFOs being added under a certain level.
detect_clicked_ufo() #Necessary to open info on UFO.

root.mainloop()