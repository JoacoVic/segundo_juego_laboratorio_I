from game_manipulation.imports import *

class FallingObject(Object):
    def __init__(self,surface_size, position,falling_object_dict, screen, key="Falling"):
        super().__init__(surface_size, position,falling_object_dict, screen,key)

        self.set_speed()
        self.set_random_position()
    
    def set_speed(self):
        """setea una velocidad aleatoria para el falling object
        """
        speed = random.randrange(3,5)
        super().set_speed(speed)
    
    def set_random_position(self):
        """establece una posición aleatoria (dentro de los limites del ancho de la pantalla) para cada falling object
        """
        self.rect.x = random.randrange(10,self.screen.get_width()-self.rect.width)
        self.rect.y = random.randrange(-100,-40)

    @staticmethod
    def create_list(amount, screen):
        """método estático: crea la lista de falling objects con la cantidad que se le pasa por parámetro

        Args:
            amount (int): la cantidad de falling objects que se quiere crear
            screen (surface.Surface): la pantalla donde se van a mostrar

        Returns:
            list: la lista con los falling objects
        """
        list = []
        for i in range(amount):
            falling_object = FallingObject((50,50),(0,0),block_dict,screen)
            list.append(falling_object)
        return list