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
    def __init__(self, N, width, height):
        self.num_agents = N
        self.grid = MultiGrid(width, height, False)
        self.schedule = RandomActivation(self)
        self.running = True

        # Create borders for the grid
        border = [(x,y) for y in range(height) for x in range(width) if y in [0, height-1] or x in [0, width - 1]]
        
        for pos in border:
            obs = ObstacleAgent(pos, self)
            # self.schedule.add(obs)
            self.grid.place_agent(obs, pos)

        # Add the agent to the starting cell
        for i in range(self.num_agents):
            a = Roomba(i, self)
            self.schedule.add(a)
            self.grid.place_agent(a, (1,1))

        # Add the trash to a random empty grid cell

        def step(self):
            '''Advance the model by one step.'''
            self.schedule.step()
            self.datacollector.collect(self)