from model import RoombaModel, ObstacleAgent, TrashAgent, RoombaAgent
from mesa.visualization.modules import CanvasGrid, BarChartModule
from mesa.visualization.ModularVisualization import ModularServer

def agent_portrayal(agent):
    if agent is None: return

    portrayal = {"Shape": "circle",
                 "Filled": "true",
                 "Layer": 0,
                 "Color": "red",
                 "r": 0.5}

    if(isinstance(agent, ObstacleAgent)):
        portrayal["Color"] = "black"
        portrayal["Layer"] = 1
        portrayal["r"] = 0.2

    if(isinstance(agent, TrashAgent)):
        portrayal["Color"] = "green"
        portrayal["Layer"] = 1
        portrayal["r"] = 0.2

    return portrayal

model_params = {"N":5, "width":10, "height":10}

grid = CanvasGrid(agent_portrayal, 10, 10, 500, 500)
bar_chart = BarChartModule(
    [{"Label":"Steps", "Color":"#AA0000"}],
    scope ="agent", sorting="ascending", sort_by="Steps")

server = ModularServer(RoombaModel, [grid, bar_chart], "Roomba Agent", model_params)

server.port = 8521 # The default
server.launch()

