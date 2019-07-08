from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule, TextElement
from mesa.visualization.UserParam import UserSettableParameter

from radartaskfcm.model import RadarTask

# Red
COOPERATIVE_COLOR = "#FF3C33"

def radar_portrayal(agent):
    if agent is None:
        return

    portrayal = {}
    portrayal["Shape"] = "circle"
    portrayal["r"] = .5
    portrayal["Layer"] = 0
    portrayal["Filled"] = "true"
    color = COOPERATIVE_COLOR

    return portrayal

# dictionary of user settable parameters - these map to the model __init__ parameters
model_params = {
    "use_team": UserSettableParameter('checkbox', 'Use Team', True)
                }

# set the portrayal function and size of the canvas for visualization
canvas_element = CanvasGrid(radar_portrayal, 20, 20, 500, 500)

# map data to chart in the ChartModule
chart_element = ChartModule([{"Label": "Wrong", "Color": COOPERATIVE_COLOR},
                                {"Label": "Correct", "Color": "#11FF44"}],
                                data_collector_name='datacollector'
                                )

# create instance of Mesa ModularServer
server = ModularServer(RadarTask, [canvas_element, chart_element],
                       "Radar Task",
                       model_params=model_params
                       )