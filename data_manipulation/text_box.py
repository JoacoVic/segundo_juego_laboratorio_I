import pygame
from pygame.locals import *
import unicodedata

FPS = 18
#si creo un att del self en un metodo, eso impacta sobre la clase actual, o lo crea a nivel de la jerarquia de clases? por ej self.slave
#solo lo crea en button o en widget

    
class TextBox():
    def __init__(self,screen,x,y,w,h,color_background,color_background_seleccionado,color_border, color_border_seleccionado, border_size ,font, font_size,font_color):
        try:
            pygame.font.init()
            self.font = pygame.font.SysFont(font, font_size)
            self._font_color = font_color
        except pygame.error as e:
            print(f"Error initializing font: {e}")
        self._screen = screen
        self._x = x
        self._y = y
        self._w = w
        self._h = h
        self._color_background = color_background
        self._color_border = color_border
        self.border_size = border_size
        self._color_background_default = color_background
        self._color_border_default = color_border
        self._color_background_seleccionado = color_background_seleccionado
        self._color_border_seleccionado = color_border_seleccionado
        self._text = ""
        # self._font = pygame.font.SysFont(font,font_size)
        self.is_selected = False
        self.render()
        
    def get_text(self):
        return self._text    
    
    def set_text(self,text):
        self._text = text
        self.render()   
    
    def render(self):
        image_text = self.font.render(self._text, True, self._font_color, self._color_background)

    
        self._slave = pygame.surface.Surface((self._w,self._h))#superficie que se adapte a la del boton
        self.slave_rect = self._slave.get_rect()
        
        self.slave_rect.x = self._x
        self.slave_rect.y = self._y
        
        self.slave_rect_collide = pygame.Rect(self.slave_rect)
        
        self._slave.fill(self._color_background)
        
        media_texto_horizontal = image_text.get_width() / 2
        media_texto_vertical = image_text.get_height() / 2

        media_horizontal = self._w / 2
        media_vertical = self._h / 2
        diferencia_horizontal = media_horizontal - media_texto_horizontal 
        diferencia_vertical = media_vertical - media_texto_vertical
        
        self._slave.blit(image_text,(diferencia_horizontal,diferencia_vertical))#podriamos sacar cuentas para centrar el texto, por el momento 10-10
        
    
    def update(self,lista_eventos):
        for evento in lista_eventos:
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if self.slave_rect_collide.collidepoint(evento.pos):#me hicieron click, esto no siempre va a funcionar
                    self._color_background = self._color_background_seleccionado
                    self._color_border = self._color_border_seleccionado
                    self.is_selected = True
                else:
                    self._color_background = self._color_background_default
                    self._color_border = self._color_border_default
                    self.is_selected = False
                self.render()
            elif self.is_selected and evento.type == pygame.KEYDOWN:
                caracter = evento.unicode
                if evento.key == pygame.K_BACKSPACE:
                   self._text = self._text[:-1]
                elif len(caracter) == 1 and unicodedata.category(caracter)[0] != 'C':
                    self._text += caracter
                self.render()
        self.draw()
    
    def draw(self):
        self._screen.blit(self._slave,self.slave_rect)
        pygame.draw.rect(self._screen, self._color_border, self.slave_rect, self.border_size)
