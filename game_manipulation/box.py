from game_manipulation.imports import *

class Box():
    def __init__(self,surface,position,size,path_image,text="",text_color="black",font_size=30,font_type="comicsansms"):
        self.path_image = path_image
        self.text = text
        self.text_color = text_color
        self.font_type = font_type
        self.font_size = font_size
        self.surface = surface
        self.position = position
        self.size = size

    def on_click(self, x_pos,y_pos,mouse_button_state):
        """verifica si se hizo click dentro de la casilla.

        Args:
            x_pos (int): la posicion x del cursor al hacer click
            y_pos (int): la posicion y del cursor al hacer click
            mouse_button_state (bool): el estado de los botones del mouse

        Returns:
            bool: constantemente retorna False, y solo al hacerse click dentro de la casilla retorna True
        """
        validation = False
        x,y = self.position
        width,height = self.size
        if mouse_button_state[0]:
            if (x_pos >= x and x_pos <= (x+width)) and (y_pos >= y and y_pos <= (y+height)):
                validation = True
        return validation
    
    def create_box(self):
        box = py.image.load(self.path_image).convert_alpha()
        self.rect = py.Rect(self.position, self.size)
        box = py.transform.scale(box,self.size)
        self.surface.blit(box,self.rect)
        self.create_text()
    
    def create_text(self):
        font = py.font.SysFont(self.font_type,self.font_size)
        box_text = font.render(self.text,False,self.text_color)
        text_rect = box_text.get_rect(center = self.rect.center)
        self.surface.blit(box_text,text_rect)