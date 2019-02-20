import numpy as np

# test data
list_of_coords = [[32,54],[74,12],[54,54],[27,49],[28,54],[78,102],[23,15],[1,1],[2,2],[3,3]]
current_coord = [0,0]

def get_next_coord(list, current):
    # Returns the closest known box coordinate to the current coordinate
    
    shortest_distance = 1000;
    
    nearest_coord = [0,0]
    
    # loops through every coordinate in the list of coordinates
    for coord in list:
        
        # calculates distance to that coordinate
        distance = np.sqrt((coord[0] - current[0])**2 + (coord[1] - current[1])**2)

        if(distance < shortest_distance and distance != 0):
                
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
    
    #print(current_bearing, theta)
    
    # adds 360 to both to alleviate 0 error
    current_bearing = current_bearing + 360
    theta = theta + 360
    
    #print(current_bearing, theta)
    
    bearing = theta - current_bearing
    
    if(bearing < -180):
        bearing = 360 + bearing
    elif(bearing > 180):
        bearing = 360 - bearing
        
    return round(bearing)

# test for getting list of coordinates in order from get_next_coord
for i in range(0,5):
    current_coord = get_next_coord(list_of_coords, current_coord)
    print(current_coord)

# test for calculating a turn angle based on current position, next block position and the current bearing
print(calculate_turn_angle([0,0],[-1,-1],-45))


#print(calculate_turn_angle(current_coord, get_next_coord(list_of_coords, current_coord), -45))

