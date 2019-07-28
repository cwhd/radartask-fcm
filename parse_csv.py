import pandas as pd
import numpy as np

df = pd.read_csv('radar_Hierarchy_distributed_.csv')
#df = pd.read_csv('radar_Hierarchy_blocked_.csv')
#df = pd.read_csv('radar_team_blocked.csv')
#df = pd.read_csv('radar_team_distributed.csv')
#print(df)

#TODO parse every 30 rows to get the total for each interation
total_wright = 0
total_wrong = 0
for i in range(101):
    index_get = i * 30 - 1
    if index_get > 0:
        print('Iteration: ' + str(index_get))
        print('Correct: ' + str(df['Correct'][index_get]))    
        print('Wrong' + str(df['Wrong'][index_get]))
        total_wright += df['Correct'][index_get]
        total_wrong += df['Wrong'][index_get]

print('total correct: ' + str(total_wright))
print('total wrong: ' + str(total_wrong))
percent_correct = total_wright / (total_wright + total_wrong)

print('correct percentage: ' + str(percent_correct))
