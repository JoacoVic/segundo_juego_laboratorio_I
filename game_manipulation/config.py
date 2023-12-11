from game_manipulation.imports import *
FPS = 60
class Config:
    def __init__(self,screen_size,FPS,background_path,running):
        py.mixer.init()
        self.running = running
        self.screen_size = screen_size
        self.screen = py.display.set_mode(self.screen_size)
        self.set_fps(FPS)
        self.clock = py.time.Clock()
        self.set_title("Batman: The UTN Version")
        self.set_icon(r"assets\Imagenes\icono_ventana.jpg")
        self.set_background(background_path)
        
    def set_title(self, title):
        py.display.set_caption(title)

    def set_icon(self, icon):
        screen_icon = py.image.load(icon)
        py.display.set_icon(screen_icon)
    
    def set_fps(self, FPS):
        self.FPS = FPS
    
    def set_music(self, music, amount=0,volume=0.2):
        music = py.mixer.Sound(music)
        self.set_volume(music,volume)
        self.start_music(music,amount)
        return music
    
    def set_volume(self,music,volume):
        music.set_volume(volume)
    
    def start_music(self,music,amount):
        music.play(amount)
    
    def stop_music(self,music):
        music.stop()
    
    def set_background(self, background):
        self.background = py.image.load(background)
        self.background = py.transform.scale(self.background, self.screen_size)

    def fill_screen(self,color=None):
        if color != None:
            self.screen.fill(color)
        else:
            self.screen.blit(self.background, (0, 0))
    
    def set_loop(self):
        pass
