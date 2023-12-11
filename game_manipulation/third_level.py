from game_manipulation.imports import *

class ThirdLevel(Game):
    def __init__(self,screen_size,FPS,background_path,running,level,enemies_death_score=100):
        super(). __init__(screen_size,FPS,background_path,running,level,enemies_death_score)
        self.set_final_boss()
        self.set_countdown(60)
        self.set_falling_objects(25)
    
    def set_platforms(self):
        #Visibles
        floor = Platform(self.screen,(self.screen_size[0],70),(0,self.screen_size[1]-70),r"assets\Imagenes\piso_nivel_uno.png")
        plat_1 = Platform(self.screen,(250,50),(100,400),r"assets\Imagenes\plataforma_2.png")
        plat_2 = Platform(self.screen,(250,50),(1000,400),r"assets\Imagenes\plataforma_2.png")
        plat_3 = Platform(self.screen,(400,50),(500,200),r"assets\Imagenes\plataforma_2.png")
        self.platforms_list = [floor,plat_1,plat_2,plat_3]

        #Invisibles
        inv_plat_1 = Platform(self.screen,(10,50),(100,350))
        inv_plat_2 = Platform(self.screen,(10,50),(350,350))
        inv_plat_3 = Platform(self.screen,(10,50),(500,150))
        inv_plat_4 = Platform(self.screen,(10,50),(900,150))
        self.invisible_platforms_list = [inv_plat_1,inv_plat_2,inv_plat_3,inv_plat_4]
    
    def set_heroe(self):
        self.heroe = Heroe((85,110),heroe_dict,self.screen,(1200,545),last_direction="Left")
    
    def set_final_boss(self):
        self.final_boss = FinalBoss((100,140),clayface_dict,self.screen,(20,480))
        self.final_boss_appearance = True
        self.third_level = True
    
    def set_falling_objects(self,amount=10):
        self.falling_objects_list = FallingObject.create_list(amount,self.screen)
    
    def blit_falling_objects(self):
        """anima el falling object, verifica la colisión con el heroe, se elimina de la lista y/o se reutiliza cuando el jugador entra en la etapa final del nivel.
        """
        for falling_object in self.falling_objects_list:
            falling_object.move_down()
            falling_object.animate()
            if falling_object.rect.y > self.screen.get_height():
                self.falling_objects_list.remove(falling_object)
        self.heroe.check_falling_object_collision(self.falling_objects_list,self.platforms_list)
        self.reblit_falling_objects()

    def reblit_falling_objects(self):
        if len(self.falling_objects_list) == 0 and self.final_boss.life_amount <= 25:
            self.set_falling_objects(15)
    
    def set_enemies(self):
        bat_1 = Enemy((85,110),bat_dict,self.screen,(600,90))
        solomon_1 = Enemy((90,115),solomon_dict,self.screen,(200,290),2,5,"Left")
        self.enemies_list = [bat_1,solomon_1]
    
    def set_items(self):
        coin_pack_1 = self.create_items(5,1000,370)
        coin_pack_2 = self.create_items(8,500,170)
        self.coins_packs_list = [coin_pack_1,coin_pack_2]

        self.heart = self.create_items(1,100,370,heart_dict)
        self.power_up_batarang = self.create_items(1,140,370,powered_batarangs_dict)