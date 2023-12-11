from game_manipulation.imports import *

class Item(Object):
    def __init__(self,surface_size,position,item_dict,screen,key="Movement"):
        super().__init__(surface_size,position,item_dict,screen,key)