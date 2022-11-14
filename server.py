from model import RoombaModel, ObstacleAgent, TrashAgent, RoombaAgent
from mesa.visualization.modules import CanvasGrid, BarChartModule, PieChartModule
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter

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

model_params = {"N":UserSettableParameter("slider", "Roomba Num", 10, 1, 50, 1), "trash_rate": UserSettableParameter("slider", "Trash Rate", 0.5, 0.1, 1, 0.01), "width":10, "height":10}

grid = CanvasGrid(agent_portrayal, 10, 10, 500, 500)

bar_chart = BarChartModule(
    [{"Label":"Steps", "Color":"#cf3e3e"}],
    scope ="agent", sorting="ascending", sort_by="Steps")

pie_chart = PieChartModule(
    [{"Label": "Clean", "Color": "#cdcbd4"}, {"Label": "Trash", "Color": "green"}, ]
)

server = ModularServer(RoombaModel, [grid, pie_chart, bar_chart], "Roomba Agent", model_params)

server.port = 8521 # The default
server.launch()

