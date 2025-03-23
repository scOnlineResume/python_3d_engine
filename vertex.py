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
        self.position = position_vector
        self.projected_position = (0,0) # Set to (0,0) for now, changle later in the function

        # Used for movement
        self.speed = self.game.get_movement_speed()
        self.rotation_speed = self.game.get_rotation_speed()







    def get_position(self):
        return self.position

    def get_vertex_number(self):
        return self.vertex_number

    def update(self,actions):
        self.calculate_new_position(actions)
        #self.calculate_projected_position()





    def calculate_new_position(self,actions):
        if (actions["right"]):
            # Strafe right
            self.move_left_right(1,-1)
        if (actions["left"]):
            # Strafe left
            self.move_left_right(1,1)
        if (actions["up"]):
            # Move forward
            self.move_forward_back(1,-1)
        if (actions["down"]):
            # Move backward
            self.move_forward_back(1,1)
        if (actions["q"]):
            # Move up
            self.move_up_down(1,1)
        if (actions["e"]):
            # Move down
            self.move_up_down(1,-1)
        if actions["arrow_left"]:
            # Look left
            self.look_left_right(1,-1)
        if actions["arrow_right"]:
            # Look right
            self.look_left_right(1,1)
        if actions["arrow_up"]:
            # Look up
            self.look_up_down(1,-1)
        if actions["arrow_down"]:
            # Look down
            self.look_up_down(1,1)
        
    def move_left_right(self,speed,direction_number):        
        # Move the vertex left or right
        self.position[0] += speed * direction_number

    def move_forward_back(self,speed,direction_number):
        # Move the vertex forward or back
        self.position[2] += speed * direction_number

    def look_left_right(self,speed,direction_number):
        # Get camera position
        camera_x, camera_y, camera_z = self.game.get_camera()

        # Rotate each vertex around a 2D circle
        rotation_center = (self.game.GAME_W/2,self.position[1],0)

        # The x-z coordinates relative to center of rotation
        rel_x_z = (self.position[0] - rotation_center[0] ,self.position[2] - rotation_center[2] - game_constants.CAMERA_DIFF)

        # Distance between vector and rotation center
        rel_x_z_magnitude = math.sqrt(rel_x_z[0]**2 + rel_x_z[1]**2)
        if rel_x_z_magnitude == 0:
            rel_x_z_magnitude = 0.01

        # Calculate the corresponding normal vector
        rel_x_z_normal = [rel_x_z[0]/rel_x_z_magnitude,rel_x_z[1]/rel_x_z_magnitude]

        # Calculate angle of the vertex relative to rotation center by considering
        # whether x and z are positive or negative
        theta = unit_circle.take_correct_angle(rel_x_z_normal[0],rel_x_z_normal[1])

        # Value by which to increment angle
        angle_increment_value = 0.01 * direction_number

        # Quick calculation to update horizontal angle tracker
        h_angle = self.game.get_camera_angle_left_right()
        h_angle += angle_increment_value
        self.game.set_camera_angle_left_right(h_angle)


        # Increment the theta
        theta += angle_increment_value

        # Calculate new x-z normal
        new_x_normal = math.cos(theta)
        new_z_normal = math.sin(theta)
        rel_x_z_normal = [new_x_normal,new_z_normal]



        # Multiply normal with the magnitude
        rel_x_z = [rel_x_z_normal[0] * rel_x_z_magnitude, rel_x_z_normal[1] * rel_x_z_magnitude + game_constants.CAMERA_DIFF]

        # Calculate the new point
        new_point = [rel_x_z[0]+self.game.GAME_W/2,self.position[1],rel_x_z[1]]
        self.position[0] = new_point[0]
        self.position[1] = new_point[1]
        self.position[2] = new_point[2]


    def look_up_down(self,speed,direction_number):
        ## TODO - maybe change later to limit how much up and down can get rotated,
        # to prevent camera issue
        
        # Get Camera Position
        camera_x, camera_y, camera_z = self.game.get_camera()

        # Rotate each vertex around a 2D circle
        rotation_center = (self.position[0],self.game.GAME_H/2,0)

        # The y-z coordinates relative to center of rotation
        rel_y_z = (self.position[1] - rotation_center[1] ,self.position[2] - rotation_center[2] - game_constants.CAMERA_DIFF)

        # Distance between vector and rotation center
        rel_y_z_magnitude = math.sqrt(rel_y_z[0]**2 + rel_y_z[1]**2)
        if rel_y_z_magnitude == 0:
            rel_y_z_magnitude = 0.01

        # Calculate the corresponding normal vector
        rel_y_z_normal = [rel_y_z[0]/rel_y_z_magnitude,rel_y_z[1]/rel_y_z_magnitude]

        # Calculate angle of the vertex relative to rotation center by considering
        # whether y and z are positive or negative
        theta = unit_circle.take_correct_angle(rel_y_z_normal[0],rel_y_z_normal[1])

        # Value by which to increment angle
        angle_increment_value = 0.01 * direction_number

        # Quick calculation to update vertical angle tracker
        v_angle = self.game.get_camera_angle_up_down()
        v_angle += angle_increment_value
        self.game.set_camera_angle_up_down(v_angle)

        # Increment the theta
        theta += angle_increment_value

        # Calculate new y-z normal
        new_y_normal = math.cos(theta)
        new_z_normal = math.sin(theta)
        rel_y_z_normal = [new_y_normal,new_z_normal]

        # Multiply normal with the magnitude
        rel_y_z = [rel_y_z_normal[0] * rel_y_z_magnitude, rel_y_z_normal[1] * rel_y_z_magnitude + game_constants.CAMERA_DIFF]

        # Calculate the new point
        new_point = [self.position[0],rel_y_z[0] + self.game.GAME_H/2,rel_y_z[1]]
        self.position[0] = new_point[0]
        self.position[1] = new_point[1]
        self.position[2] = new_point[2]
        

    def move_up_down(self,speed,direction_number):
        # Move the vertex up or down
        self.position[1] += speed * direction_number




    def calculate_projected_position(self):
        screen_width = self.shape.game.GAME_W
        screen_height = self.shape.game.GAME_H
        depth_angle = self.shape.game.view_depth_angle
        point_3d = self.position

        camera_x, camera_y, camera_z = self.game.get_camera()

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



