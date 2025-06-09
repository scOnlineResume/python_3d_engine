import pygame
import math
from triangle import Triangle
import vector_3D


class Shape():
    def __init__(self,level,game, camera, coordinates,naam,scale):
        self.game = game
        self.level = level
        self.naam = naam
        self.triangle_coordinates = []
        self.triangles = []
        self.camera = camera
        self.center = coordinates
        self.load_shape(scale)



    def load_shape(self,scale):
        # Load the shape from the object files
        # From the object file, we can get data on the temp_triangle
        # and we can also get data on the different triangles
        # We should also change the self.center

        # The line before processing
        unprocessed_lines = []

        # Points would get stored in this array
        points = []

        # Triangle info gets stored in this array
        temp_triangle = []

        # Sorted triangle array
        self.triangle_coordinates.clear()
        
        # Save the different lines into the unprocessed lines array
        ## TODO - change to load shape based on user input
        path_to_shape_file = "objects" + f"\{self.naam}"
        with open(path_to_shape_file) as data_file: 
            for line in data_file:
                unprocessed_lines.append(line)

        # Populate the points array and temp_triangle array
        for element in unprocessed_lines:
            if element[0] == "v":
                new_element = element[1:] # Remove the 'v' at start
                new_element = new_element.split()
                for index,item in enumerate(new_element):
                    new_element[index] = float(item) * scale
                points.append(new_element)
            elif element[0] == "f":
                new_element = element[1:] # Remove the 'f' at start
                new_element = new_element.split()
                for index,item in enumerate(new_element):
                    new_element[index] = int(item)
                temp_triangle.append(new_element)

        # Now, we need to add the temp_triangle into the triangle.
        # The "temp_triangle" array contains each triangle, and each
        # element contains an array of 3 numbers. These three numbers
        # refer to indexes in the "points" array. Or rather, it refers
        # to the index + 1. So we need to subtract by 1 to get the correct
        # index.
        for ii in range(len(temp_triangle)):
            self.populate_triangle_coordinates_array(temp_triangle[ii],points)
        
        # Sort triangle array
        self.triangle_coordinates.sort(key=self.helper_return_z)
        self.triangle_coordinates.reverse()


        # Load the actual triangles
        for ii in range(len(self.triangle_coordinates)):
            self.load_triangle_from_point(self.triangle_coordinates[ii])

    def load_triangle_from_point(self,triangle):
        point0 = triangle[0]
        point1 = triangle[1]
        point2 = triangle[2]



        point0 = vector_3D.vector_addition(point0,self.center)
        point1 = vector_3D.vector_addition(point1,self.center)
        point2 = vector_3D.vector_addition(point2,self.center)

        self.triangles.append(Triangle(self.game, self.camera,self,point0,point1,point2))

    def populate_triangle_coordinates_array(self,triangle,point):
        point0_index = triangle[0] - 1
        point1_index = triangle[1] - 1
        point2_index = triangle[2] - 1

        point0 = point[point0_index]
        point1 = point[point1_index]
        point2 = point[point2_index]

        self.triangle_coordinates.append([point0,point1,point2])

    
    def update(self,actions):
        for shape in self.triangles:
            shape.update(actions)

        ## TODO - it's very inefficient to do this calculation on every
        # iteration of the update loop. Later, maybe change it to only
        # call the reset_triangles() functions maybe once every 1000 
        # iterations of the loop
        self.reset_triangles()



    def render(self,display):
        for shape in self.triangles:
            shape.render(display)


    def reset_triangles(self):
        # Reverse triangle coordinates
        self.triangles.sort(key=self.helper_return_z_2)
        self.triangles.reverse()

    def get_center_z(self):
        # NOTE - this function seems to get the z value of the center of the entire shape
        # Count the number of triangles in the shape
        number_of_vertices = len(self.triangles) * 3


        # Running total of "x", "y", and "z" values
        x_running = 0
        y_running = 0
        z_running = 0

        for triangle in self.triangles:
            v0, v1, v2 = triangle.get_vertices()

            x_running += v0[0] + v1[0] + v2[0]
            y_running += v0[1] + v1[1] + v2[1]
            z_running += v0[2] + v1[2] + v2[2]
        

        x_avg = x_running / number_of_vertices
        y_avg = y_running / number_of_vertices
        z_avg = z_running / number_of_vertices

        
        return z_avg


    def helper_return_z(self,v1):
        return (v1[0][2] + v1[1][2] + v1[2][2])/3

    def helper_return_z_2(self,triangle):
        # NOTE - this function seems to get the average z value for one triangle
        # Get the vertices of the current triangle
        v0, v1, v2 = triangle.get_camera_space_positions()

        # Return the average of the z values
        return (v0[2] + v1[2] + v2[2])/3



    