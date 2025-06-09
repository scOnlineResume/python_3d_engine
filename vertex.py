import pygame
import math
import unit_circle
import game_constants

class Vertex():
    def __init__(self,game,triangle,shape,position_vector):
        self.game = game
        self.triangle = triangle
        self.shape = shape
        self.shape_center = self.shape.center

        # Positions in different spaces
        self.position = position_vector
        self.camera_space_position = [0,0,0]
        self.projected_position = (0,0) # Set to (0,0) for now, changle later in the function

        ## TODO - get this data from somewhere else later
        self.speed = 10
        self.rotation_speed = 0.2







    def get_position(self):
        return [self.position[0],self.position[1],self.position[2]]

    def get_vertex_number(self):
        return self.vertex_number

    def set_camera_space_position(self,x,y,z):
        self.camera_space_position[0] = x
        self.camera_space_position[1] = y
        self.camera_space_position[2] = z

    def get_camera_space_position(self):
        return self.camera_space_position

    def update(self,actions):
        #self.calculate_new_position(actions)
        #self.calculate_projected_position()
        pass

        
    def move_left_right(self,speed,direction_number):
        ## TODO - later, this function will be called from Triangle object
        # then it would return the value.

        # Move the vertex left or right
        self.position[0] += speed * direction_number

    def move_forward_back(self,speed,direction_number):
        ## TODO - later, this function will be called from Triangle object
        # then it would return the value.

        # Move the vertex forward or back
        self.position[2] += speed * direction_number


    def move_up_down(self,speed,direction_number):
        ## TODO - later, this function will be called from Triangle object
        # then it would return the value.
        
        # Move the vertex up or down
        self.position[1] += speed * direction_number




    def calculate_projected_position(self):
        screen_width = self.shape.game.GAME_W
        screen_height = self.shape.game.GAME_H
        depth_angle = self.shape.game.view_depth_angle
        point_3d = self.camera_space_position


        length_of_slice = screen_width + 2* (point_3d[2] - game_constants.CAMERA_DISTANCE_BUFFERED) * math.tan(depth_angle)
        new_x_min =  - ((point_3d[2] - game_constants.CAMERA_DISTANCE_BUFFERED) * math.tan(depth_angle)) 
        new_x_max =   screen_width + (point_3d[2] - game_constants.CAMERA_DISTANCE_BUFFERED) * math.tan(depth_angle) 
        new_y_min =  - ((point_3d[2] - game_constants.CAMERA_DISTANCE_BUFFERED) * math.tan(depth_angle))  
        new_y_max =   screen_width + (point_3d[2] - game_constants.CAMERA_DISTANCE_BUFFERED) * math.tan(depth_angle)  

        old_x = point_3d[0]
        old_y = point_3d[1]

        # Calculate "proportion" of x and y on the new slice
        x_proportion = (old_x + (point_3d[2] - game_constants.CAMERA_DISTANCE_BUFFERED) * math.tan(depth_angle))/length_of_slice
        y_proportion = (old_y + (point_3d[2] - game_constants.CAMERA_DISTANCE_BUFFERED) * math.tan(depth_angle))/length_of_slice

        x_new = x_proportion * screen_width
        y_new = y_proportion * screen_height

        self.projected_position = (x_new,y_new)

        # Hack, if z value less than 0, then set projected position to
        # extremely off screen funky value
        # Later, maybe change the 2500 to 0
        if point_3d[2] <= game_constants.CAMERA_DISTANCE:
            x_new = 0
            y_new = 0
            self.projected_position = (0,0)

        return (x_new,y_new)

    def render(self,display):
        # TODO - use projected position to draw onto screen
        pygame.draw.circle(display,(250,250,250),self.projected_position,1)



