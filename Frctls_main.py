from tkinter import *
from tkinter import font as tkFont
import copy
from random import uniform
import my_lsystem


class Frctls:

    rules = []


    # helvetica36 = tkFont.Font(family = 'Helvetica', size = 36, weight = 'bold')


    def __init__(self, master):
        #create and set the configuration variables, as colours, fonts, etc.

        self.canvas_bg_color = '#d5d5d5'
        self.settings_frame_bg_color = '#0d0d0d'
        self.main_font_family = 'helvetica-bold'
        self.canvas_line_weight_scaler = 1.0
        self.helv24 = tkFont.Font(family='Helvetica', size=24, weight='bold')
        self.helv16 = tkFont.Font(family='Helvetica', size=16, weight='bold')
        self.helv36 = tkFont.Font(family='Helvetica', size=36, weight='bold')

        #takes the tk root object and assigns it to a local variable
        self.master = master
        self.master.config(bg = 'white')

        # #binds the <Configure> event to the resize elements function
        # self.master.bind('<Configure>', self.print_screen_size)

        #creates the main frame, wich is the parent of all ither widgets

        self.main_frame = Frame(self.master, bg = 'white')

        self.main_frame.place(x = 0, y = 0, relwidth = 1.0, relheight = 1.0)

        #Creates the main drawing canvas, where the fractals are going to be rendered
        self.drawing_canvas = Canvas(self.main_frame,
                                     height = (self.master.winfo_height()),
                                     width = self.master.winfo_width()*0.8,
                                     bg = self.canvas_bg_color)
        self.drawing_canvas.place(relx = 0.0, rely = 0.0, relwidth = 0.8, relheight = 1.0)


        self.settings_frame = Frame(self.main_frame, bg = self.settings_frame_bg_color)
        self.settings_frame.place(relx = 0.8, rely = 0.0, relwidth = 0.2, relheight = 1.0)

        self.settings_title = Label(self.settings_frame, text = 'Settings', bg = self.settings_frame_bg_color, fg = 'white', font = self.helv24)
        self.settings_title.place(relx = 0.5, rely = 0.05, anchor = 'n')

        #adding the action buttons (Execute fractal, save design, load design)

        #First, we create a container to hold the buttons
        self.settings_buttons_frame = Frame(self.settings_frame, bg = self.settings_frame_bg_color)
        self.settings_buttons_frame.place(relx = 0.5, rely = 0.6, anchor = 'n', relwidth = 0.9, relheight = 0.38)
        self.settings_buttons_frame.columnconfigure(0, weight=1)

        #Then, the buttons
        self.run_fractal_button = Button(self.settings_buttons_frame, text = 'FRCTL', bg = 'white', borderwidth = 0.0, font = self.helv24)
        self.run_fractal_button.grid(row = 0, column = 0, sticky = EW)

        #vertical spacing
        self.settings_buttons_frame.grid_rowconfigure(1, minsize = 7)

        self.save_fractal_button = Button(self.settings_buttons_frame, text = 'Save Design', bg = 'white', borderwidth = 0.0, font = self.helv16)
        self.save_fractal_button.grid(row = 2, column = 0, sticky = EW)

        #vertical spacing
        self.settings_buttons_frame.grid_rowconfigure(3, minsize = 5)

        self.load_fractal_button = Button(self.settings_buttons_frame, text = 'Load Design', bg = 'white', borderwidth = 0.0, font = self.helv16)
        self.load_fractal_button.grid(row = 4, column = 0, sticky = EW)




my_lsystem.createSentence("A", ["AABA", "BB"], 5)

root = Tk()
root.geometry ('{}x{}'.format(root.winfo_screenwidth(), root.winfo_screenheight()))
root.state('zoomed')
root.title("FRCTLS")
root.wm_iconbitmap('resources/icon.ico')


frctls = Frctls(root)
root.mainloop()
