from PIL import Image

#━━━━━━━━━━#   VARIABLES   #━━━━━━━━━━#

# UFOs available to be displayed
### Add one by copying a line and putting it under, change the name at the start and the path to your image.
ufo_skins = {
    "Blue": {"Path": "ufos/blue.png", "Height": Image.open("ufos/blue.png").height},
    "Pink": {"Path": "ufos/pink.png", "Height": Image.open("ufos/pink.png").height},
    "Red": {"Path": "ufos/red.png", "Height": Image.open("ufos/red.png").height},
    "Gold": {"Path": "ufos/gold.png", "Height": Image.open("ufos/gold.png").height},
    "Silver": {"Path": "ufos/silver.png", "Height": Image.open("ufos/silver.png").height},
    "Cyprus": {"Path": "ufos/cyprus.png", "Height": Image.open("ufos/cyprus.png").height},
}

# UFOs shown at the launch of the app.
### Change if you want to start the app with more UFOs, max_ufo_number doesn't apply on it, set 0 to disable.
starting_ufos = 4

# All speeds the UFOs can fly at.
### Change if you want to set custom values for UFOs at the start, avoid exceeding 8 due to visual glitches.
speed_values = [2, 2.25, 2.50, 2.75, 3, 3.25, 3.50, 3.75, 4, 4.25, 4.50, 4.75, 5, 5.25, 5.50, 5.75, 6, 6.25, 6.50, 6.75, 7, 7.25, 7.50, 7.75, 8]

# Number of milliseconds when a UFO gets added, max_ufo_number applies.
### Change the value to add UFOs quicker/slower to the board (in milliseconds), set 0 if disabled.
add_ufo_time = 30000

# Maximum UFOs displayed on the screen.
### Change if you want to display more UFOs, can lag on low-end devices above 25.
max_ufo_number = 25

# Maximum speed for UFOs.
### Change to increase the maximum speed of UFOs when created, will cause visual glitches above 8.
max_ufo_speed = 8

# Maximum degrees rotation for spawned UFOs.
### Change to tilt more your UFOs, causes visual glitches for some UFO skins above 12.
max_rotation_ufo = 10

# All colors, change to your liking.
DARK_GRAY = "#1F1F1F"  # Dark tint of gray, used for bottom_bar, popup background and entries background.
LIGHT_GRAY = "#2C2C2C"  # Light tint of gray, used for popup_frame color, and background of buttons 
LIGHTEST_GRAY = "#3C3C3C"  # Lightest tint of gray, used for buttons hover color, frames containing UFOs images and separators
BACKG_BLUE = "#0664F5"  # Border of the button once the background/UFO is selected.
FONT_COLOR = "#FFFFFF"  # Font color for all the text in the app.
LIGHT_GREEN = "#00FF00"  # Background color of notification popup in bottom right.

# IDs of UFOs created, made so it is easier to delete and recognize them.
### Change if you want to change the IDs offsets.
id_entities = 1

# Time battle mini-game will last, in seconds.
### Change if you want longer time for this mini-game.
minigame_time = 10

# Width and height of the screen, changes according to the screen resolution.
wscreen, hscreen = 1440, 810

# Settings for a Tkinter Button used frequently.
bg_preview_style = {"width": 80, "height": 80, "fg_color": LIGHT_GRAY, "hover_color": LIGHTEST_GRAY, "corner_radius": 15, "cursor": "hand2"}

# State of the notification popup (whether it is currently shown or not).
notif_popup_shown = False

# State of the info popup (whether it is currently shown or not), True if shown, False otherwise.
shown_info_popup = False
# ID of the currently displayed info popup, None if none.
shown_info_id = None