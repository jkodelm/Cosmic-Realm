"""CR_Interface by jKLm.

This file contains multiple functions used for Cosmic_Realm."""

#━━━━━━━━━━#   IMPORTS   #━━━━━━━━━━#

import tkinter as tk
from random import choice, randint
from PIL import Image, ImageTk

from customtkinter import *
from CR_Classes import Ufo
from CR_Variables import DARK_GRAY, LIGHT_GRAY, LIGHTEST_GRAY, BACKG_BLUE, FONT_COLOR, bg_preview_style, hscreen, ufo_skins, notif_popup_shown, max_ufo_speed, max_ufo_number, shown_info_popup, shown_info_id, minigame_time

#━━━━━━━━━━#   FUNCTIONS   #━━━━━━━━━━#

def import_interface(spacee):
    """Imports elements from another file. Parameter:
    -> spacee (Space class): Grid used for the UFOs."""
    global ispace
    ispace = spacee
        
def bottom_bar_setup():
    """Setups the bottom bar of the interface."""
    global popup_canvas
    
    text_backgrounds = tk.Label(bottom_bar, text="Backgrounds:", font=("Verdana",24,"bold"), bg=DARK_GRAY, fg=FONT_COLOR)
    text_backgrounds.pack(side="left", padx=5)
    
    bg_previewss = []

    for bg_index in range(1, 5):
        img_path = f"bgs/bg{bg_index}_preview.png"
        img = Image.open(img_path).resize((80, 80))

        bg_preview = CTkButton(bottom_bar, **bg_preview_style, text="", image=CTkImage(img, size=(80, 80)), command=lambda bg_index=bg_index: ispace.change_bg(f"bgs/bg{bg_index}.png", bg_index, bg_previewss))
        bg_preview.pack(side="left", padx=5)

        bg_previewss.append(bg_preview)

    separatorl = tk.Frame(bottom_bar, width=2, height=80, bg=LIGHTEST_GRAY)
    separatorl.pack(side="left",padx=5)
    
    popup_canvas = tk.Canvas(root, bg=DARK_GRAY, borderwidth=0, highlightthickness=0, relief="flat")
    popup_canvas.place(x=0, y=1920, relwidth=1, relheight=1)
    
    help_button = CTkButton(bottom_bar, **bg_preview_style, text="?", font=("Verdana",31), command=lambda: show_popup('Help'))
    help_button.pack(side="right",padx=5)
    
    separatorr = tk.Frame(bottom_bar, width=2, height=80, bg=LIGHTEST_GRAY)
    separatorr.pack(side="right",padx=5)
    
    minus_button = CTkButton(bottom_bar, width=80, height=80, text="‒", font=("Verdana",55), anchor="n", fg_color="#D80000", text_color="#B10000", hover_color="red", corner_radius=15, cursor="hand2", command=ispace.delete_random_ufo)
    minus_button.pack(side="right", padx=5)
    
    plus_button = CTkButton(bottom_bar, width=80, height=80, text="+", font=("Verdana",55), anchor="n", fg_color="#00EB00", text_color="#00C400", hover_color="#00FF00", corner_radius=15, cursor="hand2", command=lambda: ispace.add_ufo(True))
    plus_button.pack(side="right", padx=5)
    
    separatorr2 = tk.Frame(bottom_bar, width=2, height=80, bg=LIGHTEST_GRAY)
    separatorr2.pack(side="right",padx=5)
    
    battle_button = CTkButton(bottom_bar, width=80, height=80, text="☣", font=("Verdana",55), anchor="center", fg_color="#00EBEB", text_color="#00C4C4", hover_color="#00FFFF", corner_radius=15, cursor="hand2", command=lambda: bottom_bar_renew('Battle'))
    battle_button.pack(side="right", padx=5)
    
    evade_button = CTkButton(bottom_bar, width=80, height=80, text="⯐", font=("Verdana",55,"bold"), anchor="w", fg_color="#EB9800", text_color="#C47F00", hover_color="#FFA500", corner_radius=15, cursor="hand2", command=lambda: bottom_bar_renew('Laser'))
    evade_button.pack(side="right", padx=5)

    create_button = CTkButton(bottom_bar, width=10, height=80, text="Create", font=("Verdana",34,"bold"), anchor="center", fg_color="#1CDC8D", text_color="white", hover_color="#28E496", corner_radius=15, cursor="hand2", command=lambda: show_popup('Create'))
    create_button.pack(side="left", padx=5, expand=True, fill="x")
    
    return bg_previewss

def bottom_bar_renew(option):
    """Creates a bottom bar on top of the original one, and has the essencials of the 2 minigames. Parameter:
    -> option (str): text giving info on the selected game."""
    global shown_info_popup, play_minigame, last_mouse_position 
    
    def quit_renew_bottom_bar():
        """Quits and destroys the newly created bottom bar."""
        global shown_info_popup, play_minigame
        
        play_minigame = False
        renew_bottom_bar.destroy()
        shown_info_popup = False
        
    def get_ufo_coords():
        """Get coordinates of all UFOs on the board."""
        ufo_coords = {}
        for getting_coords in ispace.ufos.values():
            ufo_coords[getting_coords.get_id()] = getting_coords.get_coords()
        return ufo_coords

    def handle_battle_winner(game_id_alive):
        """Handle the winner of the battle minigame. Parameter:
        -> game_id_alive (tuple): The two UFOs that collided together."""
        game_id_dead = game_id_alive.pop(randint(0, 1))
        ispace.ufos[str(game_id_dead)].destroy_element()
        renew_bottom_text.config(text=f"Contestant ID {game_id_dead} has been {choice(['eliminated', 'terminated', 'exploded', 'killed', 'reduced to ashes'])} by Contestant ID {game_id_alive[0]}!")
        global countdown
        countdown = 0.0

    def handle_laser_winner(game_id_alive, minig):
        """Handle the winner of the laser minigame. Parameters:
        -> game_id_alive (tuple): The two UFOs that collided together.
        -> minig (str): text giving info on the selected game."""
        save_seconds = round(countdown)
        stop_game()
        renew_bottom_text.config(text=f"Pointer was in the axis of Contestant ID {game_id_alive[1]} after {save_seconds} second{'s' if countdown >= 2.0 else ''}! It gets one laser win!")
        give_points(minig, game_id_alive[1])

    def check_single_ufo_winner(minig):
        """Check if there is only one UFO left on the board. Parameter:
        -> minig (str): text giving info on the selected game."""
        if len(ispace.ufos) == 1 and play_minigame:
            stop_game()
            renew_bottom_text.config(text=f"Contestant ID {list(ispace.ufos)[0]} has won! It gets one battle win!")
            give_points(minig)

    def mini_game(minig):
        """Core function for the games. Parameter:
        -> minig (str): text giving info on the selected game."""
        global play_minigame, countdown, last_mouse_position, minigame_time, ispace, root

        ufo_coords = get_ufo_coords()

        if len(ispace.ufos) > 1 and play_minigame:
            game_id_alive = check_overlap(ufo_coords, minig)

            if game_id_alive is not None: #If mouse or UFO caught overlapping another
                if minig == 'Battle':
                    handle_battle_winner(game_id_alive)
                elif minig == 'Laser':
                    handle_laser_winner(game_id_alive, minig)
            else:
                countdown += 0.1

                if play_minigame:
                    if minig == 'Laser':
                        mouse_coords, wscreen, hscreen = root.winfo_pointerxy(), root.winfo_width(), root.winfo_height() #mouse_coords is not correct, no idea on how to fix it
                        if (mouse_coords[0] > wscreen or mouse_coords[1] > hscreen-100) or abs(last_mouse_position[0] - mouse_coords[0]) < 5 or abs(last_mouse_position[1] - mouse_coords[1]) < 5:
                            countdown -= 0.1
                        renew_bottom_text.config(text=f"The mouse has survived {round(countdown)} second{'s' if countdown >= 1.5 else ''} so far. If count stops, keep moving pointer or go on top left.")
                        last_mouse_position = mouse_coords
                    elif countdown >= float(minigame_time):
                        stop_game()
                        renew_bottom_text.config(text=f"{len(ispace.ufos)} UFOs have survived the battle! They each get rewarded with one battle win!")
                        give_points(minig)
                    elif minigame_time - countdown <= 5.0: #If remains 5 seconds for battle
                        renew_bottom_text.config(text=f"5 seconds left!")
                    else:
                        pass

            check_single_ufo_winner(minig)
            root.after(100, lambda: mini_game(minig))
        else:
            if play_minigame:
                renew_bottom_text.config(text=f"Game cannot start since there are not enough UFOs.")

                
    def check_overlap(dict_analyse, minig_name):
        """Checks if UFOs overlap according to calculations of their coordonates. Parameters:
        -> dict_analyse (dict): all UFOs cordonates when function mini_game was called.
        -> minig_name (str): text giving info on the selected game."""

        game_dic_keys = list(dict_analyse.keys())
        dict_analyse_vals = list(dict_analyse.values())
        if minig_name == 'Battle':
            game_dic_coords = [value_coords for value_coords in dict_analyse.values()]
            game_width, game_height = 160, 120
        if minig_name == 'Laser':
            game_dic_coords = [root.winfo_pointerxy()]
            game_width, game_height = 160, 120
        
        for i in range(len(game_dic_coords)):
            x0, y0 = game_dic_coords[i][0], game_dic_coords[i][1]
            for j in range(i+1, len(dict_analyse)):
                x1, y1 = dict_analyse_vals[j][0], dict_analyse_vals[j][1]
                if (x0 < x1 and (x0 - game_width < x1 <= x0 + game_width) and (y0 - game_height < y1 <= y0 + game_height)) or (x1 < x0 and (x1 - game_width < x0 <= x1 + game_width) and (y1 - game_height < y0 <= y1 + game_height)):
                    return [game_dic_keys[i], game_dic_keys[j]]
                
        return None

    def give_points(minimage_name, ufo_winner=None):
        """Adds points according to the won minigame to the standing UFOs. Parameters:
        -> minig (str): text giving info on the selected game.
        -> ufo_winner (None or int): id of UFO that won in the evade minigame."""
        
        if minimage_name == 'Laser':
            ispace.ufos[str(ufo_winner)].add_evade_win()
        if minimage_name == 'Battle':
            for point_ufos in ispace.ufos:
                ispace.ufos[point_ufos].add_battle_win()
                
    def before_mini_game(optionn):
        """Small setups before stating the battle game. Parameter:
        -> optionn (str): text giving info on the selected game."""
        global play_minigame, countdown
            
        play_minigame = True
        countdown = 0.0
        
        renew_bottom_text.config(text="Game started!")
        renew_start.destroy()
        renew_close_button.configure(text="End game", command=lambda: stop_game(optionn))
        
        mini_game(optionn)
        
    def stop_game(minig=None):
        """Stops game, with adequate end text."""
        global countdown, play_minigame
        
        play_minigame = False
        renew_close_button.configure(text="❌", command=quit_renew_bottom_bar)
        if minig is None:
            renew_bottom_text.config(text="Game has been stopped.")
        if minig == 'Battle':
            renew_bottom_text.config(text=f"{len(ispace.ufos)} UFOs have survived. They each get one battle point!")
            give_points(minig)
        if minig == 'Laser':
            renew_bottom_text.config(text=f"Pointer has survived {round(countdown)} seconds.")
            
        

    shown_info_popup, play_minigame = True, False
    last_mouse_position = (0,0) #Position pof mouse needed to rgister is mouse has moved since last call
    
    renew_bottom_bar = tk.Frame(bottom, height=90, bg=DARK_GRAY)
    renew_bottom_bar.place(relwidth=1, x=10, y=5)
    renew_bottom_bar.propagate(False)
    
    renew_bottom_text = tk.Label(renew_bottom_bar, font=("Verdana",18), bg=DARK_GRAY, fg=FONT_COLOR)
    renew_bottom_text.pack(side="left", padx=5)
    
    renew_close_button = CTkButton(renew_bottom_bar, **bg_preview_style, text="❌", font=("Verdana",31), command=quit_renew_bottom_bar)
    renew_close_button.pack(side="right",padx=25)
    
    renew_start = CTkButton(renew_bottom_bar, width=150, height=80, text="Start", font=("Verdana",31,"bold"), anchor="center", fg_color="#1CDC8D", text_color="white", hover_color="#28E496", corner_radius=15, cursor="hand2", command=lambda: before_mini_game(option))
    renew_start.pack(side="right")
    
    if option == 'Laser':
        renew_bottom_text.config(text="Move your mouse and avoid UFOs x and y axis. Counter stops if you stand or leave the area.")
        
    elif option == 'Battle':
        renew_bottom_text.config(text=f"If 2 UFOs collide, one of them dies. If one remain, or {minigame_time} seconds of nothing, game ends.")
    
    play_minigame = True

def show_popup(section_name, info_dict=None):
    """Shows a popup with elements inside of it. Parameters:
    -> section_name (str): Name of the section ('Create', 'Help' or 'Info') to define used elements.
    -> info_dict (dict): Characteristics of an UFO if section_name is 'Info', None otherwise."""
    
    popup_canvas.place_configure(y=hscreen)
    
    def move_popup():
        """Moves a solid color across the screen from bottom to top, using .place() and a loop."""
        
        y_popup_canvas = popup_canvas.winfo_y()

        if y_popup_canvas > 50:
            popup_canvas.place_configure(y=y_popup_canvas - (hscreen / 10))
            root.after(20, move_popup)
        else:
            popup_canvas.place_configure(y=0)
            root.after(1, popup_main_components) #Timer is here only so popup_canvas gets correctly placed before anything.

    def popup_main_components():
        """Setups main components shared by all popups types."""
        global popup_frame, notif_popup_frame, shown_info_popup
        
        shown_info_popup = True
        
        popup_frame = CTkFrame(popup_canvas, width=1080, height=608, fg_color=LIGHT_GRAY, corner_radius=15)
        popup_frame.place(anchor="center", relx=0.5, rely=0.5)
        popup_frame.propagate(False)

        popup_title = tk.Label(popup_frame, text=section_name, font=("Verdana", 44, "bold"), bg=LIGHT_GRAY, fg="white")
        popup_title.pack(side="top", pady=5)

        popup_cross = CTkButton(popup_frame, width=78, height=78, fg_color=LIGHT_GRAY, hover_color=LIGHTEST_GRAY, text="❌", font=("Verdana", 32), corner_radius=15, anchor="center", cursor="hand2", command=hide_popup)

        popup_cross.place(anchor="center", relx=0.96, rely=0.07)
        popup_cross.propagate(False)
        
        notif_popup_frame = tk.Frame(popup_canvas, bg=DARK_GRAY, height=34)
        notif_popup_frame.pack(side="bottom", padx=5, pady=5, fill="x")
        
        define_popup_componants()
        
    def define_popup_componants():
        """Defines what fucntion is used according to section_name."""
        
        if section_name == 'Create':
            setup_popup_create()   
            
        if section_name == 'Help':
            setup_popup_help()
            
        if section_name == 'Info':
            setup_popup_info(info_dict)
            
    move_popup()

def hide_popup():
    """Destroys all elements in the popup and moves a solid color across the screen from top to bottom, using .place() and a loop."""
    global shown_info_popup, shown_info_id
    
    popup_frame.destroy()
    notif_popup_frame.destroy()
    y_popup_canvas = popup_canvas.winfo_y()

    if y_popup_canvas < hscreen:
        popup_canvas.place_configure(y=y_popup_canvas + (hscreen / 10))
        root.after(20, hide_popup)
    else:
        popup_canvas.place_configure(y=1080)
        shown_info_popup, shown_info_id = False, None

def detect_clicked_ufo():
    """Searches for changes in a dictionary, if found, shows a popup with specific information."""
    global shown_info_popup, shown_info_id

    for diff_val in ispace.clicked_ufos.keys():
        if ispace.clicked_ufos[diff_val] != "No":
            if not shown_info_popup:
                shown_info_popup, shown_info_id = True, str(diff_val)
                show_popup('Info', info_dict=ispace.clicked_ufos[diff_val])
                
            ispace.clicked_ufos[diff_val] = "No"
    
    root.after(250, detect_clicked_ufo)
        
def notif_popup(message,color):
    """Setups a small notification on bottom right when popup is active. Parameters:
    -> message (str): Message displayed by the popup.
    -> color (str): color for the notification push."""
    global notif_popup_shown, current_np
    
    def set_notif_popup(messagee, colorr):
        """Shows a small notification on bottom right.
        Parameters:
        -> messagee (str): Message displayed by the popup.
        -> colorr (str): color for the notification push."""
        notif_ld = CTkFrame(notif_popup_frame, height=34, bg_color=DARK_GRAY, fg_color=colorr, corner_radius=10)
        notif_ld.place(relx=1.0, rely=1.0, anchor='se')
        
        if colorr == 'red':
            symblo = '✘'
        elif colorr == '#00FF00':
            symblo = '✔'
        else:
            symblo = ''
    
        text_notif_ld = tk.Label(notif_ld, bg=colorr, font=("Verdana", 14), text=f"{symblo}{messagee}")
        text_notif_ld.pack(padx=5, pady=3)
        
        return notif_ld
        
    def destroy_notif_popup(todest):
        """Hides the notification after 3 seconds. Parameter:
        -> todest, the notification tkinter frame."""
        
        todest.destroy()
        notif_popup_shown = False
    
    if notif_popup_shown:
        current_np.destroy()
    
    current_np = set_notif_popup(message,color)
    notif_popup_shown = True
    current_np.after(3000, lambda: destroy_notif_popup(current_np))
                        
def setup_popup_info(dic_vals):
    """Setups elements for the 'Info' popup. Parameters:
    -> dic_vals (dict): Dictionnary with all the stats and info on the clicked UFO."""
    global popup_frame, info_delete_button, info_alive_value
    
    def delete_ufo():
        """Deletes an UFO on the board, from the 'Info' popup tab."""
        global shown_info_id#, info_delete_button, info_alive_value
        
        ispace.ufos[shown_info_id].destroy_element()
        info_alive_value.config(text="Dead")
        info_delete_button.destroy()
        
        notif_popup("The UFO has been removed.", '#00FF00')
    
    info_middle_frame = tk.Frame(popup_frame, bg=LIGHT_GRAY)
    info_middle_frame.pack(padx=50, pady=15, fill='both', expand=True)
    
    info_left_hand_frame = tk.Frame(info_middle_frame, bg=LIGHT_GRAY, width=185)
    info_left_hand_frame.pack(side="left", fill='y')
    
    info_right_hand_frame = tk.Frame(info_middle_frame, bg=LIGHT_GRAY)
    info_right_hand_frame.pack(side="left", fill='both')
    
    info_skin_frame = CTkFrame(info_left_hand_frame, width=185, height=185, fg_color=LIGHTEST_GRAY, corner_radius=15)
    info_skin_frame.pack()
    info_skin_frame.propagate(False)

    info_skin_canvas = tk.Canvas(info_skin_frame, width=170, height=170, bg=LIGHTEST_GRAY, highlightthickness=0)
    info_skin_image = ImageTk.PhotoImage(Image.open(dic_vals["Image path"]))
    info_skin_canvas.create_image(85, 85, anchor="center", image=info_skin_image)
    info_skin_canvas.image = info_skin_image
    info_skin_canvas.pack(padx=5, pady=5)
    
    for info_vals in dic_vals:
        
        info_loop_frame = tk.Frame(info_right_hand_frame, bg=LIGHT_GRAY)
        info_loop_frame.pack(padx=30, anchor="w")
        
        info_loop_text = tk.Label(info_loop_frame, text=f"{info_vals}:", font=("Verdana", 22, "bold"), bg=LIGHT_GRAY, fg="white")
        info_loop_text.pack(side="left", padx=5, pady=0)
    
        info_loop = tk.Label(info_loop_frame, text=dic_vals[info_vals], font=("Verdana", 22), bg=LIGHT_GRAY, fg="white")
        info_loop.pack(side="left")
        
        if info_vals == 'Alive since':
            info_alive_value = info_loop
        
    info_delete_button = CTkButton(info_right_hand_frame, height=30, fg_color="#D80000", font=("Verdana", 32), text="Delete UFO", text_color='white', hover_color="red", corner_radius=15, cursor="hand2", command=delete_ufo)
    info_delete_button.pack(side="bottom")  
    
def setup_popup_create():
    """Setups elements for the 'Create' popup."""
    global create_selected_ufo, create_shownufos
    
    create_selected_ufo = None
    
    def button_selected(toaddborder, toremoveb=None):
        global create_selected_ufo
        
        if toaddborder.cget('border_color') == BACKG_BLUE:
            toaddborder.configure(border_color=LIGHT_GRAY)
            create_selected_ufo = None
        else:
            toaddborder.configure(border_color=BACKG_BLUE)
            create_selected_ufo = toaddborder
            
        if toaddborder != toremoveb and toremoveb is not None:
            toaddborder.configure(border_color=BACKG_BLUE)
            toremoveb.configure(border_color=LIGHT_GRAY)
            create_selected_ufo = toaddborder
    
    def create_ufo():
        """Checks if all set values fit, and creates the UFO."""
        global create_selected_ufo, create_shownufos
        
        create_name_ufo,create_skin_ufo,create_custom_x,create_custom_y,create_custom_speed,create_custom_direction,create_custom_rotation = None,None,None,None,None,None,None
        
        if len(ispace.ufos) >= max_ufo_number:
            return notif_popup(f"There cannot be more than {max_ufo_number} UFOS on screen.", 'red')
        
        cnval = create_name_entry.get()
        if cnval != "" and len(cnval) <= 20:
            create_name_ufo = cnval
        elif cnval != "" and len(cnval) > 20:
            return notif_popup("Your UFO's name must be under 20 caracters.", 'red')
        else:
            return notif_popup("You must set a custom name to create your UFO.", 'red')
            
        if create_selected_ufo is not None:
            create_skin_ufo = create_shownufos[create_selected_ufo]
        else:
            return notif_popup("You must set a custom skin for your UFO.", 'red')
        
        csxval = create_starting_x.get()
        if csxval != "":
            if csxval.isdigit() and 0 <= int(csxval) <= 1920:
                create_custom_x = csxval
            else:
                return notif_popup("The value of 'Starting x' is not between 0 and 1920.", 'red')

        csyval = create_starting_y.get()    
        if csyval != "":
            if csyval.isdigit() and 0 <= int(csyval) <= 980:
                create_custom_y = csyval
            else:
                return notif_popup("The value of 'Starting y' is not between 0 and 1080.", 'red')
            
        cssval = create_starting_speed.get()
        if cssval != "":
            if cssval.replace('.', '', 1).isdigit() and len(cssval) < 6:
                cssval_float = float(cssval)
                if 2.0 <= cssval_float <= float(max_ufo_speed):
                    create_custom_speed = cssval_float
                else:
                    return notif_popup("The value of 'Speed' is not between 2 and 8. It can be a float value.", 'red')
            else:
                return notif_popup("Invalid input. Please enter a numeric value for 'Speed' under 5 caracters.", 'red')

        csdval = create_starting_direction.get().lower() 
        if csdval != "":
            if csdval in ['l', 'r', 'u', 'd']:
                create_custom_direction = csdval
            else:
                return notif_popup("The value of 'Direction' must be either 'l', 'r', 'u' or 'd'", 'red')
            
        csrval = create_starting_rotation.get()
        if csrval != "":
            if csrval.isdigit() and 0 <= int(csrval) <= 15:
                create_custom_rotation = csrval
            else:
                return notif_popup("The value of 'Rotation' is not between 0 and 15.", 'red')
        
        Ufo(ispace, canvas, named=create_name_ufo, typed=create_skin_ufo, ext=False, set_x=create_custom_x, set_y=create_custom_y, speedd=create_custom_speed, directionn=create_custom_direction, rotationn=create_custom_rotation)  
        return notif_popup(f"The UFO '{create_name_ufo}' has been created.", '#00FF00')
            
    padded_popup_zone = tk.Frame(popup_frame, width=30, height=30, bg=LIGHT_GRAY)
    padded_popup_zone.pack(padx=0, pady=5, fill="both")
    
    create_name_text = tk.Label(padded_popup_zone, text="Name:", font=("Verdana", 28), bg=LIGHT_GRAY, fg="white", justify="center")
    create_name_text.pack(side="top")
    
    create_name_entry = CTkEntry(padded_popup_zone, width=400, height=60, font=("Verdana", 24), fg_color=DARK_GRAY, text_color="white", placeholder_text="Write here a name for your ufo", placeholder_text_color=LIGHT_GRAY, border_color=DARK_GRAY, corner_radius=15)
    create_name_entry.pack(side="top", padx=10, pady=5)
    
    create_skin_text = tk.Label(padded_popup_zone, text="Skins:", font=("Verdana", 28), bg=LIGHT_GRAY, fg="white")
    create_skin_text.pack()
    
    create_skin_frame = CTkFrame(padded_popup_zone, width=10, height=100, fg_color=LIGHT_GRAY, corner_radius=15)
    create_skin_frame.pack(padx=0, pady=5, expand=True, fill="x")
    
    create_skin_frame2 = tk.Frame(create_skin_frame, bg=LIGHT_GRAY)
    create_skin_frame2.pack()
    
    create_shownufos = {}
    for create_i in ufo_skins.keys():
        create_ufo_img = Image.open(ufo_skins[create_i]['Path'])
        create_ufo_h = int((create_ufo_img.width / create_ufo_img.height) * 70)
        create_ufo_img.resize((create_ufo_h, 70))
        
        create_last_ufo_id = CTkButton(create_skin_frame2, **bg_preview_style, border_width=3, border_color=LIGHT_GRAY, text="", image=CTkImage(create_ufo_img, size=(create_ufo_h, 70)))
        create_last_ufo_id.configure(command=lambda last_id=create_last_ufo_id: button_selected(last_id, create_selected_ufo))
        create_last_ufo_id.pack(side="left", padx=1)
        
        create_shownufos[create_last_ufo_id] = create_i
    
    create_options_text = tk.Label(padded_popup_zone, text="Options (optional):", font=("Verdana", 28), bg=LIGHT_GRAY, fg="white")
    create_options_text.pack(padx=10)
    
    create_options_frame1 = tk.Frame(padded_popup_zone, width=60, height=60, bg=LIGHT_GRAY)
    create_options_frame1.pack(padx=30, pady=5)
    
    create_options_frame2 = tk.Frame(padded_popup_zone, width=400, height=60, bg=LIGHT_GRAY)
    create_options_frame2.pack(padx=30)
    
    create_starting_x_text = tk.Label(create_options_frame1, text="Starting x:", font=("Verdana", 18), bg=LIGHT_GRAY, fg="white")
    create_starting_x_text.pack(side="left", padx=5, pady=5)
    
    create_starting_x = CTkEntry(create_options_frame1, width=145, height=50, font=("Verdana", 24), fg_color=DARK_GRAY, text_color="white", placeholder_text="0 to 1920", placeholder_text_color=LIGHT_GRAY, border_color=DARK_GRAY, corner_radius=15)
    create_starting_x.pack(side="left", pady=5)
    
    create_starting_y_text = tk.Label(create_options_frame1, text="Starting y:", font=("Verdana", 18), bg=LIGHT_GRAY, fg="white")
    create_starting_y_text.pack(side="left", padx=5, pady=5)
    
    create_starting_y = CTkEntry(create_options_frame1, width=145, height=50, font=("Verdana", 24), fg_color=DARK_GRAY, text_color="white", placeholder_text="0 to 980", placeholder_text_color=LIGHT_GRAY, border_color=DARK_GRAY, corner_radius=15)
    create_starting_y.pack(side="left", pady=5)
    
    create_starting_speed_text = tk.Label(create_options_frame2, text="Speed:", font=("Verdana", 18), bg=LIGHT_GRAY, fg="white")
    create_starting_speed_text.pack(side="left", padx=5, pady=5)
    
    create_starting_speed = CTkEntry(create_options_frame2, width=115, height=50, font=("Verdana", 24), fg_color=DARK_GRAY, text_color="white", placeholder_text=f"2 to {max_ufo_speed}", placeholder_text_color=LIGHT_GRAY, border_color=DARK_GRAY, corner_radius=15)
    create_starting_speed.pack(side="left", pady=5)
    
    create_starting_direction_text = tk.Label(create_options_frame2, text="Direction:", font=("Verdana", 18), bg=LIGHT_GRAY, fg="white")
    create_starting_direction_text.pack(side="left", padx=5, pady=5)
    
    create_starting_direction = CTkEntry(create_options_frame2, width=150, height=50, font=("Verdana", 24), fg_color=DARK_GRAY, text_color="white", placeholder_text="l, r, u or d", placeholder_text_color=LIGHT_GRAY, border_color=DARK_GRAY, corner_radius=15)
    create_starting_direction.pack(side="left", pady=5)
    
    create_starting_rotation_text = tk.Label(create_options_frame2, text="Rotation:", font=("Verdana", 18), bg=LIGHT_GRAY, fg="white")
    create_starting_rotation_text.pack(side="left", padx=5, pady=5)
    
    create_starting_rotation = CTkEntry(create_options_frame2, width=115, height=50, font=("Verdana", 24), fg_color=DARK_GRAY, text_color="white", placeholder_text="0 to 15", placeholder_text_color=LIGHT_GRAY, border_color=DARK_GRAY, corner_radius=15)
    create_starting_rotation.pack(side="left", pady=5)
    
    create_validate = CTkButton(padded_popup_zone, width=130, height=60, font=("Verdana", 30), text="Create the UFO", fg_color="#1CDC8D", hover_color="#28E496", cursor="hand2", corner_radius=15, command=create_ufo)
    create_validate.pack(pady=8)
    create_validate.propagate(False)


def setup_popup_help():
    """Setups elements for the 'Help' popup."""
    
    
    help_top_text = tk.Label(popup_frame, text="Here's a list of all the button:", font=("Verdana", 22), bg=LIGHT_GRAY, fg="white")
    help_top_text.pack()
    
    help_bg_frame = tk.Frame(popup_frame, bg=LIGHT_GRAY)
    help_bg_frame.pack(anchor='w', padx=5, pady=5)

    help_bg_preview = CTkButton(help_bg_frame, **bg_preview_style, text="", image=CTkImage(Image.open("bgs/bg2_preview.png").resize((80, 80)), size=(80, 80)))
    help_bg_preview.pack(side="left", padx=5)
    
    help_bg_text = tk.Label(help_bg_frame, text="Change the background image, 4 different options to choose.", font=("Verdana", 20), bg=LIGHT_GRAY, fg="white")
    help_bg_text.pack(side="left")
    
    help_create_frame = tk.Frame(popup_frame, bg=LIGHT_GRAY)
    help_create_frame.pack(anchor='w', padx=5, pady=5)
    
    help_create_button = CTkButton(help_create_frame, width=10, height=80, text="Create", font=("Verdana",34,"bold"), anchor="center", fg_color="#1CDC8D", text_color="white", hover_color="#28E496", corner_radius=15, cursor="hand2")
    help_create_button.pack(side="left", padx=5)
    
    help_create_text = tk.Label(help_create_frame, text="Create your own UFO, with name, skin and more options.", font=("Verdana", 20), bg=LIGHT_GRAY, fg="white")
    help_create_text.pack(side="left")
    
    help_evade_frame = tk.Frame(popup_frame, bg=LIGHT_GRAY)
    help_evade_frame.pack(anchor='w', padx=5, pady=5)
    
    help_evade_button = CTkButton(help_evade_frame, width=80, height=80, text="⯐", font=("Verdana",55,"bold"), anchor="w", fg_color="#EB9800", text_color="#C47F00", hover_color="#FFA500", corner_radius=15, cursor="hand2")
    help_evade_button.pack(side="left", padx=5)
    
    help_evade_text = tk.Label(help_evade_frame, text="Evade minigame, where you must flee UFOs and survive the longest.", font=("Verdana", 20), bg=LIGHT_GRAY, fg="white")
    help_evade_text.pack(side="left")
    
    help_battle_frame = tk.Frame(popup_frame, bg=LIGHT_GRAY)
    help_battle_frame.pack(anchor='w', padx=5, pady=5)
    
    help_battle_button = CTkButton(help_battle_frame, width=80, height=80, text="☣", font=("Verdana",55), anchor="center", fg_color="#00EBEB", text_color="#00C4C4", hover_color="#00FFFF", corner_radius=15, cursor="hand2")
    help_battle_button.pack(side="left", padx=5)
    
    help_battle_text = tk.Label(help_battle_frame, text="Battle minigame, UFOs fights until one remains.", font=("Verdana", 20), bg=LIGHT_GRAY, fg="white")
    help_battle_text.pack(side="left")
    
    help_plusminus_frame = tk.Frame(popup_frame, bg=LIGHT_GRAY)
    help_plusminus_frame.pack(anchor='w', padx=5, pady=5)
    
    help_plus_button = CTkButton(help_plusminus_frame, width=80, height=80, text="+", font=("Verdana",55), anchor="n", fg_color="#00EB00", text_color="#00C400", hover_color="#00FF00", corner_radius=15, cursor="hand2")
    help_plus_button.pack(side="left", padx=5)
    
    help_plus_text = tk.Label(help_plusminus_frame, text="Adds an UFO to the board.", font=("Verdana", 20), bg=LIGHT_GRAY, fg="white")
    help_plus_text.pack(side="left")
    
    help_minus_button = CTkButton(help_plusminus_frame, width=80, height=80, text="‒", font=("Verdana",55), anchor="n", fg_color="#D80000", text_color="#B10000", hover_color="red", corner_radius=15, cursor="hand2")
    help_minus_button.pack(side="left", padx=5)
    
    help_minus_text = tk.Label(help_plusminus_frame, text="Removes a random UFO.", font=("Verdana", 20), bg=LIGHT_GRAY, fg="white")
    help_minus_text.pack(side="left")

#━━━━━━━━━━#   MAIN   #━━━━━━━━━━#

root = CTk()
root.title("Cosmic Realm")
root.geometry("1440x810")
root.iconbitmap("icon.ico")
root.minsize(1440, 810)
root.maxsize(1920, 1080)

bottom = tk.Frame(root, height=100, bg=DARK_GRAY)
bottom.pack(side="bottom", fill="x")
bottom.propagate(False)

bottom_bar = tk.Frame(bottom, height=90, bg=DARK_GRAY)
bottom_bar.pack(fill="x", padx=10, pady=5)
bottom_bar.propagate(False)

canvas = tk.Canvas(root, width=1920, height=1080, borderwidth=0, highlightthickness=0, relief="flat")
canvas.pack(expand=True, fill="both")