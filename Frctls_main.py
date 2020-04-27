from tkinter import *
import copy
from random import uniform


class Frctls:

    rules = []


    def __init__(self, master):
        #create and set the configuration variables, as colours, fonts, etc.

        self.canvas_bg_color = '#d5d5d5'
        self.settings_frame_bg_color = '#0d0d0d'
        self.main_font_family = 'helvetica-bold'
        self.canvas_line_weight_scaler = 1.0

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

        self.settings_title = Label(self.settings_frame, text = 'Settings', bg = self.settings_frame_bg_color, fg = 'white', font = self.main_font_family)
        self.settings_title.place(relx = 0.5, rely = 0.05, anchor = 'n')





root = Tk()
root.geometry ('{}x{}'.format(root.winfo_screenwidth(), root.winfo_screenheight()))
root.state('zoomed')
root.title("FRCTLS")
root.wm_iconbitmap('resources/icon.ico')


frctls = Frctls(root)
root.mainloop()
