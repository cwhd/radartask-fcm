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

    def generateCreateCypher(self, model_id, new_weights):

        cypher_create =  ("CREATE "
            "(`0` :`Decide Good` {modelId:'" + model_id + "',goal:'good',description:'good'}) , "
            "(`1` :Prop1 {modelId:'" + model_id + "',goal:'property1',description:'property1'}) , "
            "(`2` :Prop2 {modelId:'" + model_id + "',goal:'property2',description:'property2'}) , "
            "(`3` :Prop3 {modelId:'" + model_id + "',goal:'property3',description:'property3'}) , "
            "(`4` :`Decide Bad` {modelId:'" + model_id + "',goal:'bad',description:'bad'}) , "
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
            "(`1`)-[:`affects` {value:'" + str(new_weights[11]) + "'}]->(`4`)") #prop1->bad
            
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
        
    def getNewWeights(self):

        weight_count = 12
        weights = []
        for i in range(weight_count):
            weights.append(random.randint(-100,100)/100)

        return weights

"""
TODO learning algorithm
- check FCM guess value against actual value
  - save the guessed answer and the actual answer for later
  - if it's wrong, readjust weights, save back to NEO
  - save number of iterations and value history
"""