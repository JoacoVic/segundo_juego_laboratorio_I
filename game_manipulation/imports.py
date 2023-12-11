import pygame as py
import random
import json
import re
import sqlite3
from assets import *
from data_manipulation.text_box import TextBox
from game_manipulation.box import Box
from game_manipulation.config import *
from game_manipulation.programmer_mode import *
from object_manipulation.animation_dicts import *
from object_manipulation.object import Object
from object_manipulation.falling_object import FallingObject
from object_manipulation.final_boss import FinalBoss
from object_manipulation.projectile import Projectile
from object_manipulation.heroe import Heroe
from object_manipulation.platform import Platform
from object_manipulation.enemy import Enemy
from object_manipulation.trap import Trap
from object_manipulation.item import Item
from game_manipulation.game import *
from game_manipulation.third_level import ThirdLevel
from game_manipulation.first_level import FirstLevel
from game_manipulation.second_level import SecondLevel
from game_manipulation.level_selection import LevelSelection