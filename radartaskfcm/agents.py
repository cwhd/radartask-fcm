from mesa import Agent
import random
from radartaskfcm.fcmwrapper import FCMUtils
from radartaskfcm.neowrapper import NeoUtils

# TODO worker can act as a team or subordinate or manager
# TODO manager gets inputs from agents to make a decision
# TODO add a learning method for updating weights

class Worker():

    def __init__(self, model_id):
        self.model_id = model_id
        self.breed = 'worker'
        self.fcm = '' # TODO this is the actual mental model
        self.neoService = NeoUtils()
        self.fcmService = FCMUtils()
        self.learning_threshold = .6
        self.weight_memory = []
        self.current_correct_count = 0
        self.current_check_count = 0
        #self.number_of_weights = 15 # 7
        self.number_of_weights = 7
        #TODO current weights should come from the DB at first...
        #self.current_weights = [.5,.5,.5,.5,.5,.5,.5,.5,.5,-.5,-.5,-.5, 0, .3, -.3]
        self.current_weights = [.5,.5,.5,.5,.5,.5,.3]
        self.last_decision = ''

    #given 3 inputs, decide if this is a friendly, hostile, or neutral aircraft
    def decide(self,radar_info):
        #the values are 1-3, so subtracting 2 gives us -1, 0, or 1
        radar_info[:] = [x - 2 for x in radar_info]

        fcm_input1 = { 'name':'property1', 'act':'TANH', 'output':radar_info[0], 'fixedOutput': False }
        fcm_input2 = { 'name':'property2', 'act':'TANH', 'output':radar_info[1], 'fixedOutput': False }
        fcm_input3 = { 'name':'property3', 'act':'TANH', 'output':radar_info[2], 'fixedOutput': False }
        body_input = [fcm_input1, fcm_input2, fcm_input3]
        concepts = { 'concepts':body_input }
        fcm_result = self.fcmService.getFCM(self.model_id, concepts)

        #print(fcm_result)
        good_guess = fcm_result['good']
        bad_guess = fcm_result['bad']
        neutral_guess = fcm_result['neutral']

        if(neutral_guess == 1):
            self.last_decision = "Neutral"
        elif(good_guess > 0):
            self.last_decision = "Good"
        elif(bad_guess > 0):
            self.last_decision = "Bad"
        else:
            self.last_decision = "Neutral"

        return self.last_decision


    def learn(self, is_correct):
        #TODO maybe I need to have different lists for how many are right, doing more mutation at 
        # the lower levels and less to none at the higher
        #print('updating mental model with new weights for worker ' + str(self.model_id))
        self.current_check_count += 1
        if(is_correct):
            self.current_correct_count += 1

        #check if there are any weights saved in weight_memory...
        #if there are grab 1 and tweak it, or grab 2 and combine them
        #TODO I wonder if we can make that process fuzzy as well, not so procedural
        # - that could be a good book - "fuzzy code"
        if(self.current_check_count > 4):
            #print('.', end='')
            #this section kills off lower performing weights in memory
            two_scorers = [t for t in self.weight_memory if t[0] == 2]
            three_scorers = [t for t in self.weight_memory if t[0] == 3]
            four_scorers = [t for t in self.weight_memory if t[0] == 4]
            five_scorers = [t for t in self.weight_memory if t[0] == 5]

            #increase learning threshold if we have good performers
            if(len(four_scorers) > 5 or len(five_scorers) > 4):
                self.learning_threshold = .8
            elif(len(four_scorers) > 10 or len(five_scorers) > 8):
                self.learning_threshold = .8

            if(self.current_correct_count / self.current_check_count >= self.learning_threshold):
                print('CORRECT')
                #print('--------------------------')
                #just in case it already exists
                print('Score Mix Before: Twos:' + str(len(two_scorers)) + ', Threes: ' + str(len(three_scorers)) + ', Fours: ' + str(len(four_scorers)) + ', Fives: ' + str(len(five_scorers)))
                same_to_go = [t for t in self.weight_memory if t[1] == self.current_weights]
                #print('Checking weights...')
                #print(self.current_weights)
                #print(same_to_go)
                #print(self.weight_memory)
                #print('-------------------------------------------------')

                if(len(same_to_go) < 1):
                    #self.weight_memory.remove((self.current_correct_count, self.current_weights))
                    self.weight_memory.append((self.current_correct_count, self.current_weights))

                #print('--------------------------------------')
                #print('CORRECT!!! adding memory: ' + str(len(self.weight_memory)))
                #print('--------------------------------------')
                #print(self.weight_memory)
                #TODO sort the memory, put better results on top
                #print("keeping current weights; check count: " + str(self.current_correct_count) + ", current threshold = " + str(self.current_correct_count / self.current_check_count))
                #print(self.current_weights)
            else:
                #TODO use the tuple to select the best: results = [t[1] for t in mylist if t[0] == 10]
                #print('wrong, changing mental model!')
                new_weights = self.fcmService.getNewWeights()
                #print('new weights:')
                #print(new_weights)
                memory_length = len(self.weight_memory)
                #print('memory length:' + str(memory_length))
                if(memory_length == 1):
                    #just replace 2 weights randomly
                    random_property_1 = random.randint(0,self.number_of_weights - 1)
                    random_property_2 = random.randint(0,self.number_of_weights - 1)
                    print('Memory 1:')
                    #print(self.current_weights)
                    self.current_weights[random_property_1] = new_weights[random_property_1]
                    self.current_weights[random_property_2] = new_weights[random_property_2]
                    #print(self.current_weights)

                elif(memory_length > 2):
                    #print('Memory > 2:')
                    #genetic mutation...
                    random_parent_index_1 = random.randint(0, memory_length - 1)
                    random_parent_index_2 = random.randint(0, memory_length - 2)

                    random_parent_weights_1 = self.weight_memory[random_parent_index_1]
                    self.weight_memory.remove(random_parent_weights_1)
                    random_parent_weights_2 = self.weight_memory[random_parent_index_2]

                    self.weight_memory.append(random_parent_weights_1)

                    child = []
                    for i in range(len(random_parent_weights_1[1])):
                        if(random.randint(0,100) > 89):
                            child.append(random.randint(0,100)/100)
                        elif(i % 2 == 0):
                            child.append(random_parent_weights_1[1][i])
                        else:
                            child.append(random_parent_weights_2[1][i])

                    new_weights = child

                    #print('happy family')
                    #print(random_parent_weights_1[1])
                    #print(random_parent_weights_2[1])
                    #print(child)

                    #print('Score Mix After: Twos:' + str(len(two_scorers)) + ', Threes: ' + str(len(three_scorers)) + ', Fours: ' + str(len(four_scorers)) + ', Fives: ' + str(len(five_scorers)))

                fcm_result = self.fcmService.replaceFCM(self.model_id, new_weights)
                self.current_weights = new_weights
                #print("new weights: ")
                print('Weight Memory: ' + str(len(self.weight_memory)))

            self.current_check_count = 0
            self.current_correct_count = 0

        return "learning"

    def _clean_history(self):
        #if there are 4 scorers, remove half the 3 scorers and 2/3 of the 2 scorers?
        #print('removing low scorers...')
        two_scorers = [t for t in self.weight_memory if t[0] == 2]
        three_scorers = [t for t in self.weight_memory if t[0] == 3]
        four_scorers = [t for t in self.weight_memory if t[0] == 4]
        five_scorers = [t for t in self.weight_memory if t[0] == 5]

        if(len(five_scorers) > 2):
            #print('We have 5s..2: ' + str(len(two_scorers)) + ', 3: ' + str(len(three_scorers)) + ', 4: ' + str(len(four_scorers)) + ', 5: ' + str(len(five_scorers)))
            for i in range(int(round(len(three_scorers)*.6))) :
                self.weight_memory.remove(three_scorers[i])
            for i in range(int(round(len(two_scorers)*.8))) :
                self.weight_memory.remove(two_scorers[i])
        elif(len(four_scorers) > 4):
            #print('removing low scorers...2: ' + str(len(two_scorers)) + ', 3: ' + str(len(three_scorers)) + ', 4: ' + str(len(four_scorers)))
            for i in range(int(round(len(three_scorers)/2))) :
                self.weight_memory.remove(three_scorers[i])
            for i in range(int(round(len(two_scorers)*.6))) :
                self.weight_memory.remove(two_scorers[i])
            #print('New score update: ' + str(len(two_scorers)) + ', 3: ' + str(len(three_scorers)) + ', 4: ' + str(len(four_scorers)))
        elif(len(four_scorers) > 20):
            for i in range(int(round(len(four_scorers)*.5))) :
                self.weight_memory.remove(four_scorers[i])

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
            #print('using models: ' + str(i + 4))
            team_member = Worker("radar" + str(i + 4))
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

        if attribute_sum < 17:
            aircraft_type = "Friendly"
        elif attribute_sum > 19:
            aircraft_type = "Hostile"
        else:
            aircraft_type = "Neutral"

        return aircraft_type

    def step(self):
        radar_info = self.get_radar_info()
        #print("radar info:" + str(radar_info))
        decisions = []
        for i in range(self.team_count):
            worker = self.team_members[i]
            #print("worker:" + str(i) + " " + str(worker))
            decisions.append(worker.decide(radar_info[i*3:i*3+3])) #get worker decision
        
        #print("decisions: " + str(decisions))
        final_vote = ''
        if decisions.count('Good') > 1:
            final_vote = 'Friendly'
        elif decisions.count('Bad') > 1:
            final_vote = "Hostile"
        else:
            final_vote = "Neutral"

        actual_aircraft_type = self.check_aircraft_type(radar_info)

        is_correct = True
        if(actual_aircraft_type == final_vote):
            self.correct_count += 1
        else:
            self.wrong_count += 1
            is_correct = False

        for i in range(self.team_count):
            worker = self.team_members[i]
            #each worker learns at thier own pace
            if(worker.last_decision == actual_aircraft_type):
                worker.learn(True)
            else:
                worker.learn(False)
