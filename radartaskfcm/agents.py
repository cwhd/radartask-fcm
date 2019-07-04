from mesa import Agent

# TODO worker can act as a team or subordinate or manager
# TODO need a method to make a decision based on 3 inputs
# TODO manager gets inputs from agents to make a decision
# TODO add an FCM in here...
# TODO add a learning method for updating weights

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
