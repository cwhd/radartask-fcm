from radartaskfcm.agents import Worker, Team

from mesa import Model
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
from mesa.time import RandomActivation
import numpy as np
from mesa.time import SimultaneousActivation, RandomActivation

class RadarTask(Model):
    # grid height
    grid_h = 20
    # grid width
    grid_w = 20

    description = 'Social Simulation with cognitive agents.'

    def __init__(self, height=grid_h, width=grid_w, use_team=False):
        super().__init__()

        self.height = height
        self.width = width
        #have to initialize the grid
        self.grid = MultiGrid(self.width, self.height, torus=True)

        self.schedule = RandomActivation(self)

        x = 5
        y = 5
        team = Team(self.next_id(), (x, y), self)
        self.grid.place_agent(team, (x, y))
        self.schedule.add(team) 

        self.datacollector = DataCollector(model_reporters={
                                            "Hostile": lambda m: self.count_bad_votes(m),
                                            "Friendly": lambda m: self.count_good_votes(m),
                                            "Neutral": lambda m: self.count_neutral_votes(m),
                                            }
                                        )

    def step(self):
        # tell all the agents in the model to run their step function
        self.schedule.step()
        # collect data
        self.datacollector.collect(self)

    def run_model(self):
        for i in range(self.run_time):
            self.step()

    @staticmethod
    def count_good_votes(model):
        #TODO when agents vote, manage it
        return True

    @staticmethod
    def count_bad_votes(model):
        #TODO when agents vote, manage it
        return True

    @staticmethod
    def count_neutral_votes(model):
        #TODO when agents vote, manage it
        return True
