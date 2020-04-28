"""
This is my simple implementation of the L-System algorithm for generating fractals

The functions include the basic text processing function, which is the core of the algorithm, as well as my implementation of a 2D fractal renderer
"""

from tkinter import *
from tkinter import *
from tkinter import font as tkFont
import copy
from random import uniform

def createSentence(current, rules, iterations):
    #this function creates the sentence based on the axiom and the rules given

    next = ""

    if iterations > 0:

        iterations-=1

        for n in current:
            for r in rules:
                if n == r[0]:
                    next = next + r[1 : len(r)]
                    break

        return createSentence(next, rules, iterations)

    else:
        print ("Generated sentence: {}".format(current))
        return current
