import os
import my_lsystem
import numpy as np


def export_svg(fractal, name, path = ''):


    #find the fractal boundaries
    boundary = get_boundary(fractal)

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

def get_boundary(fractal):

    boundary = [fractal[0][0][0], fractal[0][0][1], fractal[0][0][0], fractal[0][0][1]]

    for l in fractal:
        for p in l:
            if p[0]<boundary[0]:
                boundary[0] = p[0]
            if p[0]>boundary[2]:
                boundary[2] = p[0]
            if p[1]<boundary[1]:
                boundary[1] = p[1]
            if p[1]>boundary[3]:
                boundary[3] = p[1]

    return boundary
