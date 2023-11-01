from cmath import inf
from turtle import distance
import pygame as pg
from pygame.math import Vector2
from vi import Agent, Simulation, Window
from vi.config import Config, dataclass, deserialize
from vi.util import random_angle, probability, random_pos
import polars as pl
import seaborn as sns
import random
import numpy as np


from Config_c import CompetitionModellingConfig
from Food import Carrot
from Food import Grass
import Globals

class Rabbit(Agent):
    config: CompetitionModellingConfig
    reproduction_timer:  int = 0.5 * 60
    name: str = "rabbit"
    panic_alarm: bool = False
    state: str = 'wander'
    panic_timer: int = 0 
    panic_counter: int = 4*60 
    shelter_timer: int = 0 
    shelter_counter: int = 7*60
    leave_counter: int = 6*60
    leave_timer: int = -6*60
    join_timer: int = 0
    join_counter: int = 20

     # random walking in the environment
    def random_walking(self):
        wandering = random_angle(length=1)
        self.move = self.move.normalize()
        self.move += wandering * 0.3
        self.pos = self.pos + (self.move.normalize() * self.config.delta_time)

    # wander state
    def wander(self):
        self.random_walking()
        nr_neighboring_foxes = self.in_proximity_performance().filter(lambda agent: agent.name == 'fox').count()
        if self.shared.counter > self.leave_timer + self.leave_counter:
            if nr_neighboring_foxes > 4:
                self.panic_timer = self.shared.counter
                self.panic_alarm = True
                self.state = "panic"

    def panic(self):
        site_pos = self.get_site()
        if (self.shared.counter < self.panic_timer + self.panic_counter) and (self.panic_alarm == True):
            if site_pos is not None:
                self.move_to(site_pos)
                if self.on_site():
                    self.join_timer = self.shared.counter
                    self.state = "shelter-join"
            else:
                self.random_walking()
        else:
            self.random_walking()
            self.panic_alarm = False
            self.state = "wander"

    def move_to(self,position):
        self.move = self.move.normalize()
        self.move += position - self.pos
        self.pos = self.pos + (self.move.normalize() * self.config.delta_time)

    def join_shelter(self):
        if self.on_site():
            shelter_pos = self.get_site()
            shelter_area = pg.Rect(shelter_pos, (10, 10))
            rand_pos = random_pos(area=shelter_area)
            self.move_to(rand_pos)
            if self.shared.counter > self.join_counter+self.join_timer:
                self.shelter_timer = self.shared.counter
                self.state = "shelter-stay"
        else:
            self.state = "wander"
        
    def stay_shelter(self):
        if self.on_site():
            self.freeze_movement()
            if (self.shared.counter > self.shelter_counter+self.shelter_timer):
                self.leave_timer = self.shared.counter
                self.state = "shelter-leave"
        else:
            self.state = "wander"
    
    def leave_shelter(self):
        self.random_walking()
        T_leave = 1 * 60
        if self.shared.counter > T_leave+self.leave_timer:
            self.leave_timer = self.shared.counter 
            self.panic_alarm = False
            self.state = "wander"

    def get_site(self):
        distance_min = inf
        position = None
        for site in self._sites.sprites():
            distance = site.pos - self.pos
            distance_length = pg.Vector2.length(distance)
            if distance_length < distance_min:
                distance_min = distance_length
                position = site.pos
        if distance_min < 60:
            loc = position
        else:
            loc = None
        return loc
    
    # checks if we can reproduce, if so we reproduce
    def reproduction(self,nr):
        neighbors = self.in_proximity_performance().filter_kind(Rabbit).count()
        if probability(1-(neighbors/nr)):
            self.reproduce()

    # avoid any obstacles in the environment
    def avoid_obstacle(self):
        obstacle_center_generator = self.obstacle_intersections(scale = 2)
        for expression in obstacle_center_generator:
            obstacle_center = expression
            obstacle_avoidance = self.pos - obstacle_center
            self.move = obstacle_avoidance
            self.move = self.move.normalize()
            self.pos = self.pos + (self.move.normalize() * self.config.delta_time)

    # updates location
    def change_position(self):
        self.there_is_no_escape()
        self.avoid_obstacle()
        if self.state == "wander":
            self.wander()
        elif self.state == "panic":
            self.panic()
        elif self.state == "shelter-join":
            self.join_shelter()
        elif self.state == "shelter-stay":
            self.stay_shelter()
        elif self.state == "shelter-leave":
            self.leave_shelter()

    # updates the agent
    def update(self):
        if self.is_alive():
            self.save_data("alive", "rabbit-alive")  
        else:
            self.save_data("alive", "rabbit-dead")
        if self.shared.counter % self.reproduction_timer == 0:
            if self.on_site():
                self.reproduction(nr=18)
            else:
                self.reproduction(nr=9)