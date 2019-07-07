import requests
import json
import random
from radartaskfcm.neowrapper import NeoUtils

''' Use like this...
from cooperation.fcmwrapper import FCMAgent

    def run_fcm(self, is_greedy, concepts):
        fcmService = FCMAgent()
        fcm_result = fcmService.getFCM('greedyCow1', concepts)
        return fcm_result  

    ...then later...

    fcm_input1 = { 'name':'Food Observation', 'act':'INTERVAL', 'output':1, 'fixedOutput': True }
    fcm_input2 = { 'name':'Eat', 'act':'INTERVAL', 'output':1, 'fixedOutput': True }
    fcm_input3 = { 'name':'Energy', 'act':'INTERVAL', 'output':1, 'fixedOutput': True }
    body_input = [fcm_input1, fcm_input2]
    concepts = { 'concepts':body_input }
    fcm_result = self.run_fcm(is_greedy, concepts)

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

    def replaceFCM(self, model_id, fcm_dict):
        #TODO need to figure out adding Cypher here...
        add_cypher = ""
        delete_cypher = "MATCH (n {modelId:'" + model_id + "'}) where not exists (n.internalType) DETACH DELETE n "

        headers = {'content-type': 'application/json'}
        fcm_request = requests.post('http://localhost:8080/model', data=delete_cypher, headers=headers)
        results = fcm_request.json()
        #make sure this is 200 then...
        headers = {'content-type': 'application/json'}
        fcm_request = requests.post('http://localhost:8080/model', data=add_cypher, headers=headers)
        results = fcm_request.json()
        
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


TODO translate this to Python

   var saveCypherToNeo = function(evt) {
        console.log("SAVING TO NEO...");
        var cypherExport = document.getElementById("taCypherExport").value;
        cypherExport = cypherExport.replace(/\r?\n|\r/g, " ")
        console.log("CYPHER EXPORT:");
        console.log(cypherExport);
        
        var requestModelId = document.getElementById("currentModelId").value;
        var deleteCypher = "MATCH (n {modelId:'" + requestModelId + "'}) where not exists (n.internalType) DETACH DELETE n ";

        //first delete
        fetch('http://localhost:8080/model', {
            method: 'POST',
            body: deleteCypher 
            }).then(response => response.json())
            .then(function (body) {
                console.log("DELETED CYPHER");
                console.log(body); 
                //then insert
                fetch('http://localhost:8080/model', {
                    method: 'POST',
                    body: cypherExport 
                    }).then(response => response.json())
                    .then(function (body) {
                    console.log(body); 
                }).catch(function (error) {
                    console.log("ERROR:" + error);
                });

        }).catch(function (error) {
            console.log("ERROR:" + error);
        });

        cancelModal();
    };
    d3.select( "#save_to_neo" ).on( "click", saveCypherToNeo );

"""