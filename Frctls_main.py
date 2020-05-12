import tkinter
from tkinter import *
from tkinter import font as tkFont
import copy
from random import uniform
import my_lsystem
from operator import add
from tkinter import ALL, EventType
import svg_export as svg
from svg_export import FractalDesign
import time
from PIL import ImageTk, Image


class Frctls:

    rules = []


    def __init__(self, master):

        #takes the tk root object and assigns it to a local variable
        self.master = master
        self.master.config(bg = 'white')

        #Load assets
        self.creating_fractal_img = ImageTk.PhotoImage(Image.open("resources/creating_fractal_image.png"))


        #create and set the configuration variables, as colours, fonts, etc.

        #default settings
        self.weezer_axiom = "-FFF--F++F++++F----F--F++F++++FF++FFFFF----FF++++FF----FFFFF++FF++++F++F--F----F++++F++F--FFF++F++F----F++F"

        #creates the variables to handle the user user inputs
        self.axiom_input_string = StringVar(value ='F+F+F+F')
        self.rules_input_string = "FF"
        self.angle_input_string = StringVar(value = '30')
        self.random_input_string = StringVar(value = '0')
        self.iterations_input_string = StringVar(value ='1')
        self.lines = []
        self.redraw_fractal = False



        #gets a list of saved fractals (objects of the type FractalDesign)to let the user load old designs
        self.fractal_designs, self.fractal_names = svg.load_fractals('fractal_designs.frctl')
        self.dropdown_holder = StringVar(value = self.fractal_names[0])



        #easyly accessable style variables
        self.canvas_bg_color = '#d5d5d5'
        self.settings_frame_bg_color = '#0d0d0d'
        self.user_input_bg_color = '#1a1a1a'
        self.main_font_family = 'helvetica-bold'
        self.canvas_line_weight_scaler = 1.0
        self.helv24 = tkFont.Font(family='Helvetica', size=24, weight='bold')
        self.helv16 = tkFont.Font(family='Helvetica', size=16, weight='bold')
        self.helv36 = tkFont.Font(family='Helvetica', size=36, weight='bold')

        #The zoom level applied to the drawings
        self.zoom_level = 1.0
        self.delta_pan = [0,0]
        self.fractal_position = [(self.master.winfo_width()*0.8)/2, self.master.winfo_height()/2]
        self.fractal_angle = 0.0
        self.last_cursor_angle = 0.0
        self.master.bind('<MouseWheel>', self.mouse_scroll_zoom)

        #creates the main frame, wich is the parent of all ither widgets
        self.main_frame = Frame(self.master, bg = 'white')
        self.main_frame.place(x = 0, y = 0, relwidth = 1.0, relheight = 1.0)

        #Creates the main drawing canvas, where the fractals are going to be rendered
        self.drawing_canvas = Canvas(self.main_frame,
                                     height = (self.master.winfo_height()),
                                     width = self.master.winfo_width()*0.8,
                                     bg = self.canvas_bg_color)
        self.drawing_canvas.place(relx = 0.0, rely = 0.0, relwidth = 0.8, relheight = 1.0)
        self.drawing_canvas.bind('<B2-Motion>', self.mouse_pan)
        self.drawing_canvas.bind('<Button-2>', self.set_pan_delta)
        self.drawing_canvas.bind('<B3-Motion>', self.mouse_rotation)
        self.drawing_canvas.bind('<Button-3>', self.set_cursor_angle)
        Canvas.create_circle = my_lsystem.create_circle


        #Creates the settings frame
        self.settings_frame = Frame(self.main_frame, bg = self.settings_frame_bg_color)
        self.settings_frame.place(relx = 0.8, rely = 0.0, relwidth = 0.2, relheight = 1.0)

        self.settings_title = Label(self.settings_frame, text = 'SETTINGS', bg = self.settings_frame_bg_color, fg = 'white', font = self.helv24)
        self.settings_title.place(relx = 0.5, rely = 0.05, anchor = 'n')

        #adds the user inputs pannel

        #First, we create a container to hold the user inputs
        self.user_inputs_frame = Frame(self.settings_frame, bg = self.settings_frame_bg_color)
        self.user_inputs_frame.place(relx = 0.5, rely = 0.2, anchor = 'n', relwidth = 0.9, relheight = 0.38)
        self.user_inputs_frame.columnconfigure(0, weight=1, minsize = 150)

        #adds the axiom input inside the user input frame
        self.axiom_input_label = Label (self.user_inputs_frame, text = 'Axiom:',bg = self.settings_frame_bg_color, fg = 'white', font = self.helv16)
        self.axiom_input_label.grid(row = 0, column = 0, sticky = EW)
        self.axiom_input = Entry(self.user_inputs_frame,
                                 textvariable = self.axiom_input_string,
                                 bg = self.user_input_bg_color,
                                 fg = 'white',
                                 font = self.helv16)
        self.axiom_input.grid(row = 1, column = 0, columnspan = 2, sticky = EW)

        #adds the rules input bellow the axiom
        self.rules_input_label = Label (self.user_inputs_frame, text = 'Rules:',bg = self.settings_frame_bg_color, fg = 'white', font = self.helv16)
        self.rules_input_label.grid(row = 2, column = 0, sticky = EW)
        self.rules_input = Text(self.user_inputs_frame, bg = self.user_input_bg_color, fg = 'white', font = self.helv16, height = 7)
        self.rules_input.insert(END, self.rules_input_string)
        self.rules_input.grid(row = 3, column = 0, columnspan = 2, sticky = EW)

        #adds the angle input inside the user input frame
        self.angle_input_label = Label (self.user_inputs_frame, text = 'Angle:',bg = self.settings_frame_bg_color, fg = 'white', font = self.helv16)
        self.angle_input_label.grid(row = 4, column = 0, sticky = EW)
        self.angle_input = Entry(self.user_inputs_frame, textvariable = self.angle_input_string, bg = self.user_input_bg_color, fg = 'white', font = self.helv16)
        self.angle_input.grid(row = 4, column = 1, sticky = E)

        #adds the randomness factor input inside the user input frame
        self.randomness_input_label = Label (self.user_inputs_frame, text = 'Random:',bg = self.settings_frame_bg_color, fg = 'white', font = self.helv16)
        self.randomness_input_label.grid(row = 5, column = 0, sticky = EW)
        self.randomness_input = Entry(self.user_inputs_frame, textvariable = self.random_input_string, bg = self.user_input_bg_color, fg = 'white', font = self.helv16)
        self.randomness_input.grid(row = 5, column = 1, sticky = E)

        #adds the iterations times input inside the user input frame
        self.iterations_input_label = Label (self.user_inputs_frame, text = 'Iterations:',bg = self.settings_frame_bg_color, fg = 'white', font = self.helv16)
        self.iterations_input_label.grid(row = 6, column = 0, sticky = EW)
        self.iterations_input = Entry(self.user_inputs_frame, textvariable = self.iterations_input_string, bg = self.user_input_bg_color, fg = 'white', font = self.helv16)
        self.iterations_input.grid(row = 6, column = 1, sticky = E)

        #adds the dropdown menu for the user to load a fractal design
        self.load_fractal_dropdown = OptionMenu (self.user_inputs_frame, self.dropdown_holder, *self.fractal_names, command = self.open_design)
        self.load_fractal_dropdown.config(bg = self.settings_frame_bg_color, fg = 'white', font = self.helv16)
        self.load_fractal_dropdown.grid(row = 7, column = 0, columnspan = 2, sticky = EW)


        #adds the action buttons (Execute fractal, save design, load design)

        #First, we create a container to hold the buttons
        self.settings_buttons_frame = Frame(self.settings_frame, bg = self.settings_frame_bg_color)
        self.settings_buttons_frame.place(relx = 0.5, rely = 0.6, anchor = 'n', relwidth = 0.9, relheight = 0.38)
        self.settings_buttons_frame.columnconfigure(0, weight=1)

        #Then, the buttons
        self.run_fractal_button = Button(self.settings_buttons_frame, text = 'FRCTL', command = self.update_fractal, bg = 'white', borderwidth = 0.0, font = self.helv24)
        self.run_fractal_button.grid(row = 0, column = 0, sticky = EW)

        #vertical spacing
        self.settings_buttons_frame.grid_rowconfigure(1, minsize = 7)

        self.save_fractal_button = Button(self.settings_buttons_frame, text = 'Save Design', command = self.save_design, bg = 'white', borderwidth = 0.0, font = self.helv16)
        self.save_fractal_button.grid(row = 2, column = 0, sticky = EW)

        #vertical spacing
        self.settings_buttons_frame.grid_rowconfigure(3, minsize = 5)

        self.export_fractal_button = Button(self.settings_buttons_frame, text = 'Export Design', command = self.export_fractal, bg = 'white', borderwidth = 0.0, font = self.helv16)
        self.export_fractal_button.grid(row = 4, column = 0, sticky = EW)



    def update_fractal(self):

        #create the sentence based on the iterations, rules and axiom given by the user

        sentence = my_lsystem.create_sentence(self.axiom_input_string.get().upper(), my_lsystem.format_rules(self.rules_input.get("1.0",'end-1c')), int(self.iterations_input_string.get()))

        #transform the sentence into a fractal

        self.lines = my_lsystem.create_fractal (sentence, int(self.angle_input_string.get()), randomness = int(self.random_input_string.get()), lenght = 10)

        #adjusts the zoom level based on the size of the fractal
        bounds = my_lsystem.get_boundary(self.lines)
        print (self.lines)
        self.zoom_level = 1/((bounds[2] - bounds[0])/self.drawing_canvas.winfo_width())

        if 1/((bounds[3] - bounds[1])/self.drawing_canvas.winfo_height()) < self.zoom_level:
            self.zoom_level = 1/((bounds[3] - bounds[1])/self.drawing_canvas.winfo_height())

        #apply a margin to the zoom level
        self.zoom_level = 0.8 * self.zoom_level
        #adjusts the fractal position prior to drawing
        self.fractal_position = [0.1 * self.drawing_canvas.winfo_width(),
                                 0.9 * self.drawing_canvas.winfo_height()]
        self.fractal_position[0] += self.fractal_position[0] - ((bounds[0] * self.zoom_level)+(0.1 * self.drawing_canvas.winfo_width()))
        self.fractal_position[1] += ((-1 * (bounds[1] * (self.zoom_level))) + (0.1 * self.drawing_canvas.winfo_height())) - self.fractal_position[1]

        # #debub drawings
        # print (bounds)
        # self.drawing_canvas.create_circle(*self.fractal_position, 5)
        # self.drawing_canvas.create_circle((bounds[0] * self.zoom_level)+(0.1 * self.drawing_canvas.winfo_width()), ((-1 * (bounds[1] * (self.zoom_level))) + (0.1 * self.drawing_canvas.winfo_height())) - self.fractal_position[1], 10)

        #render the fractal
        self.drawing_canvas.delete('all')
        my_lsystem.render_fractal(self.drawing_canvas, self.lines, self.fractal_position, self.zoom_level)

    #Export Fractal as svg
    def export_fractal(self):
        svg.export_svg(self.lines, 'Teste')

    #handling the exporting popup window
    def save_design(self):
        args = [self.axiom_input.get(), self.rules_input.get("1.0",'end-1c'), self.angle_input.get(), self.randomness_input.get()]

        def save(frctl_name, axiom, rules, angle, randomness):

            new_frac = FractalDesign(frctl_name, 'none', axiom, rules, angle, randomness)
            new_frac.save_design('fractal_designs.frctl')
            popup.destroy()

        popup = Tk()
        popup.wm_title("Save design")
        self.name_string = StringVar(value = 'Name')
        name_input = Entry(popup, textvariable = self.name_string, bg = self.user_input_bg_color, fg = 'white', font = self.helv16)
        name_input.pack()
        B1 = Button(popup, text="Save", command = lambda: save(name_input.get(), *args))
        B1.pack()
        popup.mainloop()

    def open_design(self, event):

        self.axiom_input_string.set(self.fractal_designs[event].get_data()[2])
        self.rules_input_string = self.fractal_designs[event].get_data()[3]
        self.angle_input_string.set(self.fractal_designs[event].get_data()[4])
        self.random_input_string.set(self.fractal_designs[event].get_data()[5])





    #Handles the zoom level
    def mouse_scroll_zoom(self, event):

        ammount = 1+(0.0005*event.delta)

        self.drawing_canvas.scale('all', event.x, event.y, ammount, ammount)
        #updates the zoom level based on the mouse wheel movement

        # self.zoom_level = self.zoom_level + (event.delta*0.02)
        #
        # self.zoom_level = 1.0
        # #apply the new zoom level to the Canvas
        #
        # self.drawing_canvas.delete('all')
        # self.drawing_canvas.scale(ALL, event.x, event.y, 1.001 * event.delta, 1.001 * event.delta)
        # my_lsystem.render_fractal(self.drawing_canvas, self.lines, self.fractal_position, self.zoom_level)


    #Handles the mouse pan
    def mouse_pan (self, event):

        #updates the fractal position based on the delta from the current mouse position. This delta is obtained in the function set_pan_delta()
        #print (event)
        self.drawing_canvas.move('all', event.x - self.delta_pan[0], event.y - self.delta_pan[1])
        self.delta_pan[0], self.delta_pan[1] = event.x, event.y
        # self.fractal_position = [event.x - self.delta_pan[0], event.y - self.delta_pan[1]]
        #
        # #apply the new zoom level to the Canvas
        #
        # self.drawing_canvas.delete('all')
        # my_lsystem.render_fractal(self.drawing_canvas, self.lines, self.fractal_position, self.zoom_level)


    def set_pan_delta(self, event):

        #Get the current offset from to mouse to the fractal position

        self.delta_pan[0], self.delta_pan[1] = event.x, event.y

        #print(self.delta_pan)

    #Handles the rotation
    def mouse_rotation (self, event):

        global_fractal_origin = [self.fractal_position[0] + (my_lsystem.get_fractal_center(self.lines)[0]*self.zoom_level),
                                 self.fractal_position[1] + (my_lsystem.get_fractal_center(self.lines)[1]*self.zoom_level)]


        new_cursor_angle = my_lsystem.get_angle(global_fractal_origin, [event.x, event.y])
        rotation_angle = self.last_cursor_angle - new_cursor_angle

        self.lines = my_lsystem.rotate_fractal(self.lines, -rotation_angle)
        self.drawing_canvas.delete('all')
        my_lsystem.render_fractal(self.drawing_canvas, self.lines, self.fractal_position, self.zoom_level)
        self.drawing_canvas.create_circle(*global_fractal_origin, 5)
        self.last_cursor_angle = new_cursor_angle


    def set_cursor_angle (self, event):
        global_fractal_origin = [self.fractal_position[0] + (my_lsystem.get_fractal_center(self.lines)[0]*self.zoom_level),
                                 self.fractal_position[1] + (my_lsystem.get_fractal_center(self.lines)[1]*self.zoom_level)]
        self.last_cursor_angle = my_lsystem.get_angle (global_fractal_origin,[event.x, event.y])






root = Tk()
root.geometry ('{}x{}'.format(root.winfo_screenwidth(), root.winfo_screenheight()))
root.state('zoomed')
root.title("FRCTLS")
root.wm_iconbitmap('resources/icon.ico')

frctls = Frctls(root)
root.mainloop()
