import os, sys, time, pygame, math
from shape import Shape
from triangle import Triangle
from level import Level
import game_constants
class Game():
    def __init__(self):
        pygame.init()
        self.GAME_W = game_constants.GAME_WIDTH
        self.GAME_H = game_constants.GAME_HEIGHT
        self.game_canvas = pygame.Surface((self.GAME_W,self.GAME_H))
        self.screen = pygame.display.set_mode((self.GAME_W,self.GAME_H))
        self.running, self.playing = True, True
        self.actions = {"left":False,"right":False,"up":False,"down":False,"q":False,"e":False,"arrow_left":False,"arrow_right":False,"arrow_up":False,"arrow_down":False}
        self.dt, self.prev_time = 0,0

        self.view_depth_angle = (math.pi)/8  # DO NOT CHANGE THIS, CHANGING WOULD RUIN THE WHOLE ENGINE


        ##### Variables related to the camera ####
        self.camera = [0,0,0]
        self.camera_angle_left_right = 0
        self.camera_angle_up_down = 0
        self.movement_speed = 4
        self.rotation_speed = 0.00001

        self.level = Level(self,self.camera) 

    def game_loop(self):
        while self.playing:
            self.get_dt()
            self.get_events()
            self.update()
            self.render()

    def get_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    self.actions["left"] = True
                if event.key == pygame.K_d:
                    self.actions["right"] = True
                if event.key == pygame.K_w:
                    self.actions["up"] = True
                if event.key == pygame.K_s:
                    self.actions["down"] = True
                if event.key == pygame.K_q:
                    self.actions["q"] = True
                if event.key == pygame.K_e:
                    self.actions["e"] = True
                if event.key == pygame.K_LEFT:
                    self.actions["arrow_left"] = True
                if event.key == pygame.K_RIGHT:
                    self.actions["arrow_right"] = True
                if event.key == pygame.K_UP:
                    self.actions["arrow_up"] = True
                if event.key == pygame.K_DOWN:
                    self.actions["arrow_down"] = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    self.actions["left"] = False
                if event.key == pygame.K_d:
                    self.actions["right"] = False
                if event.key == pygame.K_w:
                    self.actions["up"] = False
                if event.key == pygame.K_s:
                    self.actions["down"] = False
                if event.key == pygame.K_q:
                    self.actions["q"] = False
                if event.key == pygame.K_e:
                    self.actions["e"] = False
                if event.key == pygame.K_LEFT:
                    self.actions["arrow_left"] = False
                if event.key == pygame.K_RIGHT:
                    self.actions["arrow_right"] = False
                if event.key == pygame.K_UP:
                    self.actions["arrow_up"] = False
                if event.key == pygame.K_DOWN:
                    self.actions["arrow_down"] = False
    
    def reset_keys(self):
        for action in self.actions:
            self.actions[action] = False


    def update(self):
        self.level.update(self.actions)

    def render(self):
        self.level.render(self.game_canvas)
        self.screen.blit(pygame.transform.scale(self.game_canvas, (self.GAME_W,self.GAME_H)),(0,0))
        pygame.display.flip()

    def get_dt(self):
        now = time.time()
        self.dt = now - self.prev_time
        self.prev_time = now

    def get_camera(self):
        return self.camera[0],self.camera[1],self.camera[2]

    def set_camera(self,x,y,z):
        self.camera[0] = x
        self.camera[1] = y
        self.camera[2] = z


    def get_movement_speed(self):
        return self.movement_speed
    
    def get_rotation_speed(self):
        return self.rotation_speed

    def get_camera_angle_left_right(self):
        return self.camera_angle_left_right

    def set_camera_angle_left_right(self,value):
        self.camera_angle_left_right = value

    def get_camera_angle_up_down(self):
        return self.camera_angle_up_down

    def set_camera_angle_up_down(self, value):
        self.camera_angle_up_down = value

game_object = Game()
while game_object.running:
    game_object.game_loop()

    