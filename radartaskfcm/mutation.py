import random
import string
import re

class MutationUtils():

    #2) determine which mutation to use, then return the new weights and connections
    def evolveCypher(self, model_id, weights, initial_connections):

        start_node = 0
        end_node = 5
        #create_cypher = base_nodes
        ec_array = initial_connections

        random_mutation_picker = random.randint(0, 2)
        # 1 = add connection
        # 2 = remove connection
        # 3 = change weight
        ec_string = "" #used to join connetions...
        print("MUTATING TYPE = " + str(random_mutation_picker))
        if random_mutation_picker == 0:
            #add a connection and corresponding weight
            #print("-----------------------")
            #print("ADDING CONNECTION")
            random_start_node = random.randint(start_node, end_node)
            random_end_node = random.randint(start_node, end_node)
            new_connection = "(`" + str(random_start_node) + "`)-[:`affects` {value:'0'}]->(`" + str(random_end_node) + "`)"
            ec_array.append(new_connection)
            weights.append('0.5')

        elif random_mutation_picker == 1 and len(ec_array) > 1:
            #remove a connection and corresponding weight
            #print("-----------------------")
            #print("REMOVING CONNECTION")
            index_to_remove = random.randint(0,len(ec_array)-1)
            del(ec_array[index_to_remove])
            del(weights[index_to_remove])

        else: #random_mutation_picker == 2:
            #get a random weight and change it
            #print("-----------------------")
            #print("UPDATING WEIGHT")
            index_to_mutate = random.randint(0,len(ec_array)-1)
            new_value = random.randint(-100,100)/100
            weights[index_to_mutate] = new_value
            print(weights[index_to_mutate])

        return (ec_array, weights)

    #1a) get an initial set of connections to start with
    def getInitialConnections(self):
        ec_1 = "(`1`)-[:`affects` {value:'0'}]->(`0`)" 
        ec_2 = "(`2`)-[:`affects` {value:'0'}]->(`0`)" 
        ec_3 = "(`3`)-[:`affects` {value:'0'}]->(`0`)"
        ec_4 = "(`3`)-[:`affects` {value:'0'}]->(`2`)"
        ec_5 = "(`3`)-[:`affects` {value:'0'}]->(`1`)"
        ec_6 = "(`2`)-[:`affects` {value:'0'}]->(`1`)"
        ec_7 = "(`2`)-[:`affects` {value:'0'}]->(`3`)"
        ec_8 = "(`1`)-[:`affects` {value:'0'}]->(`2`)"
        ec_9 = "(`1`)-[:`affects` {value:'0'}]->(`3`)"
        ec_10 = "(`3`)-[:`affects` {value:'0'}]->(`4`)" 
        ec_11 = "(`2`)-[:`affects` {value:'0'}]->(`4`)" 
        ec_12 = "(`1`)-[:`affects` {value:'0'}]->(`4`)" 
        ec_13 = "(`2`)-[:`affects` {value:'0'}]->(`5`)" 
        ec_14 = "(`1`)-[:`affects` {value:'0'}]->(`5`)" 
        ec_15 = "(`3`)-[:`affects` {value:'0'}]->(`5`)"   
        ec_array = [ec_1, ec_2, ec_3, ec_4, ec_5, ec_6, ec_7, ec_8, ec_9, ec_10, ec_11, ec_12, ec_13, ec_14, ec_15]
        return ec_array

    #1b)get the nodes for the FCM
    def getBaseNodes(self, model_id):
        create_cypher = ("CREATE "
        "(`0` :`Decide Good` {modelId:'" + model_id + "',goal:'good',description:'good'}) , "
        "(`1` :Prop1 {modelId:'" + model_id + "',goal:'property1',description:'property1'}) , "
        "(`2` :Prop2 {modelId:'" + model_id + "',goal:'property2',description:'property2'}) , "
        "(`3` :Prop3 {modelId:'" + model_id + "',goal:'property3',description:'property3'}) , "
        "(`4` :`Decide Bad` {modelId:'" + model_id + "',goal:'bad',description:'bad'}) , "
        "(`5` :`Decide Neutral` {modelId:'" + model_id + "',goal:'neutral',description:'neutral'}) , ")
        return create_cypher

    #1c) get initial weights for everyone
    def getInitialWeights(self):
        return [-0.5, 0.5, -0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0, 0.3, -0.3]

    #3i)-internal add weights to the connections,
    def addWeights(self, connections, weights):
        i = 0
        while i < len(connections):
            connections[i] = re.sub('value:\'\d*\.?\d+\'', 'value:\'' + str(weights[i]) + '\'', connections[i])
            i += 1
        return connections

    #3) combine the nodes, connections, and weights
    def putItTogether(self, connections, weights, nodes):
        #ec_string = ""
        connections = self.addWeights(connections, weights)
        nodes += ','.join(connections)
        return nodes

    #example method that puts it all together
    def mutateFCM(self, model_id):
        #initialize everything
        #model_id = "7575"
        connections = getInitialConnections()
        weights = getInitialWeights()
        nodes = getBaseNodes(model_id)

        for x in range(10):
            evolved = evolveCypher("4545", weights, connections)
            weights = evolved[1]
            connections = evolved[0]
            evolved_cypher = putItTogether(connections, weights, nodes)
            print(evolved_cypher)    