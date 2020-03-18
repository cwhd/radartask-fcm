from mesa import Agent
import random
from radartaskfcm.fcmwrapper import FCMUtils
from radartaskfcm.neowrapper import NeoUtils
from radartaskfcm.mutation import MutationUtils
#from radartaskfcm.deapeval import Deapeval

# Represents the manager in a hierarchy
class Manager():

    def __init__(self, model_id):
        self.model_id = model_id
        self.neoService = NeoUtils()
        self.fcmService = FCMUtils()
        self.worker_opinions = [1,1,1,1,1,1,1,1,1]
        self.mutationService = MutationUtils()
        #self.deapeval = Deapeval()

    def decide(self, workers):

        #TODO this needs to change to reflect the FCM for the manager
        #fcm_input1 = { 'name':'property1', 'act':'SIGMOID', 'output':worker_decisions[0], 'fixedOutput': False }
        #fcm_input2 = { 'name':'property2', 'act':'SIGMOID', 'output':worker_decisions[1], 'fixedOutput': False }
        #fcm_input3 = { 'name':'property3', 'act':'SIGMOID', 'output':worker_decisions[2], 'fixedOutput': False }
        #body_input = [fcm_input1, fcm_input2, fcm_input3]
        #concepts = { 'concepts':body_input }
        #fcm_result = self.fcmService.getFCM(self.model_id, concepts)
        #print('deciding...')
        good_weight = 0
        bad_weight = 0
        neutral_weight = 0
        for i in range(len(workers)):
            #print(i)
            if(workers[i].last_decision == 'Good'):
                good_weight += self.worker_opinions[1]
            elif(workers[i].last_decision == 'Bad'):
                bad_weight += self.worker_opinions[1]
            elif(workers[i].last_decision == 'Neutral'):
                neutral_weight += self.worker_opinions[1]

        if(good_weight > bad_weight and good_weight > neutral_weight):
            return 'Good'
        if(bad_weight > good_weight and bad_weight > neutral_weight):
            return 'Bad'
        else:
            return 'Neutral'
        
    def learn(self, is_correct, workers):
        for i in range(len(workers)):
            if workers[i].last_guess_correct:
                self.worker_opinions[i] += 1
            else:
                self.worker_opinions[i] -= 1
        #print('How the manager feels...')
        #print(self.worker_opinions)
    
# Represents a subordinate worker
class Worker():

    def __init__(self, model_id):
        self.model_id = model_id
        self.breed = 'worker'
        self.fcm = '' # TODO this is the actual mental model
        self.neoService = NeoUtils()
        self.fcmService = FCMUtils()
        #self.deapeval = Deapeval()
        self.mutationService = MutationUtils()
        self.learning_threshold = .8
        self.weight_memory = []
        self.bad_weight_memory = []
        self.connection_memory = []
        self.current_correct_count = 0
        self.current_check_count = 0
        #self.number_of_weights = 15 # 7
        self.number_of_weights = 7
        #self.current_weights = [.5,.5,.5,.5,.5,.5,.3]
        self.last_decision = ''
        self.last_certainty = 0
        self.mutation_chance = 10
        self.last_guess_correct = False
        self.fcm_result = ''
        #initialize weights
        self.current_connections = self.mutationService.getInitialConnections()
        self.current_weights = self.mutationService.getInitialWeights()
        self.fcmnodes = self.mutationService.getBaseNodes(model_id)
        
        self.initialCypher = self.mutationService.putItTogether(self.current_connections, self.current_weights, self.fcmnodes)
        #fcm_result = self.fcmService.replaceFCM(self.model_id, self.current_weights)
        fcm_result = self.fcmService.replaceFCMWithCypher(self.model_id, self.initialCypher)

    #given 3 inputs, decide if this is a friendly, hostile, or neutral aircraft
    def decide(self,radar_info):
        #the values are 1-3, so subtracting 2 gives us -1, 0, or 1
        radar_info[:] = [x - 2 for x in radar_info]

        '''
        SIGNUM
        TANH
        SIGMOID
        CAUCHY
        NARY
        LINEAR
        INTERVAL
        GAUSS
        '''

        fcm_input1 = { 'name':'property1', 'act':'LINEAR', 'output':radar_info[0], 'fixedOutput': False }
        fcm_input2 = { 'name':'property2', 'act':'LINEAR', 'output':radar_info[1], 'fixedOutput': False }
        fcm_input3 = { 'name':'property3', 'act':'LINEAR', 'output':radar_info[2], 'fixedOutput': False }
        body_input = [fcm_input1, fcm_input2, fcm_input3]
        concepts = { 'concepts':body_input }
        fcm_result = self.fcmService.getFCM(self.model_id, concepts)
        self.fcm_result = fcm_result

        #print('GETTING MODELID:' + str(self.model_id))
        #print(fcm_result)
        #print('fcm_result: good:' + str(fcm_result['good']) + ' bad:' + str(fcm_result['bad']) + ' neutral:' + str(fcm_result['neutral']))
        good_guess = fcm_result['good']
        bad_guess = fcm_result['bad']
        neutral_guess = fcm_result['neutral']

        if(neutral_guess == 1):
            self.last_decision = "Neutral"
            self.last_certainty = 1
        if(bad_guess == 1):
            self.last_decision = "Bad"
            self.last_certainty = 1
        if(good_guess == 1):
            self.last_decision = "Good"
            self.last_certainty = 1

        '''
        #make decision & determine certainty
        if(neutral_guess > good_guess and neutral_guess > bad_guess):
            self.last_decision = "Neutral"
            self.last_certainty = 1
        if(good_guess > neutral_guess and good_guess > bad_guess):
            self.last_decision = "Good"
            self.last_certainty = 1
        if(bad_guess > good_guess and bad_guess > neutral_guess):
            self.last_decision = "Bad"
            self.last_certainty = 1

        if(neutral_guess ==  good_guess or neutral_guess == bad_guess):
            self.last_decision = "Neutral"
            self.last_certainty = 0.3

        if(good_guess == bad_guess):
            self.last_decision = "Good"
            self.last_certainty = 0.5
        '''

        return self.last_decision

    #do some random mutation
    def _mutate_weights(self, weights, mutate_count):
        #print("MUTATING...")
        new_weights = self.fcmService.getNewWeights()
        for i in range(mutate_count):
            random_property = random.randint(0,self.number_of_weights - 1)
            weights[random_property] = new_weights[random_property]

        return weights

    def learn_with_mutate(self, is_correct, flip_fh):
 
        self.last_guess_correct = is_correct
        self.current_check_count += 1
        if(is_correct):
            self.current_correct_count += 1

        if(self.current_check_count > 4):
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

            #if it's correct, add it to memory
            if(self.current_correct_count / self.current_check_count >= self.learning_threshold):
                #print('CORRECT')
                #print('--------------------------')
                #just in case it already exists
                print('Score Mix Before: Twos:' + str(len(two_scorers)) + ', Threes: ' + str(len(three_scorers)) + ', Fours: ' + str(len(four_scorers)) + ', Fives: ' + str(len(five_scorers)))
                same_to_go = [t for t in self.weight_memory if t[1] == self.current_weights]
                same_connection_memory = [t for t in self.connection_memory if t[1] == self.current_connections]

                #print('SAME TO GO')
                #print(same_to_go)
                #print(same_connection_memory)
                #if(len(same_to_go) < 1 and len(same_connection_memory) < 1): 
                    #self.weight_memory.remove((self.current_correct_count, self.current_weights))
                #TODO I really should check to see if something already exists...though that would be unlikely 
                self.weight_memory.append((self.current_correct_count, self.current_weights))
                self.connection_memory.append((self.current_correct_count, self.current_connections))

            else:
                #print('NOT CORRECT')
                memory_length = len(self.weight_memory)
                if(memory_length > 20 and random.randint(0,100) > 50):
                    print('SHUFFLING GENES')
                    random_parent_index_1 = random.randint(0, memory_length - 1)
                    random_parent_index_2 = random.randint(0, memory_length - 2)

                    random_parent_weights_1 = self.weight_memory[random_parent_index_1]
                    random_parent_connections_1 = self.connection_memory[random_parent_index_1]
                    
                    self.weight_memory.remove(random_parent_weights_1)
                    self.connection_memory.remove(random_parent_connections_1)

                    random_parent_weights_2 = self.weight_memory[random_parent_index_2]
                    random_parent_connections_2 = self.connection_memory[random_parent_index_2]

                    self.weight_memory.append(random_parent_weights_1)
                    self.connection_memory.append(random_parent_connections_1)

                    child_weights = []
                    child_connections = []
                    for i in range(len(random_parent_weights_1)):
                        #print('SHUFFLING...')
                        #print(random_parent_weights_1)
                        #print(random_parent_connections_2)
                        if(i % 2 == 0):
                            child_weights.append(random_parent_weights_1[i])
                            child_connections.append(random_parent_connections_1[i])
                        else:
                            if(len(random_parent_weights_2) > i):
                                child_weights.append(random_parent_weights_2[i])
                                child_connections.append(random_parent_connections_2[i])
                            else:
                                child_weights.append(random_parent_weights_1[i])
                                child_connections.append(random_parent_connections_1[i])

                    new_weights = child_weights
                    new_connections = child_connections

                    self.current_weights = new_weights
                    self.current_connections = new_connections

                    self.initialCypher = self.mutationService.putItTogether(self.current_connections, self.current_weights, self.fcmnodes)
                    #print('REPLACHING CYPHER')
                    #print(self.initialCypher)
                    fcm_result = self.fcmService.replaceFCMWithCypher(self.model_id, self.initialCypher)
                else:
                    #print('NOT ENOUGH MEMORY, MUTATING')
                    '''
                    if(flip_fh): #random.randint(0,100) > 10 and 
                        #print("FLIPPING")
                        #print("BEFORE AND AFTER FLIP")
                        #print(self.current_weights)
                        try:
                            self.current_weights[0] = -float(self.current_weights[0])
                            self.current_weights[1] = -float(self.current_weights[1])
                            self.current_weights[2] = -float(self.current_weights[2])

                            self.current_weights[9] = -float(self.current_weights[9])
                            self.current_weights[10] = -float(self.current_weights[10])
                            self.current_weights[11] = -float(self.current_weights[11])
                        except:
                            print("FLIPPIN ERR: ")
                        print(self.current_weights)
                    else:
                        '''
                    evolved = self.mutationService.evolveCypher(self.model_id, self.current_weights, self.current_connections)
                    self.current_weightsweights = evolved[1]
                    self.current_connections = evolved[0]
                    
                    evolved_cypher = self.mutationService.putItTogether(self.current_connections, self.current_weights, self.fcmnodes)
                    #print('EVOLVED CYPHER::')
                    #print(evolved_cypher)    
                    #fcm_result = self.fcmService.replaceFCM(self.model_id, new_weights)
                    #self.current_weights = weights
                    #self.current_connections = connections

                    self.initialCypher = self.mutationService.putItTogether(self.current_connections, self.current_weights, self.fcmnodes)
                    #print('REPLACHING CYPHER')
                    #print(self.initialCypher)
                    fcm_result = self.fcmService.replaceFCMWithCypher(self.model_id, self.initialCypher)

                    #print('Weight Memory for ' + str(self.model_id) + ':' + str(len(self.weight_memory)))

            self.current_check_count = 0
            self.current_correct_count = 0        

        return "learning"

    def learn(self, is_correct):
        #TODO maybe I need to have different lists for how many are right, doing more mutation at 
        # the lower levels and less to none at the higher
        #print('updating mental model with new weights for worker ' + str(self.model_id))
        self.last_guess_correct = is_correct
        self.current_check_count += 1
        if(is_correct):
            self.current_correct_count += 1

        #check if there are any weights saved in weight_memory...
        #if there are grab 1 and tweak it, or grab 2 and combine them
        #TODO I wonder if we can make that process fuzzy as well, not so procedural
        # - that could be a good book - "fuzzy code"
        if(self.current_check_count > 4):
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

                if(len(same_to_go) < 1):
                    #self.weight_memory.remove((self.current_correct_count, self.current_weights))
                    self.weight_memory.append((self.current_correct_count, self.current_weights))

            else:
                new_weights = self.fcmService.getNewWeights()
                memory_length = len(self.weight_memory)
                if(memory_length == 1):
                    self.current_weights = self._mutate_weights(self.current_weights, 2)

                elif(memory_length > 2):
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

                    if(random.randint(0,100) <= self.mutation_chance):
                        self.current_weights = self._mutate_weights(self.current_weights, 1)

                    #print('happy family')
                    #print(random_parent_weights_1[1])
                    #print(random_parent_weights_2[1])
                    #print(child)

                    #print('Score Mix After: Twos:' + str(len(two_scorers)) + ', Threes: ' + str(len(three_scorers)) + ', Fours: ' + str(len(four_scorers)) + ', Fives: ' + str(len(five_scorers)))

                fcm_result = self.fcmService.replaceFCM(self.model_id, new_weights)
                self.current_weights = new_weights
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

#common functions for different scenarios
class BaseAgent(Agent):

    #assign aircraft properties in a distributed way
    def assign_distributed(self, radar_info, team_members):
        #print('distributed info')
        decisions = []
        for i in range(9):
            worker = team_members[i]
            if i == 0:
                decisions.append(worker.decide(radar_info[0:3])) 
            elif i < 7 and i > 0:
                decisions.append(worker.decide(radar_info[i:i+3])) 
            elif i == 7:
                decisions.append(worker.decide([radar_info[7], radar_info[8], radar_info[0]])) 
            elif i == 8:
                decisions.append(worker.decide([radar_info[8], radar_info[0], radar_info[1]])) 

        return decisions

    #assing aircraft properties in a blocked way
    def assign_blocked(self, radar_info, team_members):
        #print('blocked info')
        decisions = []
        for i in range(3): 
            for j in range(3): #assign 3 workers at a time 012, 345, 678 or 036, 147, 258
                worker = team_members[i+(3*j)]
                decisions.append(worker.decide(radar_info[i*3:i*3+3])) #get worker decision
        return decisions

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

class Hierarchy(BaseAgent):
    def __init__(self, unique_id, pos, model, info_type):
        '''
        grid: The MultiGrid object in which the agent lives.
        x: The agent's current x coordinate
        y: The agent's current y coordinate
       '''
        super().__init__(unique_id, model)
        self.breed = 'hierarchy'
        self.pos = pos
        self.team_count = 9 
        self.team_members = []
        self.correct_count = 0
        self.wrong_count = 0
        self.info_type = info_type
        for i in range(self.team_count):
            print('using models: ' + str(i + 4))
            team_member = Worker("radar" + str(i + 4))
            self.team_members.append(team_member)
        self.manager = Manager("radarmanager") #TODO make sure to get the correct model

    def step(self):

        radar_info = self.get_radar_info()
        #print("radar info:" + str(radar_info))
        decisions = []
        if(self.info_type == 'distributed'):
            decisions = self.assign_distributed(radar_info, self.team_members)
        else:
            decisions = self.assign_blocked(radar_info, self.team_members)

        final_decision = self.manager.decide(self.team_members)

        if final_decision == "Good":
            final_decision = "Friendly"
        elif final_decision == "Bad":
            final_decision = "Hostile"
        else:
            final_decision = "Neutral"          

        #print('Manager Decision: ' + final_decision)

        actual_aircraft_type = self.check_aircraft_type(radar_info)
        #print('Actual Aircraft: ' + actual_aircraft_type)

        for i in range(self.team_count):
            worker = self.team_members[i]

            if worker.last_decision == "Good":
                worker.last_decision = "Friendly"
            elif worker.last_decision == "Bad":
                worker.last_decision = "Hostile"
            else:
               worker.last_decision = "Neutral"          
            #each worker learns at thier own pace
            #if(worker.last_decision == actual_aircraft_type):
            #    worker.learn(True)
            #else:
            #    worker.learn(False)


        #print("TYPE AND DEC: " + actual_aircraft_type + ", " + final_decision)
        is_correct = True
        if(actual_aircraft_type == final_decision):
            self.correct_count += 1
        else:
            self.wrong_count += 1
            is_correct = False

        self.manager.learn(is_correct, self.team_members)

class Team(BaseAgent):
    def __init__(self, unique_id, pos, model, info_type):
        '''
        grid: The MultiGrid object in which the agent lives.
        x: The agent's current x coordinate
        y: The agent's current y coordinate
       '''
        super().__init__(unique_id, model)
        self.breed = 'team'
        self.pos = pos
        self.team_count = 9 
        self.team_members = []
        self.correct_count = 0
        self.wrong_count = 0
        self.hostile_incorrect = 0
        self.friendly_incorrect = 0
        self.neutral_incorrect = 0
        self.info_type = info_type
        for i in range(self.team_count):
            print('using models: ' + str(i + 4))
            team_member = Worker("radar" + str(i + 4))
            self.team_members.append(team_member)

    def step(self):
        radar_info = self.get_radar_info()
        #print("radar info:" + str(radar_info))
        decisions = []
        if(self.info_type == 'distributed'):
            decisions = self.assign_distributed(radar_info, self.team_members)
        else:
            decisions = self.assign_blocked(radar_info, self.team_members)
        
        #print("decisions: " + str(decisions))

        good_certainty = 0.0
        bad_certainty = 0.0
        neutral_certainty = 0.0
        for i in range(len(self.team_members)):
            if (self.team_members[i].last_decision == 'Good'):
                good_certainty += self.team_members[i].last_certainty
            elif (self.team_members[i].last_decision == 'Bad'):
                bad_certainty += self.team_members[i].last_certainty
            elif (self.team_members[i].last_decision == 'Neutral'):
                neutral_certainty += self.team_members[i].last_certainty

        #print("----------------------")
        #print("CERTAINTY: good: " + str(good_certainty) + " neutral: " + str(neutral_certainty) + " bad: " + str(bad_certainty))

        final_vote = ''
        if decisions.count('Good') > 4:
            final_vote = 'Friendly'
        elif decisions.count('Bad') > 4:
            final_vote = "Hostile"
        else:
            final_vote = "Neutral"

        certain_metric = decisions.count('Good') * good_certainty
        neutral_metric = decisions.count('Neutral') * neutral_certainty
        hostile_metric = decisions.count('Bad') * bad_certainty

        #print("FINAL VOTE BEFORE: " + str(final_vote))
        if(certain_metric > neutral_metric and certain_metric > hostile_metric):
            final_vote = 'Friendly'
        if(neutral_metric > certain_metric and neutral_metric > hostile_metric):
            final_vote = 'Neutral'
        if(hostile_metric > neutral_metric and hostile_metric > certain_metric):
            final_vote = 'Hostile'

        #print("FINAL VOTE AFTER: " + str(final_vote))
        #print("METRICS: good: " + str(certain_metric) + " neutral: " + str(neutral_metric) + " bad: " + str(hostile_metric))

        actual_aircraft_type = self.check_aircraft_type(radar_info)

        #print("ACTUAL VALUE: " + str(actual_aircraft_type))
        #print("----------------------")

        is_correct = True
        if(actual_aircraft_type == final_vote):
            self.correct_count += 1
        else:
            self.wrong_count += 1
            is_correct = False
            #self.hostile_incorrect = 0
            #self.friendly_incorrect = 0
            #self.neutral_incorrect = 0

        for i in range(self.team_count):
            worker = self.team_members[i]

            if worker.last_decision == "Good":
                worker.last_decision = "Friendly"
            elif worker.last_decision == "Bad":
                worker.last_decision = "Hostile"
            else:
               worker.last_decision = "Neutral"          

            if(worker.last_decision != actual_aircraft_type):
                if (worker.last_decision == "Hostile"):
                    self.hostile_incorrect += 1
                elif (worker.last_decision == "Friendly"):
                    self.friendly_incorrect += 1
                else:
                    self.neutral_incorrect += 1

            #print("--------------------------------")
            #print("PARITY CHECK:" + worker.last_decision + " + " + actual_aircraft_type)  
            #print("--------------------------------")

            flip_fh = False
            if (worker.last_decision == "Friendly" and actual_aircraft_type == "Hostile") or (worker.last_decision == "Hostile" and actual_aircraft_type == "Friendly"):
                flip_fh = True
            #each worker learns at thier own pace
            #if(worker.last_decision == actual_aircraft_type):
            #    worker.learn_with_mutate(True, flip_fh)
            #else:
            #    worker.learn_with_mutate(False, flip_fh)
