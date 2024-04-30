from tkinter import *
import time
from info import *
from PIL import ImageTk, Image

def show_splash_screen():
    splash = Tk()
    splash.overrideredirect(1)  # Hide titlebar

    width_of_window = 800
    height_of_window = 400
    screen_width = splash.winfo_screenwidth()
    screen_height = splash.winfo_screenheight()
    x_coordinate = (screen_width / 2) - (width_of_window / 2)
    y_coordinate = (screen_height / 2) - (height_of_window / 2)
    splash.geometry("%dx%d+%d+%d" % (width_of_window, height_of_window, x_coordinate, y_coordinate))

    splash.attributes('-alpha', 0)

    splash_bg_image = PhotoImage(file="Images/Bg_Frame.png")

    canvas = Canvas(splash, width=width_of_window, height=height_of_window, highlightthickness=0)
    canvas.pack()

    canvas.create_image(0, 0, anchor=NW, image=splash_bg_image)

    for alpha in range(0, 256, 8):
        splash.attributes('-alpha', alpha / 255)
        splash.update()
        time.sleep(0.03)

    time.sleep(Splash_time)

    splash.attributes('-alpha', 1.0)

    splash.destroy()