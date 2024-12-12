import math


def distance_calculation(coord_len1, coord_len2, coord_line1, coord_line2, lenght_map_distance):
    distance_lenght = math.sqrt(
        (coord_len1[0] - coord_len2[0]) ** 2 + (coord_len1[1] - coord_len2[1]) ** 2)
    coef_ = lenght_map_distance / distance_lenght
    distance_line = math.sqrt(
        (coord_line1[0] - coord_line2[0]) ** 2 + (coord_line1[1] - coord_line2[1]) ** 2)
    return distance_line * coef_
