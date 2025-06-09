from shape import Shape
import os
import csv
import unit_circle
import math

class Level():
    def __init__(self,game):
        self.game = game

        ## CAMERA
        self.camera = Camera(0,0,0,0,0)

        ## Shape
        self.shapes = []

        ## Lighting
        self.light_source_vector = [0,-0.707,-0.707]

        self.load_level_old()
        #self.load_level()



    def update(self,actions):
        # Update the camera
        self.camera.update(actions)
        
        # Update entities in the scene
        for shape in self.shapes:
            shape.update(actions)

        # Update the lighting
        #self.adjust_light_wrapper(actions)


        self.sort_shapes()
        

    def render(self,display):
        display.fill((20,20,70))
        for shape in self.shapes:
            shape.render(display)

    def get_light_source(self):
        return self.light_source_vector

    def set_light_source(self,x,y,z):
        self.light_source_vector[0] = x
        self.light_source_vector[1] = y
        self.light_source_vector[2] = z



    def helper_get_z_value(self,shape):
        return shape.get_center_z()


    def sort_shapes(self):
        self.shapes.sort(key=self.helper_get_z_value)
        self.shapes.reverse()

    def load_level_old(self):
        ## TODO - change to load object from text file or csv file
        # TEMP manually load shapes. Later, load shapes from text file.
        test_shape1 = Shape(self,self.game, self.camera, (250,200,1000),"donut.obj",5)
        self.shapes.append(test_shape1)

    def load_level(self):
        ## TODO - fix
        # Fix the level loading so it's not loading the same level
        path_to_csv = "level_data\\l1\\l1.csv"
        with open(path_to_csv) as data_file:
            file_reader = csv.reader(data_file,delimiter=',')
            for y_index, row in enumerate(file_reader):
                for x_index, cell in enumerate(row):
                    height = int(cell)
                    print(f"HEIGHT = {height}")
                    # Load the squares based on the height
                    for ii in range(height):
                        x_pos = x_index * 200
                        z_pos = y_index * 200
                        y_pos = ii * 200
                        pos = (x_pos,y_pos,z_pos)
                        new_shape = Shape(self,self.game,self.camera,pos,"funky_cube.obj",1)
                        self.shapes.append(new_shape)



class Camera():
    def __init__(self,x_pos,y_pos,z_pos,h_angle,v_angle):
        self.pos = [x_pos,y_pos,z_pos]
        self.h_angle = h_angle
        self.v_angle = v_angle
        self.movement_speed = 2
        self.rotation_speed = 0.02

    def update(self,actions):
        # TODO - update the camera position and angles based on the input
        if actions["left"]:
            self.pos[0] -= (self.movement_speed) * math.cos(self.h_angle)
            self.pos[2] += (self.movement_speed) * math.sin(self.h_angle) 
        if actions["right"]:
            self.pos[0] += (self.movement_speed) * math.cos(self.h_angle)
            self.pos[2] -= (self.movement_speed) * math.sin(self.h_angle)
        if actions["up"]:
            self.pos[2] += (self.movement_speed) * math.cos(self.h_angle)
            self.pos[0] += (self.movement_speed) * math.sin(self.h_angle)
        if actions["down"]:
            self.pos[2] -= (self.movement_speed) * math.cos(self.h_angle)
            self.pos[0] -= (self.movement_speed) * math.sin(self.h_angle) 
        if actions["q"]:
            self.pos[1] += self.movement_speed
        if actions["e"]:
            self.pos[1] -= self.movement_speed
        if actions["arrow_left"]:
            self.h_angle -= self.rotation_speed
        if actions["arrow_right"]:
            self.h_angle += self.rotation_speed
        if actions["arrow_up"]:
            self.v_angle += self.rotation_speed
        if actions["arrow_down"]:
            self.v_angle -= self.rotation_speed

        ## DEBUG - camera position
        #print(f"[*] DEBUG camera position: ({self.pos[0]},{self.pos[1]},{self.pos[2]})  h_angle: {self.h_angle}")

    def get_position(self):
        return self.pos

    def get_h_angle(self):
        return self.h_angle

    def get_v_angle(self):
        return self.v_angle

        

