from game_manipulation.imports import *

class SecondLevel(Game):
    def __init__(self,screen_size,FPS, background_path,running,level,death_score_enemies=300):
        super(). __init__(screen_size,FPS, background_path,running,level,death_score_enemies)
    
    def set_platforms(self):
        #Visibles
        floor = Platform(self.screen,(self.screen_size[0],70),(0,self.screen_size[1]-70),r"assets\Imagenes\piso_nivel_uno.png")
        plat_1 = Platform(self.screen,(200,50),(0,360),r"assets\Imagenes\plataforma_2.png")
        plat_2 = Platform(self.screen,(500,50),(350,360),r"assets\Imagenes\plataforma_2.png")
        plat_3 = Platform(self.screen,(350,50),(self.screen_size[0]-350,300),r"assets\Imagenes\plataforma_2.png")
        self.platforms_list = [floor,plat_1,plat_2,plat_3]
        

        #Invisibles
        inv_plat_1 = Platform(self.screen,(10,100),(self.screen_size[0]-350,200))
        self.invisible_platforms_list.append(inv_plat_1)
    
    def set_heroe(self):
        self.heroe = Heroe((85,110),heroe_dict,self.screen,(20,310))
    
    def set_enemies(self):
        solomon_1 = Enemy((90,115),solomon_dict,self.screen,(1300,505),3,5)
        solomon_2 = Enemy((90,115),solomon_dict,self.screen,(200,505),4,5)
        solomon_3 = Enemy((90,115),solomon_dict,self.screen,(700,505),3,5)
        solomon_4 = Enemy((90,115),solomon_dict,self.screen,(400,505),4,5)
        solomon_5 = Enemy((90,115),solomon_dict,self.screen,(1000,505),3,5)
        solomon_6 = Enemy((90,115),solomon_dict,self.screen,(1300,185),5,5)
        self.enemies_list = [solomon_1,solomon_2,solomon_3,solomon_4,solomon_5,solomon_6]
    
    def set_traps(self):
        fire_1 = Trap((50,60),(500,300),fire_dict,self.screen)
        fire_2 = Trap((50,60),(700,300),fire_dict,self.screen)
        self.traps_list = [fire_1,fire_2]
    
    def set_items(self):
        #Monedas
        coins_pack_1 = self.create_items(3,350,330)
        coins_pack_2 = self.create_items(2,580,330)
        coins_pack_3 = self.create_items(1,770,330)
        self.coins_packs_list = [coins_pack_1,coins_pack_2,coins_pack_3]

        #Llaves
        key_1 = self.create_items(1,1300,270,key_dict)
        key_2 = self.create_items(1,820,330,key_dict)
        key_3 = self.create_items(1,10,590,key_dict)
        key_4 = self.create_items(1,1300,590,key_dict)
        self.keys_packs_list = [key_1,key_2,key_3,key_4]
        
        #Corazon
        self.heart = self.create_items(1,50,590,heart_dict)

        #Batarang_potenciado
        self.power_up_batarang = self.create_items(1,90,590,powered_batarangs_dict)

