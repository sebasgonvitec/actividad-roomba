from mesa import Model, agent
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
from agent import RoombaAgent, ObstacleAgent, TrashAgent

class RoombaModel(Model):
    """
    Creates a new model with Roomba agents.
    Args:
        N: Number of Roomba agents
        height, width: Size of the grid
    """
    def __init__(self, N, width, height):
        self.num_agents = N
        self.grid = MultiGrid(width, height, torus=False)
        self.schedule = RandomActivation(self)
        self.running = True

        self.datacollector = DataCollector( 
        agent_reporters={"Steps": lambda a: a.steps_taken if isinstance(a, RoombaAgent) else 0})

        # Create borders for the grid
        border = [(x,y) for y in range(height) for x in range(width) if y in [0, height-1] or x in [0, width - 1]]
        
        for pos in border:
            obs = ObstacleAgent(pos, self)
            # self.schedule.add(obs)
            self.grid.place_agent(obs, pos)

        # Add the agent to the starting cell
        for i in range(self.num_agents):
            a = RoombaAgent(i, self)
            self.schedule.add(a)

            # pos_gen = lambda w, h: (self.random.randrange(w), self.random.randrange(h))
            # pos = pos_gen(self.grid.width, self.grid.height)
            # while (not self.grid.is_cell_empty(pos)):
            #     pos = pos_gen(self.grid.width, self.grid.height)
            # self.grid.place_agent(a, pos)
            self.grid.place_agent(a, (1,1))

        self.datacollector.collect(self)
        # Add the trash to a random empty grid cell

    def step(self):
        '''Advance the model by one step.'''
        self.schedule.step()
        self.datacollector.collect(self)