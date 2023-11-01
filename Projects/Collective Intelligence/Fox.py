import pygame as pg
from pygame.math import Vector2
from vi import Agent, Simulation, Window
from vi.config import Config, dataclass, deserialize
from vi.util import random_angle, probability
import polars as pl
import seaborn as sns
import random

from Config_c import CompetitionModellingConfig
from Rabbit import Rabbit
import Globals


class Fox(Agent):
    config: CompetitionModellingConfig
    energy_level: float = 1000
    energy_drain: float = 5.5
    name: str = "fox"
    hunting_speed: int = 1.05

    # random wandering in the environment
    def wander(self):
        wandering = random_angle(length=1)
        self.move = self.move.normalize()
        self.move += wandering * 0.2
        self.pos = self.pos + (self.move.normalize() * self.config.delta_time)

    def activate_hunting(self):
        # fox is in hunting state if it is hungry and looking for a rabbit to chase
        nearest_rabbit = self.in_proximity_accuracy().filter_kind(Rabbit).filter(lambda agent: agent[0].on_site() == False).first()
        if nearest_rabbit is not None:
            #rabbit found. move to target.
            self.hunt(nearest_rabbit[0])
        else:
            #no rabbit near. random move.
            self.wander()
    
    def hunt(self, rabbit):
        # instead of random walking, give target agent and fox will chase target
        self.move = self.move.normalize()
        self.move += rabbit.pos - self.pos
        self.pos = self.pos + (self.move.normalize() * self.config.delta_time*self.hunting_speed)   
    
    # if energy level is empty, die
    def die(self):
        if self.energy_level <= 0:
            self.kill()

    # check if hungry, if hungry and there is a rabbit --> eat
    def eat(self):
        rabbit = self.in_proximity_accuracy().filter_kind(Rabbit).first()
        if rabbit is not None and rabbit[0].is_alive():
            if rabbit[1]<4:
                rabbit[0].kill()  
                self.energy_level += 500
                # max energy lvl to not have super energy reserves in foxes
                if self.energy_level > 1000:
                    self.energy_level = 1000
                self.reproduction()       

    # check if we can reproduce, if we can --> reproduce and reduce energy level
    def reproduction(self):
        neighbors = self.in_proximity_performance().filter_kind(Fox).count()
        if probability(1-(neighbors/10)):
            self.reproduce()
            self.energy_level -= 300

    # avoid any obstacles in the environment
    def avoid_obstacle(self):
        obstacle_center_generator = self.obstacle_intersections(scale = 2)
        for expression in obstacle_center_generator:
            obstacle_center = expression
            obstacle_avoidance = self.pos - obstacle_center
            self.move = obstacle_avoidance
            self.move = self.move.normalize()
            self.pos = self.pos + (self.move * self.config.delta_time)

    # avoid any site in the environment
    def avoid_site(self):
        self.move = self.move.normalize()
        self.move = -1 * self.move
        self.pos = self.pos + (self.move.normalize() * self.config.delta_time)
    
    # updates location
    def change_position(self):
        self.there_is_no_escape()
        self.avoid_obstacle()
        if self.on_site():
            self.avoid_site()
        self.activate_hunting()

    # updates the agent
    def update(self):
        if self.is_alive():
            self.save_data("alive", "fox-alive")  
        else:
            self.save_data("alive", "fox-dead") 
        self.die()
        self.eat()
        # reset energy level if it exceeds 100
        if self.energy_level > 1000:
            self.energy_level = 1000
        # getting hungry over time
        self.energy_level -= self.energy_drain
