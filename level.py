from shape import Shape

class Level():
    def __init__(self,game,camera):
        self.game = game
        self.camera = camera
        self.shapes = []

        self.load_level()


    def update(self,actions):
        for shape in self.shapes:
            shape.update(actions)

        self.sort_shapes()
        

    def render(self,display):
        display.fill((0,0,0))
        for shape in self.shapes:
            shape.render(display)



    def helper_get_z_value(self,shape):
        return shape.get_center_z()


    def sort_shapes(self):
        self.shapes.sort(key=self.helper_get_z_value)
        self.shapes.reverse()

    def load_level(self):
        ## TODO - change to load object from text file or csv file
        # TEMP manually load shapes. Later, load shapes from text file.
        test_shape1 = Shape(self.game,self.camera, (350,250,600),"donut.obj")
        test_shape2 = Shape(self.game,self.camera, (300,200,2500),"funky_circle.obj")
        self.shapes.append(test_shape1)
        self.shapes.append(test_shape2)
