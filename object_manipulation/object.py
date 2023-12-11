import pygame as py

class Object:
    def __init__(self, surface_size,position,object_dict,screen,key="Idle"):
        #Variables
        self.object_dict = object_dict
        self.screen = screen
        self.initial_position = position
        self.images_counter = 0
        self.direction = key
        self.current_animation = self.object_dict[key]

        #Rectángulo
        self.rect = self.object_dict[key][0].get_rect()
        self.rect.x, self.rect.y = position
        self.rect.width,self.rect.height = surface_size

        self.set_speed()
        self.rescale_images()
    
    def rescale_images(self):
        for key in self.object_dict:
            for i in range(len(self.object_dict[key])):
                img = self.object_dict[key][i]
                self.object_dict[key][i] = py.transform.scale(img,(self.rect.width,self.rect.height))

    def animate(self, speed_transition=0.20):
        lenght = len(self.current_animation)
        if self.images_counter >= lenght:
            self.images_counter = 0
        self.screen.blit(self.current_animation[int(self.images_counter)], self.rect)
        self.images_counter += speed_transition

    def set_speed(self,speed=0):
        self.speed = speed

    def move_direction(self, direction_lambda):
        self.rect.x, self.rect.y = direction_lambda(self.rect.x, self.rect.y, self.speed)

    def move_right(self):
        self.move_direction(lambda x, y, speed: (x + speed, y))

    def move_left(self):
        self.move_direction(lambda x, y, speed: (x - speed, y))

    def move_up(self):
        self.move_direction(lambda x, y, speed: (x, y - speed))

    def move_down(self):
        self.move_direction(lambda x, y, speed: (x, y + speed))

    def check_edges(self):
        pass
    
    def show_hitbox(self, color,margin=3):
        self.rect = py.draw.rect(self.screen,color,self.rect,margin)
    
    def move(self, platforms=None):
        pass

    def set_music(self,music,volume=0.4):
        self.music = py.mixer.Sound(music)
        self.set_volume(volume)
        self.start_music()
    
    def set_volume(self,volume):
        self.music.set_volume(volume)
    
    def start_music(self):
        self.music.play()
    
    def stop_music(self):
        self.music.stop()