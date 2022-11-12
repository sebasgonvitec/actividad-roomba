from mesa import Model, agent
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
from agent import Roomba, ObstacleAgent, TrashAgent

class RoombaModel(Model):
    """
    Creates a new model with Roomba agents.
    Args:
        N: Number of Roomba agents
        height, width: Size of the grid
    """
    
