from game_manipulation.imports import *
class Game(Config):
    def __init__(self,screen_size,FPS, background_path, running,level,enemies_death_score=200):
        super().__init__(screen_size,FPS,background_path,running)
        self.original_background = background_path

        #Creación de listas y variables
        self.platforms_list = []
        self.invisible_platforms_list = []
        self.enemies_list = []
        self.traps_list = []
        self.coins_packs_list = []
        self.keys_packs_list = []
        self.heart = []
        self.power_up_batarang = []
        self.level = level
        self.enemies_death_score = enemies_death_score
        self.seconds = 0
        self.final_boss_appearance = False
        self.final_boss_death = False
        self.game_on = True
        self.back_to_menu = False
        self.next_level = False
        self.try_again = False
        self.third_level = False
        self.pause = True
        self.result = ""
        self.pause_time = 0
        self.pause_seconds = 1
        self.one_time_paused = False

        #Sets
        self.set_countdown()
        self.set_heroe()
        self.set_platforms()
        self.set_enemies()
        self.set_traps()
        self.set_items()        
        self.set_final_boss()
        self.set_falling_objects()
        self.set_roof()
        self.create_buttons()

    #Sets
    def set_platforms(self):
        pass

    def set_heroe(self):
       pass

    def set_enemies(self):
        pass

    def set_traps(self):
        pass

    def set_items(self):
        pass

    def set_final_boss(self):
        pass
    
    def set_falling_objects(self,amount=10):
        pass
    
    def set_enemies_death_score(self):
        self.heroe.update_score(self.enemies_death_score)
    
    def set_timer(self,seconds_passed):
        """inicializa un contador para la función 'create_loop_actions' y le resta el tiempo iniciado en el menú principal

        Args:
            seconds_passed (int): los segundos desde que empezó el juego (no el nivel)
        """
        self.current_time = int(py.time.get_ticks()/1000)
        self.current_time -= seconds_passed
    
    def set_countdown(self,level_time=45):
        """crea las características del contador regresivo

        Args:
            level_time (int, optional): el tiempo que va a tener el nivel
        """
        self.countdown = level_time
        self.countdown_text = f"{self.countdown}"
        self.countdown_position = (650,10)
        self.countdown_size = (50,50)
        self.countdown_rect = py.Rect(self.countdown_position,self.countdown_size)
        self.font = py.font.SysFont("PixelOperator",50)
        

    def set_roof(self):
        self.roof = Platform(self.screen,(self.screen_size[0],30),(0,0),r"assets\Imagenes\roof.png")
        self.platforms_list.append(self.roof)

    #Blits
    def blit_platforms(self,platforms_list):
        for platform in platforms_list:
            platform.blit_platform()
            
    def blit_items(self, items_packs_list):
        if len(items_packs_list) > 0:
            if type(items_packs_list[0]) != list:
                items_packs_list[0].animate()
            else:
                for pack_item in items_packs_list:
                    for item in pack_item:
                        item.animate()
        else:
            pass

    def blit_traps(self):
        if len(self.traps_list) > 0:
            for trap in self.traps_list:
                trap.animate()
        else:
            pass
    
    def blit_countdown(self):
        """crea el texto para el contador regresivo para que se muestre en la pantalla
        """
        self.countdown_surface = self.font.render(self.countdown_text,False,"white")
        self.countdown_surface = py.transform.scale(self.countdown_surface,(50,50))
        self.countdown_text = f"{self.countdown}"
        self.screen.blit(self.countdown_surface, (650,630))

    def blit_falling_objects(self):
        pass

    def blit_hitboxs(self):
        """muestra las hitbox de todos los objetos del nivel (heroe,enemigos,plataformas (visibles e invisibles),monedas y llaves)
        """
        self.heroe.show_hitbox("blue")
        py.draw.rect(self.screen, "white", self.heroe.rect_bottom,3)
        py.draw.rect(self.screen, "white", self.heroe.rect_top,3)
        for projectile in self.heroe.projectiles_list:
            projectile.show_hitbox("green")
        for enemy in self.enemies_list:
            enemy.show_hitbox("blue")
        for platform in self.platforms_list:
            py.draw.rect(self.screen, "red", platform.rect,3)
        for platform in self.invisible_platforms_list:
            py.draw.rect(self.screen, "white", platform.rect,3)
        for trap in self.traps_list:
            trap.show_hitbox("yellow")
        for coins_pack in self.coins_packs_list:
            for coin in coins_pack:
                coin.show_hitbox("green")
        for keys_pack in self.keys_packs_list:
            for key in keys_pack:
                key.show_hitbox("green")
        if self.final_boss_appearance:
            self.final_boss.show_hitbox("red")

    #Actions
    def enemies_actions(self):
        """anima a los enemigos, los remueve de la lista si no tienen vida y verifica la colision con el heroe
        """
        if len(self.enemies_list) > 0:
            for enemy in self.enemies_list:
                enemy.move(self.invisible_platforms_list)
                if enemy.check_death():
                    self.enemies_list.remove(enemy)
                    self.set_enemies_death_score()
            self.heroe.check_enemy_collision(self.enemies_list, self.platforms_list)
        else:
            pass

    def heroe_actions(self):
        """lo anima, verifica todas sus posibles colisiones (trampas,monedas,llaves,techo) y verifica su muerte
        """
        self.heroe.move(self.platforms_list, self.enemies_list)
        self.heroe.check_trap_collision(self.traps_list, self.platforms_list)
        self.heroe.check_item_collision(self.coins_packs_list)
        self.heroe.check_key_collision(self.keys_packs_list)
        self.heroe.check_roof_collision(self.roof)
        self.heroe.check_heart_collision(self.heart)
        self.heroe.check_power_up_collision(self.power_up_batarang)
        self.muerte_heroe = self.heroe.check_death(self.countdown)

    def final_boss_actions(self):
        """si el nivel contiene al jefe final lo anima,verifica la colisión del heroe con el mismo, la colision con los proyectiles del heroe, anima sus transformaciones y verifica su muerte
        """
        if self.final_boss_appearance:
            self.final_boss.blit_life()
            self.heroe.check_final_boss_collision(self.final_boss,self.platforms_list)
            self.final_boss.check_projectile_collision(self.heroe)
            self.final_boss.change_mode(self.falling_objects_list)
            if self.final_boss.drop_falling_objects:
                self.blit_falling_objects()
            self.final_boss_death = self.final_boss.check_death()
        else:
            pass
    
    #Creations
    def create_items(self,amount,x,y,dict=coin_dict):
        """crea los items que se van a mostrar en consecutivo (en fila)

        Args:
            amount (int): la cantidad de items que se quiere crear
            x (int): la posicion en x del item inicial
            y (int): la posicion en y del item inicial
            dict (dict, optional): el diccionario con las animaciones del item. Defaults to coin_dict.

        Returns:
            list: la lista con los items creados
        """
        items_list = []
        for i in range(amount):
            item = Item((30,30),(x,y),dict,self.screen)
            x += 50
            items_list.append(item)
        return items_list

    def create_loop_actions(self,events,seconds_passed,x_pos,y_pos,mouse_box_state,user_name):
        """realiza toda la lógica que se tenga que ejecutar en el loop: el manejo del tiempo, las animaciones, el modo programador y las diferentes pantallas de victoria o derrota.

        Args:
            events (list): la lista de eventos de pygame
            seconds_passed (int): los segundos desde que empezó el juego (no el nivel)
            x_pos (int): la posicion x del cursor al hacer click
            y_pos (int): la posicion y del cursor al hacer click
            mouse_box_state (bool): el estado de los botones del mouse
        """
        if self.pause:
            self.set_timer(seconds_passed)
        if self.running and self.game_on:
            self.blit_platforms(self.invisible_platforms_list)
            self.fill_screen()

            for event in events:
                if event.type == py.KEYDOWN:
                    if event.key == py.K_TAB:
                        change_mode()

            self.blit_traps()
            self.blit_platforms(self.platforms_list)
            self.blit_items(self.coins_packs_list)
            self.blit_items(self.keys_packs_list)
            self.blit_items(self.heart)
            self.blit_items(self.power_up_batarang)
            self.enemies_actions()
            self.final_boss_actions()
            self.heroe_actions()

            if get_mode():
                self.blit_hitboxs()

            #Tiempo     
            if self.pause:     
                if (self.current_time-self.pause_seconds) == self.seconds:
                    self.countdown -= 1
                    self.seconds += 1

            if self.countdown < 1 or self.heroe.death:
                self.countdown = 0
                self.set_music(r"assets\Musica\game_over.mp3")
                self.set_lose_screen()
                self.game_on = False
            self.blit_countdown()

            if self.heroe.keys_collected == 4 or self.final_boss_death:
                self.set_music(r"assets\Musica\i_m_batman.mp3")
                self.game_on = False
                self.set_win_screen(user_name)
            
            #Pausa
            if self.pause:
                self.pause_button.create_box()
                if self.pause_button.on_click(x_pos,y_pos,mouse_box_state):
                    self.set_pause_screen()
                    self.pause = False
                    self.game_on = False
                    self.one_time_paused = True
        
        #Lógica de si el jugador apretó el botón de pausa
        if not self.pause:
            self.pause_time = int(py.time.get_ticks()/1000)
            self.pause_time -= (seconds_passed + self.current_time)
            if self.pause_time == self.pause_seconds:
                self.pause_seconds += 1
            self.fill_screen()
            self.back_to_menu_button.create_box()
            self.continue_button.create_box()
            self.check_user_action(x_pos,y_pos,mouse_box_state)

        #Lógica de si el jugador pasó el nivel o no
        elif not self.game_on and self.pause:
            self.fill_screen()
            if self.result == "Victory":
                if not self.third_level:
                    self.next_level_button.create_box()
                else:
                    self.try_again_button.create_box()
                self.result_button.create_box()
            elif self.result == "Defeat":
                self.try_again_button.create_box()
                self.result_button.create_box()
            self.back_to_menu_button.position = (400,500)
            self.back_to_menu_button.create_box()
            self.score_box.create_box()
            self.check_user_action(x_pos,y_pos,mouse_box_state)
            if self.current_time == self.seconds:
                self.seconds += 1

    def set_win_screen(self,user_name):
        """Lo que se va a mostrar al ganar el nivel
        """
        self.set_background(r"assets\Imagenes\winning_screen.webp")
        self.result = "Victory"
        self.set_result_button(self.result,"green")
        self.set_score()
        self.users_data = self.load_file()
        self.current_player = self.set_user_data(user_name)
        self.users_data["players"].append(self.current_player)
        self.upload_score()
        self.update_database()

    def set_lose_screen(self):
        """lo que se va a mostrar al perder el nivel
        """
        self.set_background(r"assets\Imagenes\lose_screen.jpg")
        self.result = "Defeat"
        self.set_result_button(self.result,"red")
        self.set_score()
    
    def set_pause_screen(self):
        """lo que se va a mostrar al tocar el botón de pausa
        """
        self.set_background(r"assets\Imagenes\batman_coffee.jpg")
        self.back_to_menu_button.position = (300,100)
        self.back_to_menu_button.create_box()
        self.continue_button.create_box()
        if self.one_time_paused:
            self.pause_seconds = 0
            self.pause_time -= self.seconds
            self.one_time_paused = False
    
    def create_buttons(self):
        self.back_to_menu_button = Box(self.screen,(400,500),(200,100),r"assets\Imagenes\button_box.png","Back to menu","gray")
        self.next_level_button = Box(self.screen,(900,500),(200,100),r"assets\Imagenes\button_box.png","Next level","gray")
        self.try_again_button = Box(self.screen,(900,500),(200,100),r"assets\Imagenes\button_box.png","Try again","gray")
        self.pause_button = Box(self.screen,(10,10),(50,50),r"assets\Imagenes\pause_button.png")
        self.continue_button = Box(self.screen,(900,100),(200,100),r"assets\Imagenes\button_box.png","Continue","gray")
    
    def set_result_button(self,text,color):
        self.result_button = Box(self.screen,(600,20),(300,200),r"assets\Imagenes\bat_title_box.png",text,color)
    
    def check_user_action(self,x_pos,y_pos,mouse_box_state):
        """aplica la lógica del botón que elija el jugador

        Args:
            x_pos (int_): la posicion x del cursor al hacer click
            y_pos (int_): la posicion y del cursor al hacer click
            mouse_box_state (bool): el estado de los botones del mouse
        """
        if self.back_to_menu_button.on_click(x_pos,y_pos,mouse_box_state):
            self.running = False
            self.back_to_menu = True
        elif self.next_level_button.on_click(x_pos,y_pos,mouse_box_state) and self.result == "Victory" and not self.third_level:
            self.running = False
            self.next_level = True
        elif self.try_again_button.on_click(x_pos,y_pos,mouse_box_state):
            self.running = False
            self.try_again = True
        elif self.continue_button.on_click(x_pos,y_pos,mouse_box_state):
            self.game_on = True
            self.pause = True
            self.set_background(self.original_background)

    def set_score(self):
        if self.result == "Victory":
            self.user_score = (self.heroe.score_amount+(self.seconds*1000))*self.heroe.life_amount
            self.color = "green"
        else:
            self.user_score = 0
            self.color = "red"
        self.user_score_text = f"Your score: {self.user_score}"
        self.score_box = Box(self.screen,(10,300),(450,200),r"assets\Imagenes\bat_title_box.png",self.user_score_text,self.color,25)
    
    #Manejo de datos
    def upload_score(self):
        with open("data_manipulation\players.json","w") as file:
            json.dump(self.users_data,file,indent=2)

    def load_file(self):
        with open("data_manipulation\players.json","r") as file:
            data = json.load(file)
        return data
    
    def set_user_data(self,user_name):
        player = {}
        player["level"] = self.level
        player["user"] = user_name
        player["score"] = self.user_score
        return player
    
    def update_database(self):
        with sqlite3.connect("data_manipulation\players_database.db") as connection:
            statement = "insert into Players(level,user,score) values(?,?,?)"
            connection.execute(statement,(self.current_player["level"],self.current_player["user"],self.current_player["score"]))