import os
import my_lsystem
import numpy as np
import pickle


class FractalDesign:

    def __init__(self, name, description, axiom, rules, angle, random):

        self.name, self.description, self.axiom, self.rules, self.angle, self.random = name, description, axiom, rules, angle, random

    def __repr__(self):
        return "Name: {}\nDescription: {}\nAxiom: {}\nRules: {}\nAngle: {}\nRandom: {}".format(self.name, self.description, self.axiom, self.rules, self.angle, self.random)

    def save_design(self, filename):

        fractal = self
        temp_dict = dict()

        try:
            with open(filename, 'rb') as f:
                temp_dict = pickle.load(f)
                temp_dict.update({fractal.name : fractal})
                pickle.dump(temp_dict, f)
        except:
            with open(filename, 'wb') as f:
                temp_dict.update({fractal.name : fractal})
                pickle.dump(temp_dict, f)


    def get_data(self):
        return (self.name, self.description, self.axiom, self.rules, self.angle, self.random)

def load_fractals(filename):
    name_list = []
    temp_dict = dict()
    try:
        with open(filename, 'rb') as f:
            temp_dict = pickle.load(f)

            #try to return a dictionary of fractals to the user

            for d in list(temp_dict):
                print (d)
                #name_list.append(d['name'])

            return (temp_dict, list(temp_dict))
    except:
        print ('no fractals found at {}'.format(filename))
        return (None, list(['No saved fractal found.']))

def export_svg(fractal, name, path = ''):


    #find the fractal boundaries
    boundary = my_lsystem.get_boundary(fractal)

    #first, create the String
    svg_lines = ''
    for l in fractal:
        l = [[l[0][0]-boundary[0], l[0][1]-boundary[1]],[l[1][0]-boundary[0], l[1][1]-boundary[1]]]
        svg_lines += "<line class='a' x1='{}' y1='{}' x2='{}' y2='{}'/>\n".format(l[0][0], l[0][1], l[1][0], l[1][1])

    fractal_center = my_lsystem.get_fractal_center(fractal)

    svg_header = f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 {boundary[2] - boundary[0]} {boundary[3] - boundary[1]}'>\n"
    svg_style = "<defs>\n<style>.a{fill:none;stroke:#231f20;stroke-miterlimit:10;}</style>\n</defs>\n"
    svg_title = f"<title>{name}</title>\n"

    svg_file = svg_header + svg_style + svg_title + svg_lines + '</svg>'


    try:
        os.mkdir('{}/{}'.format(os.getcwd(), path))
    except:
        path = '{}/{}'.format(os.getcwd(), path)
        with open(f'{path}/{name}.svg', 'w') as f:
            f.write(svg_file)
