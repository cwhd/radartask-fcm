from mesa import Agent

class Worker(Agent):

    def __init__(self, unique_id, pos, model):
        '''
        grid: The MultiGrid object in which the agent lives.
        x: The agent's current x coordinate
        y: The agent's current y coordinate
       '''
        super().__init__(unique_id, model)
        self.pos = pos
        self.moore = moore
