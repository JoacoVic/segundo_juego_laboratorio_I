from game_manipulation.imports import *

py.init()
class Heroe(Object):
    def __init__(self,surface_size,heroe_dict,screen,position,speed=6,last_direction="Right"):
        super().__init__(surface_size,position,heroe_dict,screen)
        #Movimiento
        self.movement = True
        self.last_direction = last_direction
        self.projectile_direction ="Right"
        self.impact = False
        self.death = False
        self.update_rects()
        
        #Salto
        self.jump_power = -19
        self.speed_jump_limit = 19
        self.gravity = 1
        self.jumping = False
        self.roof_collision = False

        self.key_pressed = []
        self.set_speed(speed)

        #Disparo
        self.shoot = True
        self.last_time_shoot = 0
        self.projectiles_list = []
        self.powered_up = False

        #Vida
        self.life_amount = 5
        self.life_amount_text = f"{self.life_amount}"
        self.icon = py.image.load(r"assets\Imagenes\batman_icono.png")
        self.icon_position = (1110,630)
        self.icon_size = (60,50)
        self.icon = py.transform.scale(self.icon,self.icon_size)
        self.icon_rect = self.icon.get_rect()
        self.life_counter_position = (1180,630)
        self.life_counter_size = (50,50)
        self.life_counter = py.Rect(self.life_counter_position,self.life_counter_size)
        self.font = py.font.SysFont("Arial",30)

        #Puntaje
        self.score_amount = int("000")
        self.score_amount_text = f"{self.score_amount}"
        self.score_amount_position = (1240,630)
        self.score_amount_size = (100,50)
        self.score_amount_rect = py.Rect(self.score_amount_position,self.score_amount_size)
        self.font = py.font.SysFont("Arial",30)
        self.keys_collected = 0
        self.final_boss_collision = False
        
    def update_rects(self):
        """actualiza las rectas del top y del bottom del personaje
        """
        self.rect_bottom = py.Rect(self.rect.x,(self.rect.y+self.rect.height-11),self.rect.width,11)
        self.rect_top = py.Rect(self.rect.x,(self.rect.y),self.rect.width,5)

    def press_key(self):
        self.key_pressed = py.key.get_pressed()
    
    def check_direction(self):
        """verifica la direción a la que tiene que ir el heroe
        """
        self.press_key()
        if self.key_pressed[py.K_RIGHT]:
            self.direction = "Right"
        elif self.key_pressed[py.K_LEFT]:
            self.direction = "Left"
        elif self.key_pressed[py.K_UP]:
            self.direction = "Jump"
        else:
            self.direction = "Idle"
        self.shoot_projectile()

    def move(self,platforms,enemies_list):
        """anima al heroe dependiendo de su dirección, le aplica la gravedad en el caso de que esté saltando, y actualiza todo lo necesario (proyectiles,rectas,colisión con bordes, la vida y el puntaje)

        Args:
            platforms (list): la lista de plataformas
            enemies_list (list): la lista de enemigos
        """
        if self.movement:
            self.check_direction()
            match self.direction:
                case "Right":
                    if not self.jumping:
                        self.current_animation = self.object_dict["Right"]
                    self.last_direction = "Right"
                    self.move_right()
                case "Left":
                    if not self.jumping:
                        self.current_animation = self.object_dict["Left"]
                    self.last_direction = "Left"
                    self.move_left()
                case "Idle":
                    if not self.jumping:
                        if self.last_direction == "Right":
                            self.current_animation = self.object_dict["Idle"]
                        else:
                            self.current_animation = self.object_dict["Idle_left"]
                case "Jump":
                    if not self.jumping:
                        self.set_music(r"assets\Musica\salto.wav")
                        self.jumping = True
                        self.jump_power = -19
                        self.speed_jump_limit = 19
                        if self.last_direction == "Right":
                            self.current_animation  = self.object_dict["Jump_right"]
                        else:
                            self.current_animation  = self.object_dict["Jump_left"]
        self.update_rects()
        self.update_projectiles(enemies_list)
        self.check_edges()
        self.activate_gravity(platforms)
        self.animate()
        self.show_life_and_score()

        
    def activate_gravity(self, platforms):
        """aplica la lógica de la gravedad y la colisión con las plataformas para que deje de saltar (dependiendo si saltó por decisión del jugador o si recibió algún impacto)

        Args:
            platforms (list): la lista de plataformas
        """
        if self.jumping:
            self.rect.y += self.jump_power
            if self.jump_power + self.gravity < self.speed_jump_limit:
                self.jump_power += self.gravity
            self.update_rects()
        
        for platform in platforms:
            if self.rect_bottom.colliderect(platform.rect):
                if self.impact:
                    if platform == platforms[0]:
                        self.rect.bottom = platform.rect.top
                        self.update_rects()
                        self.impact = False
                        self.movement = True
                        break
                    else:
                        pass
                elif not self.impact:
                    self.movement = True
                    self.jump_power = 0
                    self.jumping = False
                    self.rect.bottom = platform.rect.top
                    self.update_rects()
                    break
            else:
                self.jumping = True

    def check_roof_collision(self,roof):
        """verifica la colisión con el techo

        Args:
            roof (class): el techo
        """
        if self.rect_top.colliderect(roof.rect):
            self.roof_collision = True
            if self.roof_collision:
                self.rect.y += self.speed_jump_limit
        else:
            self.gravity = 1
            self.roof_collision = False
        
    def check_edges(self):
        """verifica la colisión con los bordes, y dependiendo cuál, llama a la función 'check_left_bridge' o check_right_edge'
        """
        if self.direction == "Left":
            self.check_left_edge()
        elif self.direction == "Right":
            self.check_right_edge()

    def check_left_edge(self):
        """verifica la colisión con el borde izquierdo
        """
        if self.rect.x <= 0:
            self.rect.x += self.speed
            self.update_rects()
            
    def check_right_edge(self):
        """verifica la colisión con el borde derecho
        """
        if self.rect.x >= self.screen.get_width() - self.rect.width:
            self.rect.x -= self.speed
            self.update_rects()
    
    def check_enemy_collision(self,enemies_list, platforms):
        """verifica la colisión con los enemigos, para restarle vida y hacer la animación del impacto

        Args:
            enemies_list (list): la lista de enemigos
            platforms (list): la lista de plataformas
        """
        for enemy in enemies_list:
            if self.rect.colliderect(enemy.rect) and self.movement:
                self.movement = False
                self.set_music(r"assets\Musica\grito_impacto.wav")
                self.life_amount -= 1
                self.life_amount_text = f"{self.life_amount}"
                if self.last_direction == "Right":
                    self.current_animation = self.object_dict["Crash_right"]
                else:
                    self.current_animation = self.object_dict["Crash_left"]
                self.impact = True
                self.jump_power = -20
                self.speed_jump_limit = 20
                self.gravity = 0.5
                self.update_rects()
                self.activate_gravity(platforms)
                break 
            self.gravity = 1

    def check_trap_collision(self,traps_list, platforms):
        """verifica la colisión con las trampas, para restarle vida y hacer la animación del impacto 

        Args:
            traps_list (list): la lista con las trampas
            platforms (list): la lista con las plataformas
        """
        for trap in traps_list:
            if self.rect_bottom.colliderect(trap.rect) and self.movement:
                self.movement = False
                self.life_amount -= 1
                self.set_music(r"assets\Musica\grito_impacto.wav")
                self.life_amount_text = f"{self.life_amount}"
                if self.last_direction == "Right":
                    self.current_animation = self.object_dict["Crash_right"]
                    self.rect.x -= 150
                else:
                    self.current_animation = self.object_dict["Crash_left"]
                    self.rect.x += 150
                
                self.jump_power = -12
                self.speed_jump_limit = 12
                self.update_rects()
                self.activate_gravity(platforms)

    def check_item_collision(self,items_packs_list):
        """verifica la colisión con los items que se le pasan por parámetro, para modificarle el puntaje y removerlos de la lista para que dejen de aparecer

        Args:
            items_packs_list (list): la lista con los packs de los items
        """
        for item_pack in items_packs_list:
            for item in item_pack:
                if self.rect_bottom.colliderect(item) and self.movement:
                    item_pack.remove(item)
                    self.update_score(100)
                    self.set_music(r"assets\Musica\coin_collected.mp3")

    def check_key_collision(self,keys_packs_list):
        """verifica la colision con las llaves, para poder determinar si se completó el nivel o no

        Args:
            keys_packs_list (list): la lista con las llaves
        """
        self.check_item_collision(keys_packs_list)
        for key_pack in keys_packs_list:
            if len(key_pack) == 0:
                keys_packs_list.remove(key_pack)
                self.keys_collected += 1

    def check_heart_collision(self,heart):
        if len(heart) > 0:
            if self.rect.colliderect(heart[0]) and self.movement:
                self.set_music(r"assets\Musica\health_restore_2.mp3")
                match self.life_amount:
                    case 5|0:
                        self.life_amount += 0
                    case 4:
                        self.life_amount += 1
                    case _:
                        self.life_amount += 2
                heart.remove(heart[0])
                self.life_amount_text = f"{self.life_amount}"
        else:
            pass
    
    def check_power_up_collision(self,powered_up_logo):
        if len(powered_up_logo) > 0:
            if self.rect.colliderect(powered_up_logo[0]) and self.movement:
                self.set_music(r"assets\Musica\batarang_recharge.mp3")
                self.powered_up = True
                powered_up_logo.remove(powered_up_logo[0])

    def check_final_boss_collision(self,final_boss, platforms):
        """verifica la colisión con el jefe final

        Args:
            final_boss (class): el jefe final
            platforms (list): la lista con las plataformas
        """
        if self.rect.colliderect(final_boss.rect) and self.movement:
            self.movement = False
            self.life_amount -= 1
            self.set_music(r"assets\Musica\grito_impacto.wav")
            self.life_amount_text = f"{self.life_amount}"
            if self.last_direction == "Right":
                self.current_animation = self.object_dict["Crash_right"]
            else:
                self.current_animation = self.object_dict["Crash_left"]
            self.impact = True
            self.jump_power = -20
            self.speed_jump_limit = 20
            self.gravity = 0.5
            self.update_rects()
            self.activate_gravity(platforms)
            self.gravity = 1
    
    def check_falling_object_collision(self, falling_objects_list, platforms):
        """verifica la colisión con los falling objects, para removerlos de la lista y realizar la animación de impacto del heroe

        Args:
            falling_objects_list (list): la lista con los falling objects
            platforms (list): la lista con las plataformas
        """
        for falling_object in falling_objects_list:
            if self.rect.colliderect(falling_object.rect) and self.movement:
                falling_objects_list.remove(falling_object)
                self.movement = False
                self.life_amount -= 1
                self.set_music(r"assets\Musica\grito_impacto.wav")
                self.life_amount_text = f"{self.life_amount}"
                if self.last_direction == "Right":
                    self.current_animation = self.object_dict["Crash_right"]
                else:
                    self.current_animation = self.object_dict["Crash_left"]
                self.impact = True
                self.jump_power = -20
                self.speed_jump_limit = 20
                self.gravity = 0.5
                self.update_rects()
                self.activate_gravity(platforms)
                break
            self.gravity = 1


    def shoot_projectile(self):
        """verifica si el jugador apretó la tecla de espacio y si se debe agregar el proyectil a la lista de proyectiles
        """
        self.press_key()
        if self.shoot and self.key_pressed[py.K_SPACE]:
            current_time = py.time.get_ticks()
            if current_time - self.last_time_shoot >= 500:
                self.add_projectile()
                self.set_music(r"assets\Musica\lanzamiento_bat.wav")
                self.shoot = False
                self.last_time_shoot = current_time

    def add_projectile(self):
        """verifica la dirección del proyectil y lo añade a la lista para que pueda animarse
        """
        x = None
        margin = 47

        y = self.rect.centery
        if self.last_direction == "Right" and self.shoot:
            x = self.rect.right - margin
            self.projectile_direction = "Right"
        elif self.last_direction == "Left" and self.shoot:
            x = self.rect.left - 100 + margin
            self.projectile_direction = "Left"
        
        if x is not None:
            if self.powered_up:
                batarang_dict = projectile_powered_up_dict
            else:
                batarang_dict = projectile_dict
            self.projectiles_list.append(Projectile((30,20),(x,y),batarang_dict,self.screen))
            
    
    def update_projectiles(self, enemies_list):
        """actualiza los proyectiles para verificar si colisionaron con algún enemigo o si salieron de los márgenes de la pantalla

        Args:
            enemies_list (list): la lista con los enemigos
        """
        if len(self.projectiles_list) > 0:
            p = self.projectiles_list[0]
            p.animate()
            p.update(self.projectile_direction)
            if p.check_edges() or p.check_enemy_collision(enemies_list):
                self.projectiles_list.remove(p)
                self.shoot = True
        else:
            pass
    
    def show_life_and_score(self):
        """muestra la vida y el puntaje del heroe en pantalla
        """
        self.lives = self.font.render(self.life_amount_text,False,"green")
        self.lives = py.transform.scale(self.lives,self.life_counter_size)
        self.screen.blit(self.icon, self.icon_position)
        self.screen.blit(self.lives, self.life_counter_position)

        self.score = self.font.render(self.score_amount_text,False,"yellow")
        self.score = py.transform.scale(self.score,self.score_amount_size)
        self.screen.blit(self.score, self.score_amount_position)
    
    
    def update_score(self,amount):
        """actualiza el puntaje del heroe dependiendo si recolectó un item o eliminó a un enemigo

        Args:
            amount (int): la cantidad de puntaje que se le debe sumar
        """
        self.score_amount += amount
        self.score_amount_text = f"{self.score_amount}"
    
    
    def check_death(self,countdown):
        """verifica si el heroe ya no tiene más vidas o si se le acabó el tiempo al jugador

        Args:
            countdown (int): el contador regresivo del nivel

        Returns:
            bool: retorna True si el heroe no tiene más vidas o el tiempo del nivel es menor a 1. Caso contrario retorna False
        """
        validation = False
        if self.life_amount < 1 or countdown < 1:
            self.life_amount = 0
            self.rect.width,self.rect.height = 120,50
            if not self.death:
                self.set_music(r"assets\Musica\grito_impacto.wav")
                self.death = True
            self.movement = False
            validation = True
        return validation
    
