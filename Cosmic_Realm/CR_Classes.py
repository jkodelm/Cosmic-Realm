"""CR_Classes by jKLm.

This file contains the following classes: Ufo and Space.
They work with Cosmic_Realm by jKLm.

See more info using help(Ufo) or help(Space)."""

#━━━━━━━━━━#   IMPORTS   #━━━━━━━━━━#

#import tkinter as tk
from PIL import Image, ImageTk
from random import choice, randint
from datetime import datetime

from CR_Variables import DARK_GRAY, BACKG_BLUE, wscreen, hscreen, ufo_skins, id_entities, speed_values, add_ufo_time, max_rotation_ufo, max_ufo_number

#━━━━━━━━━━#   CLASSES   #━━━━━━━━━━#

class Ufo:
    """Creates an animated UFO image with customizable attributes on a given canvas.

    Attributes:
    - space (Space class): The space where the UFO exists are are stored.
    - canvas (tkinter canvas): The canvas where the UFO is drawn.
    - named (str): Name of the UFO. If not provided, a random name is generated.
    - typed (str): Type of the UFO. If not provided, a random type is selected from the ufo_skins dictionary.
    - ext (bool): If True, the UFO spawns outside the visible frame. Otherwise, it spawns inside.
    - set_x (int): x-axis position on the visible frame where the UFO will spawn. Randomly generated if not given.
    - set_y (int): y-axis position on the visible frame where the UFO will spawn. Randomly generated if not given.
    - speed (int): Speed of the UFO's movement. Randomly generated if not given.
    - direction (str): Starting direction of the UFO ('l', 'r', 'u', or 'd'). Randomly generated if not given.

    Getters:
    - get_name() -> str: Returns the name of the UFO.
    - get_id() -> int: Returns the id of the UFO.
    - get_info() -> dict: Returns a dictionary with characteristics of the UFO.
    - get_coords() -> Returns the current coordinates of the UFO. -> tuple

    Methods:
    - set_starting_coords(set_xx, set_yy, ext_val): Sets the UFO's starting coordinates.
    - set_size_image(): Resizes the UFO image to a width of 160 pixels, maintaining the aspect ratio.
    - hover_cursor_type(cursor_type): Changes the mouse state by cursor_type when the mouse hovers over the UFO.
    - clicked(): Sets the info of the UFO in a dictionary once clicked.
    - add_evade_win() -> Adds a evade win to the UFO.
    - add_battle_win() -> Adds a battle win to the UFO.
    - move_image(): Moves the UFO on the canvas according to its speed.
    - destroy_element(): Destroys the UFO image and makes it disappear forever."""
    
    def __init__(self, space, canvas, named=None, typed=None, ext=False, set_x=None, set_y=None, speedd=None, directionn=None, rotationn=None):
        """Init function for Space class.

        Instances:
        - self.space (Space class): The space where the UFO exists are are stored.
        - self.canvas (tkinter canvas): The canvas where the UFO is drawn.
        - self.type (str): Type of the UFO from ufo_skins' keys or 'typed' if mentionned.
        - self.__name__ (str): Name of the UFO randomly generated or 'named' if mentionned.
        - self.__id__ (int): Id of the UFO with a step of 1 each new one.
        - self.born (str): Time when UFO gets created, datetime used.
        - self.speed (float): Speed of the UFO randomly selected from speed_values or 'speedd' if mentionned.
        - self.direction (str): Direction of the UFO, randomly chosen between 'l', 'r', 'u' or 'd', or "directionn' if mentionned.
        - self.image (PhotoImage): Image of the image link depending of the UFO type.
        - self.x, self.y (ints): x and y coordinates of the UFO, starting coords when created and corrds updated when called.
        - self.image_id: The image itself, with binds assigned to it.
        - self.evade_wins : Times the UFO has won the evade minigame.
        - self.battle_wins Times the UFO has won the battle minigame."""
        global id_entities #Variable storing the IDs already used and to create new UFOs.
        
        self.space = space
        self.canvas = canvas

        self.type = typed or choice(list(ufo_skins.keys()))
        self.__name__ = named or f"{self.type[0]}-{randint(1, 100000)}"
        self.__id__ = id_entities
        id_entities += 1
        self.born = str(datetime.now().time())[:8]
        self.speed = float(speedd) if speedd is not None else choice(speed_values)
        self.direction = directionn or choice(['l','r','u','d'])
            
        self.set_starting_coords(set_x, set_y, ext)
        
        self.opened_image = Image.open(ufo_skins[self.type]["Path"])
        self.define_rotation(rotationn)
        self.image = ImageTk.PhotoImage(self.opened_image.rotate(self.rotation))

        if self.image.width() != 160:
            self.set_size_image()
            self.rotation = 0
        
        self.image_id = self.canvas.create_image(self.x, self.y, anchor="nw", image=self.image)

        canvas.tag_bind(self.image_id, '<Button-1>', self.clicked)
        canvas.tag_bind(self.image_id, '<Enter>', lambda event: self.hover_cursor_type(event, "hand2"))
        canvas.tag_bind(self.image_id, '<Leave>', lambda event: self.hover_cursor_type(event, "arrow"))

        self.space.ufos[str(self.__id__)] = self
        self.space.clicked_ufos[self.__id__] = 'No'
        
        self.evade_wins = 0
        self.battle_wins = 0

    def set_starting_coords(self, set_xx, set_yy, ext_val):
        """Sets the UFO's starting coordinates, used in __init__().
            -> set_xx(int): x axis value or None depending on if set_x is given.
            -> set_yy(int): y axis value or None depending on if set_y is given.
            -> ext_val(bool): ext value passed as parameter."""
        global wscreen, hscreen

        self.x, self.y = randint(0, wscreen - 160), randint(10, hscreen - 200)

        if set_xx is not None:
            self.x, self.y = set_xx, self.y
        elif set_yy is not None:
            self.x, self.y = self.x, set_yy
        
        if ext_val:
            img_height_coords = ufo_skins[self.type]["Height"]
            if self.direction == 'l':
                self.x, self.y = wscreen, randint(0, hscreen-img_height_coords-100)
            elif self.direction == 'r':
                self.x, self.y = -160, randint(0, hscreen-img_height_coords-100)
            elif self.direction == 'u':
                self.x, self.y = randint(0, wscreen-160), hscreen-100
            else:
                self.x, self.y = randint(0, wscreen-160), -img_height_coords

    def set_size_image(self):
        """Resizes the UFO image to a width of 160 pixels, maintaining the aspect ratio."""
        
        resizing_ufo = Image.open(ufo_skins[self.type]["Path"])
        new_h_resizing_ufo = int((160 / resizing_ufo.width) * resizing_ufo.height)
        resizing_ufo = resizing_ufo.resize((160, new_h_resizing_ufo))
        ufo_skins[self.type]["Height"] = new_h_resizing_ufo  # +10
        self.image = ImageTk.PhotoImage(resizing_ufo.rotate(0))
        
    def define_rotation(self, rotationnn):
        """Gives a rotation value to the UFO according to its starting direction. Parameter:
        - rotationnn (int or None): if int, gets the rotation to this value, else rotation value to randomly generated."""
        
        if self.direction == 'u' or self.direction == 'd':
            self.rotation = 0
        else:
            self.rotation = rotationnn or randint(0,max_rotation_ufo)
            self.rotation = int(self.rotation)
            if self.direction == 'l':
                self.rotation = -self.rotation
        
    def get_name(self):
        """Returns the name of the UFO. -> str"""
        return self.__name__
    
    def get_id(self):
        """Returns the id of the UFO. -> int"""
        return self.__id__
    
    def direction_line(self):
        if self.direction in ['l', 'r']:
            return 'horizontal'
        return 'vertical'
    
    def get_coords(self):
        """Returns the current coordinates of the UFO. -> tuple"""
        return self.canvas.coords(self.image_id)
    
    def get_info(self):
        """Returns a dictionary with characteristics of the UFO. -> dict"""
        return {"Name": self.get_name(), "ID": self.get_id(), "Speed": self.speed, "Direction": "Left and right" if self.direction == 'l' or self.direction == 'r' else "Up and down", "Rotation": abs(self.rotation), "Skin name": self.type, "Image path": ufo_skins[self.type]["Path"], "Alive since": self.born, "Evade game wins": self.evade_wins, "Battle game wins": self.battle_wins}
        
    def hover_cursor_type(self, event, cursor_type):
        """Changes the mouse state by cursor_type when the mouse hovers over the UFO. Parameter:
        - cursor_type (str): state for tkinter mouse."""
        self.canvas.config(cursor=cursor_type)
        
    def clicked(self, event):
        """Sets the info of the UFO in a dictionary once clicked."""
        self.space.clicked_ufos[self.__id__] = self.get_info()
        
    def add_evade_win(self):
        """Adds a evade win to the UFO."""
        self.evade_wins += 1
        
    def add_battle_win(self):
        """Adds a battle win to the UFO."""
        self.battle_wins += 1

    def move_image(self):
        """Moves the UFO on the canvas according to its speed and direction. It changes direction once it hits a screen border and updates the rotation."""
        
        dire = self.direction
        x, y = self.canvas.coords(self.image_id)
        heiufo = ufo_skins[self.type]["Height"]
        
        if dire == 'l': 
            self.canvas.move(self.image_id, -self.speed, 0)
            if x < 0:  # If the UFO touches the left border
                self.direction = 'r'
                self.rotate_image()

        elif dire == 'r':
            self.canvas.move(self.image_id, self.speed, 0)
            if x > wscreen - 160:  # If the UFO touches the right border
                self.direction = 'l'
                self.rotate_image()

        elif dire == 'u':
            self.canvas.move(self.image_id, 0, -self.speed)
            if y < 0:
                self.direction = 'd'

        else:
            self.canvas.move(self.image_id, 0, self.speed)
            if y > hscreen - heiufo - 100:  # If the UFO touches the bottom border
                self.direction = 'u'
                
    def rotate_image(self):
        """Rotates the given image to its opposite value."""
        
        if self.rotation > 0:
            self.rotation = -self.rotation
        else:
            self.rotation = abs(self.rotation)
        
        if self.rotation != 0:
            self.update_image()

    def update_image(self):
        """Updates the image on the board with the correct rotation."""

        self.image = ImageTk.PhotoImage(self.opened_image.rotate(self.rotation))
        self.canvas.itemconfig(self.image_id, image=self.image)
        
    def destroy_element(self):
        """Destroys the UFO image and makes it disappear forever on the canvas."""
        
        del self.space.ufos[str(self.__id__)]
        self.canvas.delete(self.image_id)
        self.image = None

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━#

class Space:
    """Creates an environment to manage UFOs (instances of the UFO class) within a Tkinter window.

    Attributes:
    - root (tkinter window or frame): The main tkinter window or frame where the UFOs will fly.
    - canvas (tkinter canvas): The canvas where the UFOs are drawn.
    
    Getters:
    None

    Methods:
    - move_all_ufos(): Moves all UFOs in the class using a loop and a timer.
    - add_ufo(exterior): Adds a UFO to the grid. The UFO comes from the borders if exterior is True, else it spawns directly in.
    - check_ufo_number(): Checks if the number of UFOs on the grid is higher than 6, and adds more if it is not the case.
    - delete_random_ufo(): Deletes a random UFO using it's id in the dictionnary self.ufos.
    - add_ufo_timer(): Adds a UFO every time given by add_ufo_time.
    - resolution_values(event): Updates the global screen width and height based on the root window's current size.
    - change_bg(image_path, button_number, bgprevs): Changes the background of the canvas with a chosen image."""
   
    def __init__(self, roott, canvasss):
        """Init function for Space class.

        Instances:
        - self.root (tkinter window or frame): The main tkinter window or frame where the UFOs will fly.
        - self.canvas (tkinter canvas): The canvas where the UFOs are drawn.
        - self.ufos (dict): Contains all ufos displayd on the self.canvas. UFO'S id as key and UFO class as value.
        - self.clicked_ufos (dict): Contains all UFOs ids with their current cliked state or not. UFO'S id as key and 'No' or info on the UFO as value if clicked.
        - self.last_image_url (int): Button number clicked used for self.change_bg, default is 1."""
        
        self.root, self.canvas = roott, canvasss
        self.ufos, self.clicked_ufos = {}, {}
        self.last_image_url = 1

    def move_all_ufos(self):
        """Moves all UFOs in the class using a loop and a timer."""
        
        for ufo in self.ufos.values():
            ufo.move_image()
        self.canvas.after(15, self.move_all_ufos)

    def add_ufo(self, exterior):
        """Adds a UFO to the grid. The UFO comes from the borders if the parameter exterio is True, else it spawns directly in."""
        
        if len(self.ufos) < max_ufo_number:
            Ufo(self, self.canvas, ext=exterior)

    def check_ufo_number(self, ufo_min):
        """Checks if the number of UFOs on the grid is higher than 'ufo_min' (int), and adds more if it is not the case."""
        
        if len(self.ufos) <= ufo_min:
            self.add_ufo(True)
        self.canvas.after(15000, self.check_ufo_number(ufo_min))
        
    def delete_random_ufo(self):
        """Deletes a random UFO using it's id in the dictionnary self.ufos."""
        
        if len(self.ufos) > 0:
            self.ufos[choice(list(self.ufos.keys()))].destroy_element()

    def add_ufo_timer(self):
        """Adds a UFO every time given by add_ufo_time."""
        
        self.add_ufo(True)
        self.canvas.after(add_ufo_time, self.add_ufo_timer)

    def resolution_values(self, event):
        """Updates the global screen width and height based on the root window's current size."""
        global wscreen, hscreen
        wscreen, hscreen = self.root.winfo_width(), self.root.winfo_height()

    def change_bg(self, image_path, button_number, bgprevs):
        """Changes the background of the canvas with a chosen image. Parameters:
        -> image_path (str): Path of the background image selected.
        -> button_number (int): Column of the clicked button, used to highlight its border.
        -> bgprevs (list): All buttons accessible to choose the background."""
        
        if image_path != self.last_image_url:
            itbg = Image.open(image_path).resize((1920, 1080))
            itbg2 = ImageTk.PhotoImage(itbg)
            
            self.canvas.create_image(0, 0, anchor="nw", image=itbg2, tags="background")
            self.canvas.image = itbg2
            self.canvas.tag_lower("background")
            self.last_image_url = image_path
            
            for configbg in range(len(bgprevs)):
                bgprevs[configbg].configure(border_color=BACKG_BLUE if configbg + 1 == button_number else DARK_GRAY, border_width=3 if configbg + 1 == button_number else 0)