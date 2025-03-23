import pygame
import math
from vertex import Vertex
import vector_3D

class Triangle():
    def __init__(self,game,shape,point1,point2,point3,camera):
        self.game = game
        self.shape = shape

        self.p_1 = point1
        self.p_2 = point2
        self.p_3 = point3

        # TEMP Camera
        self.camera = camera

        self.rotation_speed = 0.005
        # Vertices in 3d space
        self.vertices = []
        self.vertices.append(Vertex(self.game,self,self.shape,point1))
        self.vertices.append(Vertex(self.game,self,self.shape,point2))
        self.vertices.append(Vertex(self.game,self,self.shape,point3))

        # Vertices projected on 2d surface
        self.projected_vertices = []
        self.set_projected_vertices()

        # Normal vector
        self.camera_to_triangle = self.calculate_camera_to_triangle()
        self.normal = self.calculate_normal()


        ## TEMP REMOVE LIGHT SOURCE
        self.light_source_vector = (0,0,1)

    def update(self,actions):
        ## TODO - when player moves, it changes the camera coordinates.
        # If that happens, maybe update every single triangle's position.
        # Have a new function to update the position of every triangle
        # and vertices, and maybe call that function here. 
        for vertex in self.vertices:
            vertex.update(actions)

        self.set_projected_vertices()

        # Update normal
        self.camera_to_triangle = self.calculate_camera_to_triangle()
        self.normal = self.calculate_normal()

    def render(self,display):
        #for vertex in self.vertices:
        #    vertex.render(display)
        #self.draw_lines(display)
        self.fill_triangle(display)

        



    def draw_lines(self,display):
        # If the z component of the normal less than 0, then draw
        # Normal less than 0 means we can see it
        if self.normal[2] < 0:
            # 0 -> 1
            pygame.draw.line(display,(200,200,200),self.projected_vertices[0],self.projected_vertices[1],1)
            # 1 -> 2
            pygame.draw.line(display,(200,200,200),self.projected_vertices[1],self.projected_vertices[2],1)
            # 2 -> 3
            pygame.draw.line(display,(200,200,200),self.projected_vertices[2],self.projected_vertices[0],1)

    def fill_triangle(self,display):
        ## TODO - edit this function to take into account the current camera position

        color = (255,255,255)

        # Compare the normal to the light source vector, and based on that, change the color
        # Both vectors unit vectors, so calculate how "related" by doing dot product.
        normal = vector_3D.dot_product(self.normal,self.light_source_vector)
        # Set the value to positive number
        if normal < 0:
            normal *= -1
        
        # Adapting the color variable based on whether the normal to the face in the
        # same direction as the light
        color  = (color[0] * normal,color[1]*normal,color[2]*normal)

        can_draw = True
        for projected_vertex_to_test in self.projected_vertices:
            # Test if the projected vertex x_value = 0 or projected verted y_value = 0,
            # since if a vertex is off screen the projected x_value and y_value get
            # set to 0
            if projected_vertex_to_test[0] == 0 and projected_vertex_to_test[1] == 0:
                can_draw = False

        if can_draw:
            pygame.draw.polygon(display,color,self.projected_vertices)

        
        



    def set_projected_vertices(self):
        self.projected_vertices.clear()
        for vertex in self.vertices:
            new_vertex_projected = vertex.calculate_projected_position()
            self.projected_vertices.append(new_vertex_projected)

    def calculate_camera_to_triangle(self):
        # Calculate normal
        normal = self.calculate_normal()

        # Get the unit vector from camera to current triangle center
        triangle_midpoint = self.calculate_triangle_midpoint()

        # Get line vector from camera to midpoint
        camera_to_triangle = self.calculate_unit_vector(self.get_line_vector(self.camera,triangle_midpoint))

        return camera_to_triangle

    def calculate_normal(self):
        # Setup initial points
        self.p_1 = self.vertices[0].get_position()
        self.p_2 = self.vertices[1].get_position()
        self.p_3 = self.vertices[2].get_position()

        # Get line vectors from points
        vec_1 = (self.p_2[0] - self.p_1[0],self.p_2[1]-self.p_1[1],self.p_2[2]-self.p_1[2])
        vec_2 = (self.p_3[0] - self.p_1[0],self.p_3[1]-self.p_1[1],self.p_3[2]-self.p_1[2])

        # Get magnitude and unit vectors
        vec_1_magnitude = math.sqrt(vec_1[0] ** 2 + vec_1[1] ** 2 + vec_1[2] ** 2)
        vec_2_magnitude = math.sqrt(vec_2[0] ** 2 + vec_2[1] ** 2 + vec_2[2] ** 2)
        vec_1_unit = (vec_1[0]/vec_1_magnitude,vec_1[1]/vec_1_magnitude,vec_1[2]/vec_1_magnitude)
        vec_2_unit = (vec_2[0]/vec_2_magnitude,vec_2[1]/vec_2_magnitude,vec_2[2]/vec_2_magnitude)

        # Normal
        normal = vector_3D.cross_product(vec_1_unit,vec_2_unit)

        return normal


    def calculate_triangle_midpoint(self):
        p_1 = self.vertices[0].get_position()
        p_2 = self.vertices[1].get_position()
        p_3 = self.vertices[2].get_position()

        x_mid = (p_1[0] + p_2[0] + p_3[0])/3
        y_mid = (p_1[1] + p_1[1] + p_2[1])/3
        z_mid = (p_1[2] + p_2[2] + p_3[2])/3

        return (x_mid,y_mid,z_mid)

    def calculate_vector_magnitude(self,vec):
        return math.sqrt(vec[0]**2 + vec[1]**2 + vec[2]**2)

    def calculate_unit_vector(self,vec):
        magnitude = self.calculate_vector_magnitude(vec)
        return (vec[0]/magnitude,vec[1]/magnitude,vec[2]/magnitude)

    def get_line_vector(self,vec1,vec2):
        return (vec2[0] - vec1[0], vec2[1] - vec1[1], vec2[2] - vec1[2])

    def get_vertices(self):
        return self.vertices[0].get_position(), self.vertices[1].get_position(), self.vertices[2].get_position()








