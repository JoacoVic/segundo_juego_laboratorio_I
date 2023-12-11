from game_manipulation.imports import *

class Projectile(Object):
    def __init__(self,surface_size,position,projectile_list,screen,speed=20):
        super().__init__(surface_size,position,projectile_list,screen,"First_turn")
        self.set_speed(speed)
    
    def update(self,last_direction):
        if last_direction == "Right":
            self.move_right()
        elif last_direction == "Left":
            self.move_left()
    
    def check_edges(self):
        validation = False
        if self.rect.centerx < 0 or self.rect.centerx > self.screen.get_width():
                validation = True
        return validation
    
    def check_enemy_collision(self,enemies_list):
        validation = False
        for enemy in enemies_list:
            if self.rect.colliderect(enemy.rect):
                enemy.impact = True
                self.set_music(r"assets\Musica\impacto.wav", 0.5)
                if self.object_dict == projectile_dict:
                    enemy.life_amount -= 1
                else:
                    enemy.life_amount -= 2
                enemy.direction = "Impact"
                validation = True
                break
        return validation


