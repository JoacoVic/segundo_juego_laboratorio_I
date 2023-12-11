import pygame as py
from assets import *
import os

def rotate_image(images):
    """rota cada una de las imágenes de la lista que se le pasa por parámetro

    Args:
        images (list): la lista con las imágenes

    Returns:
        list: la lista con las imágenes rotadas
    """
    images_list = []
    for i in range(len(images)):
        rotated_image = py.transform.flip(images[i],True,False)
        images_list.append(rotated_image)
    
    return images_list

def load_sprites(folder_path):
    """recorre el path de la carpeta que se le pasa por parámetro para crear una lista de imágenes

    Args:
        folder_path (str): el path de la carpeta

    Returns:
        list: la lista con los sprites
    """
    sprites_list = []
    for file_name in os.listdir(folder_path):
        complete_path = os.path.join(folder_path, file_name)
        sprite = py.image.load(complete_path)
        sprites_list.append(sprite)
    return sprites_list


#Heroe
heroe_idle = load_sprites(r"assets\Imagenes\batman_quieto")
heroe_walk_right = load_sprites(r"assets\Imagenes\batman_camina")
heroe_jump_right = load_sprites(r"assets\Imagenes\batman_salta")
heroe_crash = load_sprites(r"assets\Imagenes\batman_choque")
heroe_death = load_sprites(r"assets\Imagenes\batman_muerto")

heroe_dict = {}
heroe_dict["Idle"] = heroe_idle
heroe_dict["Idle_left"] = rotate_image(heroe_idle)
heroe_dict["Right"] = heroe_walk_right
heroe_dict["Left"] = rotate_image(heroe_walk_right)
heroe_dict["Jump_right"] = heroe_jump_right
heroe_dict["Jump_left"] = rotate_image(heroe_jump_right)
heroe_dict["Crash_right"] = heroe_crash
heroe_dict["Crash_left"] = rotate_image(heroe_crash)
heroe_dict["Death"] = heroe_death
heroe_dict["Death_left"] = rotate_image(heroe_death)

#Enemigos
bat_right = load_sprites(r"assets\Imagenes\murcielago_movimiento")
bat_impact = load_sprites(r"assets\Imagenes\murcielago_impacto")
bat_explosion = load_sprites(r"assets\Imagenes\explosion")

bat_dict = {}
bat_dict["Right"] = bat_right
bat_dict["Left"] = rotate_image(bat_right)
bat_dict["Impact"] = bat_impact
bat_dict["Impact_left"] = rotate_image(bat_impact)
bat_dict["Explosion"] = bat_explosion

solomon_right = load_sprites(r"assets\Imagenes\solomon_movimiento")
solomon_impact = load_sprites(r"assets\Imagenes\solomon_impacto")
solomon_explosion = load_sprites(r"assets\Imagenes\explosion")

solomon_dict = {}
solomon_dict["Right"] = solomon_right
solomon_dict["Left"] = rotate_image(solomon_right)
solomon_dict["Impact"] = solomon_impact
solomon_dict["Impact_left"] = rotate_image(solomon_impact)
solomon_dict["Explosion"] = solomon_explosion

#Proyectil
projectile_first_turn = load_sprites(r"assets\Imagenes\batarang")
projectile_powered_up = load_sprites(r"assets\Imagenes\batarang_powered_up")

projectile_dict = {}
projectile_dict["First_turn"] = projectile_first_turn
projectile_dict["Second_turn"] = rotate_image(projectile_first_turn)

projectile_powered_up_dict = {}
projectile_powered_up_dict["First_turn"] = projectile_powered_up

#Trampas
saw_movement = load_sprites(r"assets\Imagenes\sierra")

saw_dict = {}
saw_dict["Movement"] = saw_movement

fire_movement = load_sprites(r"assets\Imagenes\fuego")

fire_dict = {}
fire_dict["Movement"] = fire_movement

#Items
coin_movement = load_sprites(r"assets\Imagenes\moneda")

coin_dict = {}
coin_dict["Movement"] = coin_movement

key_movement = load_sprites(r"assets\Imagenes\llave")

key_dict = {}
key_dict["Movement"] = key_movement

#Clayface
clayface_idle = load_sprites(r"assets\Imagenes\clayface_quieto")
clayface_impact = load_sprites(r"assets\Imagenes\clayface_impacto")
clayface_ball = load_sprites(r"assets\Imagenes\clayface_bola")
clayface_ball_movement = load_sprites(r"assets\Imagenes\clayface_bola_movimiento")
clayface_melted = load_sprites(r"assets\Imagenes\clayface_derretido")
clayface_explosion = load_sprites(r"assets\Imagenes\explosion")

clayface_dict = {}
clayface_dict["Idle"] = clayface_idle
clayface_dict["Idle_left"] = rotate_image(clayface_idle)
clayface_dict["Impact"] = clayface_impact
clayface_dict["Ball"] = clayface_ball
clayface_dict["Ball_movement"] = clayface_ball_movement
clayface_dict["Ball_movement_left"] = rotate_image(clayface_ball_movement)
clayface_dict["Melted"] = clayface_melted
clayface_dict["Explosion"] = clayface_explosion

#Bloque
block_falling = load_sprites(r"assets\Imagenes\bloque_caida")

block_dict = {}
block_dict["Falling"] = block_falling

#Corazon
heart = load_sprites(r"assets\Imagenes\heart")

heart_dict = {}
heart_dict["Movement"] = heart

#Batarang potenciado
powered_up_logo = load_sprites(r"assets\Imagenes\power_batarang")

powered_batarangs_dict = {}
powered_batarangs_dict["Movement"] = powered_up_logo