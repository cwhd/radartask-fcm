#from cooperation.agents import Cow, GrassPatch, FCMCow
#from cooperation.schedule import RandomActivationByBreed

from mesa import Model
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
from mesa.time import RandomActivation
import numpy as np

class RadarTask(Model):
    # grid height
    grid_h = 20
    # grid width
    grid_w = 20

    description = 'Social Simulation with cognitive agents.'

    #cooperative_probabilty should be between 0-100
    def __init__(self, height=grid_h, width=grid_w, use_team=False):

        self.height = height
        self.width = width
        #have to initialize the grid
        self.grid = MultiGrid(self.width, self.height, torus=True)

        super().__init__()

    def step(self):
        # tell all the agents in the model to run their step function
        #self.schedule.step()
        # collect data
        self.datacollector.collect(self)

    def run_model(self):
        for i in range(self.run_time):
            self.step()

