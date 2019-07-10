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

# parameter lists for each parameter to be tested in batch run
br_params = {"use_team": [False, False, False] }

br = BatchRunner(RadarTask,
                 br_params,
                 iterations=1,
                 max_steps=100,
                 model_reporters={"Data Collector": lambda m: m.datacollector})

if __name__ == '__main__':
    br.run_all()
    br_df = br.get_model_vars_dataframe()
    br_step_data = pd.DataFrame()
    for i in range(len(br_df["Data Collector"])):
        if isinstance(br_df["Data Collector"][i], DataCollector):
            i_run_data = br_df["Data Collector"][i].get_model_vars_dataframe()
            br_step_data = br_step_data.append(i_run_data, ignore_index=True)
    br_step_data.to_csv("radar_batch.csv")
    #TODO I need to inspect this dataframe to get a better chart
    plt.plot(br_step_data)
    plt.show()

