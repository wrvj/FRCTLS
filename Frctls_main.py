from tkinter import *
from tkinter import font as tkFont
import copy
from random import uniform
import my_lsystem


class Frctls:

    rules = []


    # helvetica36 = tkFont.Font(family = 'Helvetica', size = 36, weight = 'bold')


    def __init__(self, master):

        #takes the tk root object and assigns it to a local variable
        self.master = master
        self.master.config(bg = 'white')


        #create and set the configuration variables, as colours, fonts, etc.

        self.weezer_axiom = "-FFF--F++F++++F----F--F++F++++FF++FFFFF----FF++++FF----FFFFF++FF++++F++F--F----F++++F++F--FFF++F++F----F++F"

        #creates the variables to handle the user user inputs
        self.axiom_input_string = StringVar()
        self.rules_input_string = ""
        self.angle_input_string = StringVar()
        self.random_input_string = StringVar()
        self.iterations_input_string = StringVar()
        self.lines = []


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

        #adds the auto-update checkbox input inside the user input frame (use .get() to get the state)
        self.autoupdate_input_label = Label (self.user_inputs_frame, text = 'Auto Update:',bg = self.settings_frame_bg_color, fg = 'white', font = self.helv16)
        self.autoupdate_input_label.grid(row = 7, column = 0, sticky = EW)
        self.autoupdate_input = Checkbutton(self.user_inputs_frame, bg = self.settings_frame_bg_color)
        self.autoupdate_input.grid(row = 7, column = 1, sticky = W)

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

        self.save_fractal_button = Button(self.settings_buttons_frame, text = 'Save Design', bg = 'white', borderwidth = 0.0, font = self.helv16)
        self.save_fractal_button.grid(row = 2, column = 0, sticky = EW)

        #vertical spacing
        self.settings_buttons_frame.grid_rowconfigure(3, minsize = 5)

        self.load_fractal_button = Button(self.settings_buttons_frame, text = 'Load Design', bg = 'white', borderwidth = 0.0, font = self.helv16)
        self.load_fractal_button.grid(row = 4, column = 0, sticky = EW)

    #Handles the UPDATE Fractal button pressed
    def update_fractal(self):

        #create the sentence based on the iterations, rules and axiom given by the user
        sentence = my_lsystem.create_sentence(self.axiom_input_string.get().upper(), my_lsystem.format_rules(self.rules_input.get("1.0",'end-1c')), int(self.iterations_input_string.get()))
        #transform the sentence into a fractal
        self.lines = my_lsystem.create_fractal (sentence, int(self.angle_input_string.get()), int(self.random_input_string.get()), lenght = 10)

        #render the fractal
        self.drawing_canvas.delete('all')
        my_lsystem.render_fractal(self.drawing_canvas, self.lines, self.fractal_position, self.zoom_level)

    #Handles the zoom level
    def mouse_scroll_zoom(self, event):

        #updates the zoom level based on the mouse wheel movement
        self.zoom_level = self.zoom_level + (event.delta*0.02)

        #apply the new zoom level to the Canvas
        self.drawing_canvas.delete('all')
        my_lsystem.render_fractal(self.drawing_canvas, self.lines, self.fractal_position, self.zoom_level)

    #Handles the mouse pan

    def mouse_pan (self, event):
        #updates the fractal position based on the delta from the current mouse position. This delta is obtained in the function set_pan_delta()
        self.fractal_position = [event.x - self.delta_pan[0], event.y - self.delta_pan[1]]

        #apply the new zoom level to the Canvas
        self.drawing_canvas.delete('all')
        my_lsystem.render_fractal(self.drawing_canvas, self.lines, self.fractal_position, self.zoom_level)

    def set_pan_delta(self, event):
        #Get the current offset from to mouse to the fractal position
        self.delta_pan[0], self.delta_pan[1] = event.x-self.fractal_position[0], event.y-self.fractal_position[1]
        #print(self.delta_pan)



root = Tk()
root.geometry ('{}x{}'.format(root.winfo_screenwidth(), root.winfo_screenheight()))
root.state('zoomed')
root.title("FRCTLS")
root.wm_iconbitmap('resources/icon.ico')

frctls = Frctls(root)
root.mainloop()
