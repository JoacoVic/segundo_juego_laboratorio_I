from game_manipulation.imports import *
from assets.colores import *


class LevelSelection(Config):
    def __init__(self,screen_size,FPS,background_path,running):
        super().__init__(screen_size,FPS,background_path,running)
        self.boxes_list = []
        self.set_boxes()
        self.level_selected = ""
        self.running = running
        self.seconds_passed = 1
        self.unlock_second_level = False
        self.unlock_third_level = False
        self.buttons_appearance = True
        self.score_list_boxes = []
        self.set_text_box()
        self.score_list_appearance = False
        self.set_score_list()
        self.textbox_title_show = True

    def set_text_box(self):
        self.text_box = TextBox(self.screen,220,530,200,100,NEGRO,NEGRO,MAGENTA,AZUL_MARINO,3,"Comic Sans MS",20,TURQUESA)
        self.textbox_title = Box(self.screen,(220,530),(200,100),r"assets\Imagenes\black.jpg","Insert your user name",MORADO,15)

    def set_first_level(self):
        self.first_level = FirstLevel(self.screen_size,self.FPS,r"assets\Imagenes\fondo_nivel_uno.jpg",True,1,200)
    
    def set_second_level(self):
        self.second_level = SecondLevel(self.screen_size,self.FPS,r"assets\Imagenes\fondo_nivel_uno.jpg",True,2,300)
    
    def set_third_level(self):
        self.third_level = ThirdLevel(self.screen_size,self.FPS,r"assets\Imagenes\fondo_nivel_uno.jpg",True,3,400)

    def set_boxes(self):
        self.game_title = Box(self.screen,(20,0),(600,200),r"assets\Imagenes\bat_title_box.png","Batman: the UTN version",GRIS,18)
        self.boxes_list.append(self.game_title)
        self.first_level_box = Box(self.screen,(220,200),(220,100),r"assets\Imagenes\button_box.png","First Level",AZUL_CLARO)
        self.boxes_list.append(self.first_level_box)
        self.second_level_box = Box(self.screen,(220,310),(220,100),r"assets\Imagenes\button_box.png","Second Level",AZUL_CLARO)
        self.boxes_list.append(self.second_level_box)
        self.third_level_box = Box(self.screen,(220,420),(220,100),r"assets\Imagenes\button_box.png","Third Level",AZUL_CLARO)
        self.boxes_list.append(self.third_level_box)
        self.score_list_box = Box(self.screen,(50,500),(100,100),r"assets\Imagenes\Menu_BTN.png")
        self.boxes_list.append(self.score_list_box)

    def initiate(self):
        """el bucle principal: opera el manejo de tiempo de todo el juego, maneja los niveles y cierra el juego.
        """
        py.init()
        self.initial_time = int(py.time.get_ticks()/1000)
        self.menu_music = self.set_music(r"assets\Musica\el_señor_de_la_noche.mp3",-1,0.2)
        while self.running:
            self.clock.tick(self.FPS)
            self.current_time = int(py.time.get_ticks()/1000)
            self.current_time -= self.initial_time
            self.x_pos,self.y_pos = py.mouse.get_pos()
            self.mouse_box_state = py.mouse.get_pressed()
            self.events = py.event.get()
            for event in self.events:
                if event.type == py.QUIT:
                    self.running = False
            self.fill_screen()
            if self.buttons_appearance:
                for box in self.boxes_list:
                    box.create_box()
            if self.score_list_appearance:
                self.blit_score_list()
            self.text_box.update(self.events)
            if self.textbox_title_show:
                self.textbox_title.create_box()
            self.check_box_selected()
            py.display.flip()
        py.quit()
    
    def check_box_selected(self):
        """verifica qué nivel elige el jugador y llama a la funcion 'start_level' para operar con cada uno
        """
        if self.first_level_box.on_click(self.x_pos,self.y_pos,self.mouse_box_state) and self.buttons_appearance:
            if self.text_box._text != "":
                self.level_selected = "first"
                self.set_first_level()
                self.buttons_appearance = False
                self.score_list_appearance = False
                self.stop_music(self.menu_music)
                self.levels_music = self.set_music(r"assets\Musica\powerful-victory-trailer-103656.mp3",-1,0.3)
                self.user_name = self.text_box.get_text()
            else:
                self.set_music(r"assets\Musica\wrong.mp3")
        elif self.second_level_box.on_click(self.x_pos,self.y_pos,self.mouse_box_state) and self.buttons_appearance:
            if self.unlock_second_level and self.text_box._text != "":
                self.level_selected = "second"
                self.set_second_level()
                self.buttons_appearance = False
                self.score_list_appearance = False
                self.stop_music(self.menu_music)
                self.levels_music = self.set_music(r"assets\Musica\powerful-victory-trailer-103656.mp3",-1,0.3)
                self.user_name = self.text_box.get_text()
            else:
                self.set_music(r"assets\Musica\wrong.mp3")
        elif self.third_level_box.on_click(self.x_pos,self.y_pos,self.mouse_box_state) and self.buttons_appearance:
            if self.unlock_third_level and self.text_box._text != "":
                self.level_selected = "third"
                self.set_third_level()
                self.buttons_appearance = False
                self.score_list_appearance = False
                self.stop_music(self.menu_music)
                self.levels_music = self.set_music(r"assets\Musica\powerful-victory-trailer-103656.mp3",-1,0.3)
                self.user_name = self.text_box.get_text()
            else:
                self.set_music(r"assets\Musica\wrong.mp3",volume=0.3)
        elif self.score_list_box.on_click(self.x_pos,self.y_pos,self.mouse_box_state) and self.buttons_appearance:
            self.score_list_appearance = True
            self.set_top_players()
        elif self.textbox_title.on_click(self.x_pos,self.y_pos,self.mouse_box_state):
            self.textbox_title_show = False
        self.start_level()
    
    def start_level(self):
        """establece el tiempo actual del bucle para luego poder pasarselo por parámetro a los niveles, y dependiendo el nivel que eligio el jugador (y si lo pasó o no), habilita el o los niveles correspondientes.
        """
        
        match self.level_selected:
            case "first":
                if self.first_level.running:
                    self.first_level.create_loop_actions(self.events,self.seconds_passed,self.x_pos,self.y_pos,self.mouse_box_state, self.user_name)
                else:
                    self.current_time += self.first_level.seconds
                    self.seconds_passed += self.first_level.seconds
                    if self.first_level.back_to_menu:
                        if self.first_level.result=="Victory":
                            self.unlock_second_level = True
                        self.buttons_appearance = True
                        self.stop_music(self.levels_music)
                        self.menu_music = self.set_music(r"assets\Musica\el_señor_de_la_noche.mp3",-1,0.2)
                        self.level_selected = ""
                    elif self.first_level.next_level:
                        self.unlock_second_level = True
                        self.level_selected = "second"
                        self.set_second_level()
                    elif self.first_level.try_again:
                        self.set_first_level()
            case "second":
                if self.second_level.running:
                    self.second_level.create_loop_actions(self.events,self.seconds_passed,self.x_pos,self.y_pos,self.mouse_box_state, self.user_name)
                else:
                    self.current_time += self.second_level.seconds
                    self.seconds_passed += self.second_level.seconds
                    if self.second_level.back_to_menu:
                        if self.second_level.result=="Victory":
                            self.unlock_third_level = True
                        self.buttons_appearance = True
                        self.level_selected = ""
                        self.stop_music(self.levels_music)
                        self.menu_music = self.set_music(r"assets\Musica\el_señor_de_la_noche.mp3",-1,0.2)
                    elif self.second_level.next_level:
                        self.unlock_third_level = True
                        self.level_selected = "third"
                        self.set_third_level()
                    elif self.second_level.try_again:
                        self.set_second_level()
            case "third":
                if self.third_level.running:
                    self.third_level.create_loop_actions(self.events,self.seconds_passed,self.x_pos,self.y_pos,self.mouse_box_state, self.user_name)
                else:
                    self.current_time += self.third_level.seconds
                    self.seconds_passed += self.third_level.seconds
                    if self.third_level.back_to_menu:
                        self.buttons_appearance = True
                        self.level_selected = ""
                        self.stop_music(self.levels_music)
                        self.menu_music = self.set_music(r"assets\Musica\el_señor_de_la_noche.mp3",-1,0.2)
                    if self.third_level.try_again:
                        self.set_third_level()
            case "":
                if self.current_time == self.seconds_passed:
                    self.seconds_passed += 1
    
    #Base de datos
    def bring_top_players(self, level_selected):
        top_players_list = []
        with sqlite3.connect("data_manipulation\players_database.db") as connection:
            statement = f"SELECT user,score FROM Players WHERE level = {level_selected} ORDER BY score DESC LIMIT 3"
            results = connection.execute(statement)
            for line in results:
                top_players_list.append(line)
        return top_players_list
    
    def set_score_list(self):
        self.level_1 = Box(self.screen,(600,100),(200,50),r"assets\Imagenes\Table.png","First level","white",20)
        self.score_list_boxes.append(self.level_1)
        self.level_2 = Box(self.screen,(850,100),(200,50),r"assets\Imagenes\Table.png","Second level","white",20)
        self.score_list_boxes.append(self.level_2)
        self.level_3 = Box(self.screen,(1100,100),(200,50),r"assets\Imagenes\Table.png","Third level","white",20)
        self.score_list_boxes.append(self.level_3)
    
    def set_top_players(self):
        level_1_top_players = self.bring_top_players(1)
        level_2_top_players = self.bring_top_players(2)
        level_3_top_players = self.bring_top_players(3)
        self.create_boxes_for_top_players(level_1_top_players,600,200)
        self.create_boxes_for_top_players(level_2_top_players,850,200)
        self.create_boxes_for_top_players(level_3_top_players,1100,200)
        
    def create_boxes_for_top_players(self,level_top_players_list,x,y):
        for top_player in level_top_players_list:
            box = Box(self.screen,(x,y),(220,120),r"assets\Imagenes\Table.png",f"{top_player[0]}: {top_player[1]}","white",20)
            self.score_list_boxes.append(box)
            y += 140       

    def blit_score_list(self):
        for box in self.score_list_boxes:
            box.create_box()
