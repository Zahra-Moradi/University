import pygame as pg
from pygame.math import Vector2
from vi import Agent, Simulation, Window
from vi.config import Config, dataclass, deserialize
from vi.util import random_angle
import polars as pl
import seaborn as sns
import random

@dataclass
class CompetitionModellingConfig(Config):
    #Constants for all agents
    # alignment_weight: float = 2
    # cohesion_weight: float = 1.2
    # separation_weight: float = 1.4
    delta_time: float = 5
    # mass: int = 20
    # def weights(self) -> tuple[float, float, float]:
    # return (self.alignment_weight, self.cohesion_weight, self.separation_weight)

