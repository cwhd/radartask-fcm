from radartaskfcm.model import RadarTask
import itertools
from mesa import Model
from mesa.batchrunner import BatchRunner
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
from mesa.time import RandomActivation
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def get_df_name(df):
    name =[x for x in globals() if globals()[x] is df][0]
    return name

# NOTE change these to update the model that gets run. The possible options are the in the comments.
structure_type = "Team" #Hierarchy Team
info_type = "blocked" #distributed blocked

# these are the model params, tweak them to run different models
#br_params = {"use_team": [False], "info_type":[info_type] }
br_params = {"use_team": [True], "info_type":[info_type] }

'''
30 iterations:
correct: 17
Wrong: 13
percent correct: 0.5666666666666667
'''
#they only get 30 tries for the task
br = BatchRunner(RadarTask,
                 br_params,
                 iterations=3,
                 max_steps=200,
                 model_reporters={"Data Collector": lambda m: m.datacollector})

if __name__ == '__main__':
    print('--------------------------------------------------------------')
    print('TALLY HO')
    print('--------------------------------------------------------------')
    br.run_all()
    br_df = br.get_model_vars_dataframe()
    br_step_data = pd.DataFrame()
    for i in range(len(br_df["Data Collector"])):
        if isinstance(br_df["Data Collector"][i], DataCollector):
            i_run_data = br_df["Data Collector"][i].get_model_vars_dataframe()
            #print("IRUNDATA")
            #print(i_run_data)
            br_step_data = br_step_data.append(i_run_data, ignore_index=True)

    br_step_data.to_csv("radar_" + structure_type + "_" + info_type + ".csv")
    br_step_data.plot.xlabel = 'Ticks'
    #br_step_data.plot.line(title='Hierarcy Distributed and Blocked')
    br_step_data.plot.line(title=structure_type + ' ' + info_type)
    total_correct = br_step_data['Correct'][len(br_step_data) - 1]
    total_wrong = br_step_data['Incorrect'][len(br_step_data) - 1]

    #total_hostile_wrong = br_step_data['HostileIncorrect'][len(br_step_data) - 1]
    #total_friendly_wrong = br_step_data['FriendlyIncorrect'][len(br_step_data) - 1]
    #total_neutral_wrong = br_step_data['NeutralIncorrect'][len(br_step_data) - 1]

    percent_correct = total_correct / (total_correct + total_wrong)
    print('Correct: ' + str(total_correct))
    print('Incorrect: ' + str(total_wrong))
    print('percent correct: ' + str(percent_correct))

    #print('HostileIncorrect: ' + str(total_hostile_wrong))
    #print('FriendlyIncorrect: ' + str(total_friendly_wrong))
    #print('NeutralIncorrect correct: ' + str(total_neutral_wrong))

    print(': ' + str(percent_correct))
    plt.xlabel('Iterations')
    plt.ylabel('Count')

    plt.show()