import numpy as np
from math import sin, cos, degrees


def normalize_zero_one(val, max_val, min_val):
    return round((val - min_val) / (max_val - min_val), 2)


def euclidean_norm(start_point, end_point):
    distance = np.linalg.norm(np.asarray(start_point) - np.asarray(end_point), 2, 0)
    return distance


def get_equidistant_points(point1, point2, parts):
    return zip(np.linspace(point1[0], point2[0], parts + 1), np.linspace(point1[1], point2[1], parts + 1))


def get_arc_points(center, radius, theta0, theta1, nr_rays=25):
    x0, y0 = center

    dtheta = (theta1 - theta0) / (nr_rays - 1)
    angles = [theta0 + i * dtheta for i in range(nr_rays)]

    # DEBUG INFO
    #print("Theta 0: ", degrees(theta0))
    #print("Theta 1: ", degrees(theta1))
    #print("dtheta: ", degrees(dtheta))
    #print("Length of angles", angles.__len__())
    #for theta in angles:
    #    print("Angle in degrees: ", degrees(theta))

    points = [(x0 + radius * cos(theta), y0 - radius * sin(theta)) for theta in angles]

    #print("Length of points", points.__len__())

    return points