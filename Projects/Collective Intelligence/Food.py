import pygame as pg
from pygame.math import Vector2
from vi import Agent, Simulation, Window
from vi.config import Config, dataclass, deserialize
from vi.util import random_angle
import polars as pl
import seaborn as sns
import random

from Config_c import CompetitionModellingConfig



class Carrot(Agent):
    config: CompetitionModellingConfig
    name: str = "carrot"
    #Individual variables
    #growth_prob : float = 0.1
    def change_position(self):
        self.freeze_movement()

    def update(self):
        self.save_data("alive", "carrot")  


class Grass(Agent):
    config: CompetitionModellingConfig
    name: str = "grass"
    # individual variables
    #growth_prob : float = 0.1

    def change_position(self):
        self.freeze_movement()
        
    def update(self):
        self.save_data("alive", "grass")  

