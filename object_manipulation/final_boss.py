from game_manipulation.imports import *

class FinalBoss(Object):
    def __init__(self,surface_size,final_boss_dict,screen,position):
        super().__init__(surface_size,position,final_boss_dict,screen)
        self.original_size = surface_size
        self.original_position = position

        #Vida
        self.life_amount = 50
        self.life_amount_text = f"{self.life_amount}"
        self.icon = py.image.load(r"assets\Imagenes\clayface_icono.png")
        self.icon_position = (1240,10)
        self.icon_size = (50,50)
        self.icon = py.transform.scale(self.icon,self.icon_size)
        self.icon_rect = self.icon.get_rect()
        self.life_counter_position = (1290,10)
        self.life_counter_size = (50,50)
        self.life_counter = py.Rect(self.life_counter_position,self.life_counter_size)
        self.font = py.font.SysFont("PixelOperator",30)

        #Banderas y variables
        self.ball_mode = True
        self.melted_mode = False
        self.edge_counter = 0
        self.impact = False
        self.direction = "Right"
        self.set_speed(15)
        self.drop_falling_objects = False

    def check_edges(self):
        """verifica que no se vaya de los bordes de la pantalla
        """
        if self.rect.x >= self.screen.get_width() - self.rect.width:
            self.direction = "Left"
            self.edge_counter += 1
        elif self.rect.x <= 0:
             self.direction = "Right"
             self.edge_counter += 1

    def check_death(self):
        """verifica si no tiene más vidas

        Returns:
            bool: si se quedó sin vidas, retorna True. Caso contrario retorna False
        """
        validation = False
        if self.life_amount <= 0:
            self.current_animation = self.object_dict["Explosion"]
            self.animate()
            self.set_music(r"assets\Musica\explosion.wav")
            validation = True
        return validation
    
    def blit_life(self):
        self.lives = self.font.render(self.life_amount_text,True,"Red")
        self.lives = py.transform.scale(self.lives,self.life_counter_size)
        self.screen.blit(self.icon, self.icon_position)
        self.screen.blit(self.lives, self.life_counter_position)
    
    def check_projectile_collision(self,heroe):
        """verifica la colisión con los proyectiles del heroe para ir restándole vidas

        Args:
            heroe (class): el heroe
        """
        for projectile in heroe.projectiles_list:
            if self.rect.colliderect(projectile.rect):
                self.set_music(r"assets\Musica\impacto.wav", 0.5)
                self.impact = True
                if heroe.powered_up:
                    self.life_amount -= 2
                    heroe.update_score(200)
                else:
                    self.life_amount -= 1
                    heroe.update_score(100)
                self.life_amount_text = f"{self.life_amount}"
                heroe.projectiles_list.remove(projectile)
                heroe.shoot = True

    def animate(self,speed_transition=0.20):
        """anima al jefe final dependiendo su estado

        Args:
            speed_transition (float, optional): la velocidad de transición de las imágenes para animarlo. Defaults to 0.20.
        """
        if self.impact:
            self.current_animation = self.object_dict["Impact"]
            super().animate(0.01)
            self.impact = False
        else:
            self.current_animation = self.object_dict["Idle"]
            super().animate(speed_transition)
    
    def change_mode(self,falling_objects_list):
        """elige el modo en el que se va a transformar el jefe final dependiendo su cantidad de vidas

        Args:
            falling_objects_list (list): la lista con los falling objects
        """
        if self.life_amount <= 45 and self.ball_mode:
            if self.edge_counter < 6:
                self.ball_transformation()
                self.melted_mode = True
            else:
                self.ball_mode = False
        elif self.life_amount <= 35 and self.melted_mode:
            self.melted_transformation()
            self.drop_falling_objects = True
            if len(falling_objects_list) == 0 and not self.ball_mode:
                self.melted_mode = False
        elif self.life_amount <= 25:
            self.ball_mode = True
            self.edge_counter = -100
            self.melted_mode = True
        else:
            self.rect.x,self.rect.y = self.original_position
            self.rect.width,self.rect.height = self.original_size
            self.rescale_images()
            self.animate(0.10)

    def ball_transformation(self):
        """transforma al jefe final en una bola que se mueve de derecha a izquierda
        """
        if self.direction == "Right":
            self.current_animation = self.object_dict["Ball_movement"]
            self.move_right()
        elif self.direction == "Left":
            self.current_animation = self.object_dict["Ball_movement_left"]
            self.move_left()
        self.check_edges()
        super().animate()

    def melted_transformation(self):
        """derrite al jefe final para que pueda lanzar falling objects
        """
        if not self.ball_mode:
            self.rect.x,self.rect.y = 520,60
            super().animate()
