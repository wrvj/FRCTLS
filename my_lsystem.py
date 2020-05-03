"""
This is my simple implementation of the L-System algorithm for generating fractals

The functions include the basic text processing function, which is the core of the algorithm, as well as my implementation of a 2D fractal renderer

I am also including here some of my basic implementations of vector transformations to handle the rotation and other fractal manipulation
"""

from tkinter import *
from tkinter import *
from tkinter import font as tkFont
import copy
from random import uniform
import numpy as np
import time
from operator import add


def create_sentence(current, rules, iterations):

    #this recursive function creates the sentence based on the axiom and the rules given

    next = ""

    if iterations > 0:

        iterations-=1

        for n in current:
            for r in rules:
                if n == r[0]:
                    next = next + r[1 : len(r)]
                    break

        return create_sentence(next, rules, iterations)

    else:
        print ("Generated sentence: {}".format(current))
        return current


def create_fractal (sentence, angle_offset = 0, randomness = 0, invert_y = -1, lenght = 5):

    # returns a list of lines based on the sentence

    angle_offset = np.radians(angle_offset)
    angle = 0
    current_position = [0,0]
    lines = []
    before_time = time.time()
    vertices = [0.0,0.0]

    line_lenght = lenght

    def add_line():
        nonlocal line_lenght
        nonlocal current_position
        lines.append([[current_position[0], invert_y*current_position[1]], [current_position[0]+line_lenght*np.sin(angle), invert_y*(current_position[1]+line_lenght*np.cos(angle))]])
        vertices.append(current_position[0]+line_lenght*np.sin(angle))
        vertices.append(invert_y*(current_position[1]+line_lenght*np.cos(angle)))
        current_position = [current_position[0]+line_lenght*np.sin(angle), current_position[1]+line_lenght*np.cos(angle)]
        #print (lines)

    def rot_right():
        nonlocal angle
        angle += angle_offset

    def rot_left():
        nonlocal angle
        angle -= angle_offset

    def save_state():
        print ('saving current state')
    def restore_state():
        print ('restoring current state')


    turtle_commands = {'F': add_line, '+': rot_right, '-': rot_left, '[': save_state, ']': restore_state, 'A': add_line, 'B': add_line}


    for c in sentence:
        try:
            turtle_commands[c]()
        except:
            continue

    print(time.time() - before_time)

    return lines


def render_fractal(canvas, lines = [], cursor = [], zoom_level = 1.0, mode = 1):

    #gets an fractal object, a list of lines, and renders the lines on the canvas given a zoom level and the cursor (center of zoom)

    lines_2 = []

    #method 1
    if mode == 1:
        for l in lines:
            lines_2.append([(l[0][0]*zoom_level) + cursor[0], (l[0][1]*zoom_level) + cursor[1], (l[1][0]*zoom_level) + cursor[0], (l[1][1]*zoom_level) + cursor[1]])
            canvas.create_line(lines_2, width = 5, fill = 'black')

    #update the position
    # for i, v in enumerate(lines):
    #     lines_2.append((v*zoom_level) + cursor[i%2])
    # #get the canvas and render the fractal into it
    # canvas.create_line(lines_2, width = 3, fill = 'black')


    # for l in lines:
    #
    #     canvas.create_line([(l[0][0]*zoom_level) + cursor[0],
    #                         (l[0][1]*zoom_level) + cursor[1],
    #                         (l[1][0]*zoom_level) + cursor[0],
    #                         (l[1][1]*zoom_level) + cursor[1]], width = 0.8, fill = 'grey')
    #     canvas.create_line([(l[0][0]*zoom_level) + cursor[0],
    #                         (l[0][1]*zoom_level) + cursor[1],
    #                         (l[1][0]*zoom_level) + cursor[0],
    #                         (l[1][1]*zoom_level) + cursor[1]], width = 1.8, fill = 'black')


def format_rules(rules_string):

    #capitalize every char, remove blanks, remove the arrows '->', split the string into a list, add the default rules to the new list of rules

    return rules_string.upper().replace(' ', '').replace('\t', '').replace('\n', '').replace('\r', '').replace('->', '').split(';') + ['++', '--', '[[', ']]', '<<', '>>']


def get_angle(origin, cursor):

    if cursor[0] != origin[0] and cursor[1] != origin[1]:
        angle = np.degrees(np.arctan((cursor[1] - origin[1])/(cursor[0] - origin[0])))

        if cursor[0] > origin[0]:
            angle += 90
        else:
            angle += 270
    else:
        angle = 0

    return angle

def rotate_fractal(fractal, angle, center_offset = [0,0]):


    #takes a list of lines and returns a rotated version of this list
    origin = get_fractal_center (fractal)

    #allows the user to input a custom center of rotation, represented by an offet from the fractal's origin
    center_of_rotation = list(map(add, origin, center_offset))

    angle = np.radians(angle)
    sin_angle, cos_angle = np.sin(angle), np.cos(angle) #get some useful values from the given angle using numpy

    for l in fractal:
        l[0][0], l[0][1] = ((cos_angle * (l[0][0]- center_of_rotation[0])) - (sin_angle * (l[0][1]- center_of_rotation[1]))) + center_of_rotation[0]  , ((sin_angle * (l[0][0] - center_of_rotation[0])) + (cos_angle * (l[0][1]- center_of_rotation[1]))) + center_of_rotation[1]
        l[1][0], l[1][1] = ((cos_angle * (l[1][0]- center_of_rotation[0])) - (sin_angle * (l[1][1]- center_of_rotation[1]))) + center_of_rotation[0]  , ((sin_angle * (l[1][0] - center_of_rotation[0])) + (cos_angle * (l[1][1]- center_of_rotation[1]))) + center_of_rotation[1]

    return fractal


def get_fractal_center(fractal):

    #takes a list of lines and returns its geometric center

    center_of_mass = [0.0,0.0]

    for l in fractal:
        center_of_mass[0] += l[0][0] + l[1][0]
        center_of_mass[1] += l[0][1] + l[1][1]

    center_of_mass = [center_of_mass[0]/(len(fractal)*2), center_of_mass[1]/(len(fractal)*2)]

    return center_of_mass

def create_circle(self, x, y, r):
    return self.create_oval(x-r, y-r, x+r, y+r)
