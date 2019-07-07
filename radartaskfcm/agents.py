from mesa import Agent
import random
from radartaskfcm.fcmwrapper import FCMUtils
from radartaskfcm.neowrapper import NeoUtils

# TODO worker can act as a team or subordinate or manager
# TODO need a method to make a decision based on 3 inputs
# TODO manager gets inputs from agents to make a decision
# TODO add an FCM in here...
# TODO add a learning method for updating weights

class Worker():

    def __init__(self, model_id):
        self.model_id = model_id
        self.breed = 'worker'
        # the FCMs should be radar1, radar2 and radar3
        self.fcm = '' # TODO this is the actual mental model
        self.neoService = NeoUtils()
        self.fcmService = FCMUtils()

    #given 3 inputs, decide if this is a friendly, hostile, or neutral aircraft
    def decide(self,radar_info):
        print("CALL FCM HERE...")
        if sum(radar_info) <= 5:
            return "Good"
        elif sum(radar_info) >= 7:
            return "Bad"
        else:
            return "Neutral"

    def learn(self, is_correct):
        print('updating mental model with new weights for worker ' + str(self.model_id))
        if(not is_correct):
            #TODO call neo service here, update model for this worker
            #self.neoService.callNeo()
            new_weights = self.fcmService.getNewWeights()
            print('wrong, changing mental model!')
            print(new_weights)

        self.fcm = ''
        return "learning"

class Team(Agent):
    def __init__(self, unique_id, pos, model):
        '''
        grid: The MultiGrid object in which the agent lives.
        x: The agent's current x coordinate
        y: The agent's current y coordinate
       '''
        super().__init__(unique_id, model)
        self.breed = 'manager'
        self.pos = pos
        self.team_count = 3
        self.team_members = []
        self.correct_count = 0
        self.wrong_count = 0
        for i in range(3):
            team_member = Worker("radar" + str(i))
            self.team_members.append(team_member)

    def get_radar_info(self):
        #Randomly generate 9 attributes, each with a value from 1-3
        attribute_count = 9
        attributes = []
        for i in range(attribute_count):
            attributes.append(random.randint(1,3))

        return attributes

    def check_aircraft_type(self, attributes):
        attribute_sum = sum(attributes)
        aircraft_type = ""

        if attribute_sum <= 17:
            aircraft_type = "Friendly"
        elif attribute_sum >= 19:
            aircraft_type = "Hostile"
        else:
            aircraft_type = "Neutral"

        return aircraft_type

    def step(self):
        print("step...")
        radar_info = self.get_radar_info()
        print("radar info:")
        print(radar_info)
        decisions = []
        for i in range(self.team_count):
            worker = self.team_members[i]
            decisions.append(worker.decide(radar_info[i*3:i*3+3])) #get worker decision
        
        final_vote = ''
        if decisions.count('Good') > 1:
            final_vote = 'Friendly'
        elif decisions.count('Bad') > 1:
            final_vote = "Hostile"
        else:
            final_vote = "Neutral"

        is_correct = True
        if(self.check_aircraft_type(radar_info) == final_vote):
            self.correct_count += 1
        else:
            self.wrong_count += 1
            is_correct = False

        for i in range(self.team_count):
            worker = self.team_members[i]
            worker.learn(is_correct)