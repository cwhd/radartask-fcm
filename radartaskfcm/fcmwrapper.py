import requests
import json
import random
from radartaskfcm.neowrapper import NeoUtils

''' Use like this...
from radartaskfcm.fcmwrapper import FCMUtils

    fcmService = FCMUtils()
    fcm_input1 = { 'name':'Food Observation', 'act':'INTERVAL', 'output':1, 'fixedOutput': True }
    fcm_input2 = { 'name':'Eat', 'act':'INTERVAL', 'output':1, 'fixedOutput': True }
    fcm_input3 = { 'name':'Energy', 'act':'INTERVAL', 'output':1, 'fixedOutput': True }
    body_input = [fcm_input1, fcm_input2]
    concepts = { 'concepts':body_input }
    fcm_result = fcmService.getFCM('greedyCow1', concepts)

'''
class FCMUtils():

#TODO would be cool to have a code generation button in the FCM modeler - 
# - so when you have params that you want, 
# -- click a button
# -- get some code you can copy/paste into here for params

    """
    Method to get results of an FCM based agent. 
    model_id : the id of the model from the FCM system
    starting_state_dict : dictionary of node state information to use as a starting point  
    """
    def getFCM(self, model_id, starting_state_dict):
        #print("getting FCM...")

        post_body = json.dumps(starting_state_dict)

        headers = {'content-type': 'application/json'}
        fcm_request = requests.post('http://localhost:8080/fcm/' + model_id + '/run?maxEpochs=1', data=post_body, headers=headers)
        results = fcm_request.json()
        results_dict = json.loads(fcm_request.text)
        fcm_dict = {}
        for node in results_dict['iterations'][0]['nodes']:
            fcm_dict[node['name']] = node['value']

        return fcm_dict

    def generateEvolvingCypher(self, model_id, new_weights):
        #TODO each of these lines can be a different string in an array, add them together 
        start_node = 0
        end_node = 5
        create_cypher = ("CREATE "
            "(`0` :`Decide Good` {modelId:'" + model_id + "',goal:'good',description:'good'}) , "
            "(`1` :Prop1 {modelId:'" + model_id + "',goal:'property1',description:'property1'}) , "
            "(`2` :Prop2 {modelId:'" + model_id + "',goal:'property2',description:'property2'}) , "
            "(`3` :Prop3 {modelId:'" + model_id + "',goal:'property3',description:'property3'}) , "
            "(`4` :`Decide Bad` {modelId:'" + model_id + "',goal:'bad',description:'bad'}) , "
            "(`5` :`Decide Neutral` {modelId:'" + model_id + "',goal:'neutral',description:'neutral'}) , ")

        #python - can I have a string with parameters that I fill in later?
        random_mutation_picker = random.randint(0, 2)
        # 1 = add connection
        # 2 = remove connection
        # 3 = change weight
        #print("current mutation = " + str(random_mutation_picker))
        if random_mutation_picker == 0:
            print("adding a connection")
            # numbers should be random within the params of the model
            # randomly generate the name
            random_start_node = random.randint(start_node, end_node)
            random_end_node = random.randint(start_node, end_node)
            new_connection = "(`" + random_start_node + "`)-[:`affects` {value:'0.5'}]->(`" + random_end_node + "`), "
            create_cypher += new_connection
            create_cypher += getCypherConnections(self, model_id, new_weights)
            print(create_cypher)
            return create_cypher

        elif random_mutation_picker == 1:
            print("removing connection")
        elif random_mutation_picker == 2:
            print("updating a weight")


        #combine successful models
        # - take half of one, half of the other

        #ASSUMPTIONS
        #- We will always have 6 nodes
        #- each node can have 0-5 outgoing connections
        #- a node can connect to any other node
        #- weights can be different 
        #- we can have a variable number of mutations on change

        return create_cypher

    def getCypherConnections(self, model_id, new_weights):
        return("(`1`)-[:`affects` {value:'-0.5'}]->(`0`), " #prop1->good
            "(`2`)-[:`affects` {value:'-0.5'}]->(`0`), " #prop2->good
            "(`3`)-[:`affects` {value:'-0.5'}]->(`0`), " #prop3->good
            "(`3`)-[:`affects` {value:'" + str(new_weights[0]) + "'}]->(`2`), "
            "(`3`)-[:`affects` {value:'" + str(new_weights[1]) + "'}]->(`1`), "
            "(`2`)-[:`affects` {value:'" + str(new_weights[2]) + "'}]->(`1`), "
            "(`2`)-[:`affects` {value:'" + str(new_weights[3]) + "'}]->(`3`), "
            "(`1`)-[:`affects` {value:'" + str(new_weights[4]) + "'}]->(`2`), "
            "(`1`)-[:`affects` {value:'" + str(new_weights[5]) + "'}]->(`3`), "
            "(`3`)-[:`affects` {value:'0.5'}]->(`4`), " #prop3->bad
            "(`2`)-[:`affects` {value:'0.5'}]->(`4`), " #prop2->bad
            "(`1`)-[:`affects` {value:'0.5'}]->(`4`)," #prop1->bad
            "(`2`)-[:`affects` {value:'0'}]->(`5`), " #prop2->neutral
            "(`1`)-[:`affects` {value:'0.3'}]->(`5`), " #prop1->neutral
            "(`3`)-[:`affects` {value:'-0.3'}]->(`5`)") #prop3->neutral  

    def generateCreateCypher(self, model_id, new_weights):
        print("FOR TESTIN...")
        generateEvolvingCypher(model_id, new_weights)

        '''
        cypher_create_old =  ("CREATE "
            "(`0` :`Decide Good` {modelId:'" + model_id + "',goal:'good',description:'good'}) , "
            "(`1` :Prop1 {modelId:'" + model_id + "',goal:'property1',description:'property1'}) , "
            "(`2` :Prop2 {modelId:'" + model_id + "',goal:'property2',description:'property2'}) , "
            "(`3` :Prop3 {modelId:'" + model_id + "',goal:'property3',description:'property3'}) , "
            "(`4` :`Decide Bad` {modelId:'" + model_id + "',goal:'bad',description:'bad'}) , "
            "(`5` :`Decide Neutral` {modelId:'" + model_id + "',goal:'neutral',description:'neutral'}) , "
            "(`1`)-[:`affects` {value:'" + str(new_weights[0]) + "'}]->(`0`), " #prop1->good
            "(`2`)-[:`affects` {value:'" + str(new_weights[1]) + "'}]->(`0`), " #prop2->good
            "(`3`)-[:`affects` {value:'" + str(new_weights[2]) + "'}]->(`0`), " #prop3->good
            "(`3`)-[:`affects` {value:'" + str(new_weights[3]) + "'}]->(`2`), "
            "(`3`)-[:`affects` {value:'" + str(new_weights[4]) + "'}]->(`1`), "
            "(`2`)-[:`affects` {value:'" + str(new_weights[5]) + "'}]->(`1`), "
            "(`2`)-[:`affects` {value:'" + str(new_weights[6]) + "'}]->(`3`), "
            "(`1`)-[:`affects` {value:'" + str(new_weights[7]) + "'}]->(`2`), "
            "(`1`)-[:`affects` {value:'" + str(new_weights[8]) + "'}]->(`3`), "
            "(`3`)-[:`affects` {value:'" + str(new_weights[9]) + "'}]->(`4`), " #prop3->bad
            "(`2`)-[:`affects` {value:'" + str(new_weights[10]) + "'}]->(`4`), " #prop2->bad
            "(`1`)-[:`affects` {value:'" + str(new_weights[11]) + "'}]->(`4`)," #prop1->bad
            "(`2`)-[:`affects` {value:'" + str(new_weights[12]) + "'}]->(`5`), " #prop2->neutral
            "(`1`)-[:`affects` {value:'" + str(new_weights[13]) + "'}]->(`5`), " #prop1->neutral
            "(`3`)-[:`affects` {value:'" + str(new_weights[14]) + "'}]->(`5`)") #prop3->neutral
        '''
        #TODO maybe if I just have nodes that are connected to the outcomes, not each other...

        #only need 7 if we hard code decisions and find the neutral
        #neutral needs to be a formula...maybe just take one weight and do something to it
        neutral_weights = []
        neutral_weights.append(new_weights[6])
        neutral_weights.append(new_weights[6]*1)
        neutral_weights.append(new_weights[6]*1)
        random.shuffle(neutral_weights)
        cypher_create =  ("CREATE "
            "(`0` :`Decide Good` {modelId:'" + model_id + "',goal:'good',description:'good'}) , "
            "(`1` :Prop1 {modelId:'" + model_id + "',goal:'property1',description:'property1'}) , "
            "(`2` :Prop2 {modelId:'" + model_id + "',goal:'property2',description:'property2'}) , "
            "(`3` :Prop3 {modelId:'" + model_id + "',goal:'property3',description:'property3'}) , "
            "(`4` :`Decide Bad` {modelId:'" + model_id + "',goal:'bad',description:'bad'}) , "
            "(`5` :`Decide Neutral` {modelId:'" + model_id + "',goal:'neutral',description:'neutral'}) , "
            "(`1`)-[:`affects` {value:'-0.5'}]->(`0`), " #prop1->good
            "(`2`)-[:`affects` {value:'-0.5'}]->(`0`), " #prop2->good
            "(`3`)-[:`affects` {value:'-0.5'}]->(`0`), " #prop3->good
            "(`3`)-[:`affects` {value:'" + str(new_weights[0]) + "'}]->(`2`), "
            "(`3`)-[:`affects` {value:'" + str(new_weights[1]) + "'}]->(`1`), "
            "(`2`)-[:`affects` {value:'" + str(new_weights[2]) + "'}]->(`1`), "
            "(`2`)-[:`affects` {value:'" + str(new_weights[3]) + "'}]->(`3`), "
            "(`1`)-[:`affects` {value:'" + str(new_weights[4]) + "'}]->(`2`), "
            "(`1`)-[:`affects` {value:'" + str(new_weights[5]) + "'}]->(`3`), "
            "(`3`)-[:`affects` {value:'0.5'}]->(`4`), " #prop3->bad
            "(`2`)-[:`affects` {value:'0.5'}]->(`4`), " #prop2->bad
            "(`1`)-[:`affects` {value:'0.5'}]->(`4`)," #prop1->bad
            "(`2`)-[:`affects` {value:'0'}]->(`5`), " #prop2->neutral
            "(`1`)-[:`affects` {value:'0.3'}]->(`5`), " #prop1->neutral
            "(`3`)-[:`affects` {value:'-0.3'}]->(`5`)") #prop3->neutral            

            #"(`2`)-[:`affects` {value:'" + str(neutral_weights[0]) + "'}]->(`5`), " #prop2->neutral
            #"(`1`)-[:`affects` {value:'" + str(neutral_weights[1]) + "'}]->(`5`), " #prop1->neutral
            #"(`3`)-[:`affects` {value:'" + str(neutral_weights[2]) + "'}]->(`5`)") #prop3->neutral            

        return cypher_create

    def replaceFCM(self, model_id, new_weights):
        add_cypher = self.generateCreateCypher(model_id, new_weights)
        delete_cypher = "MATCH (n {modelId:'" + model_id + "'}) where not exists (n.internalType) DETACH DELETE n "

        headers = {'content-type': 'application/json'}
        fcm_request = requests.post('http://localhost:8080/model', data=delete_cypher, headers=headers)
        results = fcm_request.json()
        #print("delete results: " + str(results))
        #make sure this is 200 then...
        headers = {'content-type': 'application/json'}
        fcm_request = requests.post('http://localhost:8080/model', data=add_cypher, headers=headers)
        results = fcm_request.json()
        #print("delete results: " + str(results))
        #print("add cypher: " + add_cypher)
        #print("delete cypher: " + delete_cypher)

    def replaceFCMWithCypher(self, model_id, add_cypher):
        #delete...
        delete_cypher = "MATCH (n {modelId:'" + model_id + "'}) where not exists (n.internalType) DETACH DELETE n "
        headers = {'content-type': 'application/json'}
        fcm_request = requests.post('http://localhost:8080/model', data=delete_cypher, headers=headers)
        results = fcm_request.json()
        #add...
        headers = {'content-type': 'application/json'}
        fcm_request = requests.post('http://localhost:8080/model', data=add_cypher, headers=headers)
        results = fcm_request.json()
        #print('REPLACEMENT RESULTS')
        #print(results)
        #print(results['errors'])
        if len(results['errors']) > 0:
            print('ERROR ADDING CYPHER')
            print(add_cypher)

        
    def getNewWeights(self):

        weight_count = 7
        weights = []
        for i in range(weight_count):
            weights.append(random.randint(-100,100)/100)

        return weights
