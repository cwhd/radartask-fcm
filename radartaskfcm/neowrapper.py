import requests
import json
import random

class NeoUtils():

    '''
    Call Neo4J through the REST API
    '''
    def callNeo(self, neo_query, data_contents):

        post_body = "{ \"statements\" : [ {"
        post_body += "\"statement\" : \""
        post_body += neo_query
        post_body += "\""
        if(data_contents):
            post_body += ", \"resultDataContents\":"
            post_body += data_contents
        post_body += "} ] }"
        
        headers = {'content-type': 'application/json', 'Authorization':'bmVvNGo6YWRtaW4='}
        neo_request = requests.post('http://neo4j:7474/db/data/transaction/commit', data=post_body, headers=headers)
        results = neo_request.json()
        results_dict = json.loads(neo_request.text)

        return results_dict
