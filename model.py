from mesa import Model, agent
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
from agent import RoombaAgent, ObstacleAgent, TrashAgent

# TODO: Generate trash based on trash rate check
# TODO: Data collection and display 
# TODO: Test case: Two Roombas erase the same trash

class RoombaModel(Model):
    """
    Creates a new model with Roomba agents.
    Args:
        N: Number of Roomba agents
        height, width: Size of the grid
    """
    def __init__(self, trash_rate, N, width, height, steps):
        self.num_agents = N
        self.grid = MultiGrid(width, height, torus=False)
        self.schedule = RandomActivation(self)
        self.running = True
        self.steps = 0
        self.max_steps = steps

        self.datacollector = DataCollector( 
            model_reporters={"Trash": lambda m: self.count_trash(), "Clean": lambda c: self.count_clean()},
            agent_reporters={"Steps": lambda a: a.steps_taken if isinstance(a, RoombaAgent) else 0})
        

        # Create borders for the grid
        border = [(x,y) for y in range(height) for x in range(width) if y in [0, height-1] or x in [0, width - 1]]
        
        for pos in border:
            obs = ObstacleAgent(pos, self)
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

        # Fill cells with trash according to trash rate
        for i in range(1, self.grid.width-1):
            for j in range(1, self.grid.height-1):
                if self.random.random() < trash_rate:
                    trash = TrashAgent((i,j), self)
                    self.grid.place_agent(trash, (i,j))
                    
        self.datacollector.collect(self)

    def step(self):
        '''Advance the model by one step.'''
        self.schedule.step()
        self.datacollector.collect(self)
        self.steps+=1
        
        #Stop if there is no more trash left or step limit reached
        if self.count_trash() == 0 or self.steps >= self.max_steps-1:
            self.running = False


    def count_trash(self):
        """
        Helper method to count trash in a given model.
        """
        trash = 0
        for cell in self.grid.coord_iter():
            cell_content, x, y = cell
            for agent in cell_content:
                if isinstance(agent, TrashAgent):
                    trash += 1
        return trash
    
    def count_clean(self):
        return (self.grid.height-1)*(self.grid.width-1) - self.count_trash()

       





