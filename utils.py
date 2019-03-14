import numpy as np


def get_next_coord(list, current):
    # Returns the closest known box coordinate to the current coordinate

    shortest_distance = 1000;

    nearest_coord = [0, 0]

    # loops through every coordinate in the list of coordinates
    for coord in list:

        # calculates distance to that coordinate
        distance = np.sqrt((coord[0] - current[0]) ** 2 + (coord[1] - current[1]) ** 2)

        if (distance < shortest_distance and distance != 0):
            shortest_distance = distance
            nearest_coord = coord

    # removes the found coordinate from the list of coordinates so it won't be found again
    list.remove(nearest_coord)

    return nearest_coord


def calculate_turn_angle(current_coord, next_coord, current_bearing):
    # finds x and y components of relative position vector
    x_comp = next_coord[0] - current_coord[0]
    y_comp = next_coord[1] - current_coord[1]

    # calculate angle between current coordinate and the next
    theta = np.arctan2(y_comp, x_comp)

    # converts from degrees to radians
    theta = (theta / np.pi) * 180

    # print(current_bearing, theta)

    # adds 360 to both to alleviate negative error
    current_bearing = current_bearing + 360
    theta = theta + 360

    bearing = theta - current_bearing

    bearing = bearing % 360

    if (bearing < 0):
        bearing = 360 + bearing
    return round(bearing)


def get_angle(current_coords, next_coords, current_bearing):
    desired_bearing = - np.arctan2(
        (next_coords[1] - current_coords[1]), (next_coords[0] - current_coords[0])) * 180 / np.pi

    if current_bearing > desired_bearing:
        return 360 - current_bearing + desired_bearing

    else:
        return desired_bearing - current_bearing


# get distance measurement between two coordinates - returns in integer centimetres
def get_distance(current_coords, next_coords):
    # get conversion between pixels and distance cm / pixel
    pixel_conversion = 99.7 / 235

    pixel_distance = ((current_coords[0] - next_coords[0]) ** 2 + (current_coords[1] - next_coords[1]) ** 2) ** 0.5

    return int(round(pixel_distance * pixel_conversion))


def get_nearest_box(boxes, robot):
    # takes a list of boxes, filters for ones that are available then returns box with nearest coordinates
    def distance_to_robot(box):
        return ((box.x - robot.x) ** 2 + (box.y - robot.y) ** 2) ** 0.5

    available_boxes = [box for box in boxes if box.available]

    available_boxes.sort(key=lambda box: box.x)
    return available_boxes[0]


def get_nearest_box_with_removal(boxes, robot):
    # take a list of boxes, filtered for those available, returns box and updated list of boxes
    def distance_to_robot(box):
        return ((box.x - robot.x) ** 2 + (box.y - robot.y) ** 2) ** 0.5

    available_boxes = [box for box in boxes if box.available]

    # sort based on lowest x position
    available_boxes.sort(key=lambda bot: bot.x)

    nearest_box = available_boxes[0]
    updated_box = nearest_box
    updated_box.available = False

    boxes[boxes.index(nearest_box)] = updated_box

    return boxes, nearest_box
