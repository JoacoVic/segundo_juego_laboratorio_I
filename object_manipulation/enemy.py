from game_manipulation.imports import *

class Enemy(Object):

    def __init__(self,surface_size,enemy_dict,screen,position,speed=5,life_amount=3,key="Right"):
        super().__init__(surface_size,position,enemy_dict,screen,key)
        
        self.direction = self.set_direction()
        self.last_direction = self.set_last_direction()
        self.set_speed(speed)
        self.impact = False
        self.life_amount = life_amount
    
    def set_direction(self):
        """elige aleatoriamente la dirección del enemigo

        Returns:
            str: la dirección escogida
        """
        direction = random.choice(["Left","Right"])
        return direction

    def set_last_direction(self):
        """en base a la dirección que tenga el enemigo, se establece la dirección anterior como la opuesta

        Returns:
            str: la dirección opuesta a la dirección actual
        """
        if self.direction == "Left":
            last_direction = "Right"
        elif self.direction == "Right":
            last_direction = "Left"
        return last_direction

    def move(self,invisible_platforms_list):
        """anima al enemigo en base a su dirección y llama a la función 'check_edges' para verificar la colisión con las plataformas invisibles y los bordes de la pantalla

        Args:
            invisible_platforms_list (list): la lista con las plataformas invisibles
        """
        match self.direction:
            case "Right":
                self.current_animation = self.object_dict["Right"]
                self.move_right()
                self.last_direction = "Left"
            case "Left":
                self.current_animation = self.object_dict["Left"]
                self.move_left()
                self.last_direction = "Right"
            case "Impact":
                if self.impact:
                    if self.last_direction == "Left":
                        self.current_animation = self.object_dict["Impact"]
                    elif self.direction == "Right":
                        self.current_animation = self.object_dict["Impact_Left"]
                    self.impact = False
                else:
                    if self.last_direction == "Right":
                        self.direction = "Left"
                    elif self.last_direction == "Left":
                        self.direction = "Right"
       
        self.check_edges(invisible_platforms_list)
        self.animate()
        
    def check_edges(self, invisible_platforms_list):
        """verifica la colisión con las plataformas invisibles y los bordes de la pantalla


        Args:
            invisible_platforms_list (list): la lista con las plataformas invisibles
        """
        if self.rect.x >= self.screen.get_width() - self.rect.width:
            self.direction = "Left"
        elif self.rect.x <= 0:
             self.direction = "Right"
        for invisible_plat in invisible_platforms_list:
            if self.rect.colliderect(invisible_plat.rect) and self.direction == "Right":
                self.direction = "Left"
            elif self.rect.colliderect(invisible_plat.rect) and self.direction == "Left":
                self.direction = "Right"
                

    def check_death(self):
        """anima la muerte del enemigo si no tiene más vidas

        Returns:
            bool: retorna True si el enemigo no tiene más vidas. Caso contrario retorna False
        """
        validation = False
        if self.life_amount <= 0:
            self.current_animation = self.object_dict["Explosion"]
            self.animate()
            self.set_music(r"assets\Musica\explosion.wav")
            validation = True
        return validation