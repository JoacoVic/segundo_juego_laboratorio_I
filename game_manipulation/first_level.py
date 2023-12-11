from game_manipulation.imports import *

class FirstLevel(Game):
    def __init__(self,screen_size,FPS,background_path,running,level,enemies_death_score=200):
        super(). __init__(screen_size,FPS,background_path,running,level,enemies_death_score)
    
    def set_platforms(self):
        #Visibles
        floor = Platform(self.screen,(self.screen_size[0],70),(0,self.screen_size[1]-70),r"assets\Imagenes\piso_nivel_uno.png")
        plat_1 = Platform(self.screen,(500,50),(self.screen_size[0]-500,420),r"assets\Imagenes\plataforma_1.png")
        plat_2 = Platform(self.screen,(500,50),(250,320),r"assets\Imagenes\plataforma_1.png")
        plat_3 = Platform(self.screen,(200,50),(0,400),r"assets\Imagenes\plataforma_1.png")
        plat_4 = Platform(self.screen,(500,50),(self.screen_size[0]-500,150),r"assets\Imagenes\plataforma_1.png")
        self.platforms_list = [floor,plat_1,plat_2,plat_3,plat_4]

        #Invisibles
        inv_plat_1 = Platform(self.screen,(10,200),(self.screen_size[0]-500,450))
        inv_plat_2 = Platform(self.screen,(10,100),(250,180))
        inv_plat_3 = Platform(self.screen,(10,100),(730,180))
        self.invisible_platforms_list = [inv_plat_1,inv_plat_2,inv_plat_3]

    def set_heroe(self):
         self.heroe = Heroe((85,110),heroe_dict,self.screen,(20,560))

    def set_enemies(self):
        bat_1 = Enemy((85,110),bat_dict,self.screen,(1200,510),8)
        bat_2 = Enemy((85,110),bat_dict,self.screen,(600,180),8)
        bat_3 = Enemy((85,110),bat_dict,self.screen,(600,40),8)
        self.enemies_list = [bat_1,bat_2,bat_3]

    def set_traps(self):
        saw_1 = Trap((50,60),(650,585),saw_dict,self.screen)
        saw_2 = Trap((50,60),(500,285),saw_dict,self.screen)
        saw_3 = Trap((50,60),(250,285),saw_dict,self.screen)
        self.traps_list = [saw_1,saw_2,saw_3]
    
    def set_items(self):
        #Monedas
        coin_pack_1 = self.create_items(4,250,580)
        coin_pack_2 = self.create_items(8,850,580)
        coin_pack_3 = self.create_items(6,900,390)
        coin_pack_4 = self.create_items(7,870,120)
        coin_pack_5 = self.create_items(4,310,280)
        coin_pack_6 = self.create_items(3,70,370)
        self.coins_packs_list = [coin_pack_1,coin_pack_2,coin_pack_3,coin_pack_4,coin_pack_5,coin_pack_6]

        #Llaves
        key_1 = self.create_items(1,1250,580,key_dict)
        key_2 = self.create_items(1,1250,390,key_dict)
        key_3 = self.create_items(1,1250,120,key_dict)
        key_4 = self.create_items(1,30,370,key_dict)
        self.keys_packs_list = [key_1,key_2,key_3,key_4]