import math

def calculate_quadrant(x,y):
    # Gets the x value and y value, then
    # calculates which quadrant the point
    # belongs in
    quadrant = 0
    if (x>= 0 and y>= 0):
        quadrant = 1
    if (x < 0 and y >= 0):
        quadrant = 2
    if (x < 0 and y < 0):
        quadrant = 3
    if (x >= 0 and y < 0):
        quadrant = 4

    return quadrant



def degree_to_radian(angle):
    return angle* (math.pi)/180

def radian_to_degree(angle):
    return angle* 180/(math.pi)

def take_correct_angle(x_value,y_value):
    # Function to take angle calculated from x, angle calulated from y and quadrant. Based
    # on the quadrant, the correct angle should get selected
    quadrant = calculate_quadrant(x_value,y_value)
    # Get some new x and y variables, which have positive values
    x = x_value if (x_value >= 0) else -x_value
    y = y_value if (y_value >= 0) else -y_value

    correct_angle = 0
    if (quadrant == 1):
        correct_angle = math.acos(x)
    if (quadrant == 2):
        correct_angle = math.pi - math.acos(x)
    if (quadrant == 3):
        correct_angle = -(math.pi - math.acos(x))
    if (quadrant == 4):
        correct_angle = -(math.acos(x))
    return correct_angle

