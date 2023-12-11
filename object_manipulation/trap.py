from game_manipulation.imports import *

class Trap(Object):
    def __init__(self,surface_size,position,trap_dict,screen,key="Movement"):
        super().__init__(surface_size,position,trap_dict,screen,key)
