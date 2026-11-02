import random
import matplotlib as plt
import numpy as np
from prettytable import PrettyTable



def fitness_function(params):
    a, b, c = params
    if a <= 0:
        return -float('inf')
    
    vertex_x = -b/(2 * a)
    vertex_y = a * (vertex_x ** 2) + b * vertex_x + c
    
    y_left = a * (-1) ** 2 + b * (-1) + c
    y_right = a * (1) ** 2 + b * (1) + c
    
    curviness = abs(y_left - vertex_y) + abs(y_right - vertex_y)
    return -curviness
    