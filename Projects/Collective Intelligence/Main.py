import pygame as pg
from pygame.math import Vector2
from vi import Agent, HeadlessSimulation, Simulation, Window
from vi.config import Config, dataclass, deserialize
from vi.util import random_angle
import polars as pl
import seaborn as sns
import random

from Rabbit import Rabbit
from Config_c import CompetitionModellingConfig
from Fox import Fox
from Food import Carrot
from Food import Grass
import Globals

class CompetitionModelling(Simulation):
    config: CompetitionModellingConfig

df= (
    CompetitionModelling(
        CompetitionModellingConfig(
            image_rotation=False,
            movement_speed=1,
            radius=40,
            seed=1,
            window=Window(500,500),
            duration=3*60*60,
            fps_limit=0,
        )
    )
    .spawn_obstacle(image_path= "images\\lake.png", x=250, y=250)
    .spawn_site(image_path= "images\\shelter2.png", x=150, y=350)
    .spawn_site(image_path= "images\\shelter2.png", x=350, y=150)
    .batch_spawn_agents(50, Rabbit, images=["images\\rabbit.png"])
    .batch_spawn_agents(50, Fox, images=["images\\fox.png"])
   
    .batch_spawn_agents(1, Carrot, images=["images\\invisible-carrot.png"])
    .run()
    .snapshots
)

print(df)
df.write_csv("rabbit-fox-extended-behavior-baseline.csv")