from mesa import Agent

class RoombaAgent(Agent):
    """
    Agent that simulates the behaviour of a Roomba
    Attributes:
        unique_id: Agent's ID
        direction: Randomly chosen direction, from one of eight possible
    """
    def __init__(self, unique_id, model):
        """
        Creates a new Roomba agent
        Args:
            unique_id: Agent's ID
            model: Model reference for the target
        """
        super().__init__(unique_id, model)
        self.direction = 4
        self.steps_taken = 0
    
    def move(self):
        """ 
        Determines if the agent can move in the direction that was chosen
        """
        # Returns every surrounding cell
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,
            include_center=True)
        
        # Returns agents in each neighboring cell
        neighbor_agents = list(map(self.model.grid.get_cell_list_contents, possible_steps))
        
        # List to store the cells where there is no obstacle
        freeSpaces = []
        # Boolean to store if there is an agent in the cell
        isObstacle = False

        # For each cell, check if any existing agent is obstacle and append True or False accordingly
        for i in range(len(neighbor_agents)):
            for j in neighbor_agents[i]:
                if(isinstance(j, ObstacleAgent) or isinstance(j, RoombaAgent)):
                    isObstacle = True
            if(isObstacle):
                freeSpaces.append(False)
                isObstacle = False
            else:
                freeSpaces.append(True)

        #print(freeSpaces)

        next_moves = [p for p, f in zip(possible_steps, freeSpaces) if f==True]

        next_move = self.random.choice(next_moves)
        print("Next move is: ", next_move)
        
        if self.random.random() < 0.5:
            self.model.grid.move_agent(self, next_move)
            self.steps_taken += 1

        # If the cell is empty, moves the agent to that cell; otherwise, it stays at the same position
        # if freeSpaces[self.direction]:
        #     self.model.grid.move_agent(self, possible_steps[self.direction])
        #     print(f"Se mueve de {self.pos} a {possible_steps[self.direction]}; direction {self.direction}")
        # else:
        #     print(f"No se puede mover de {self.pos} en esa direccion.")

    def clean(self):
        """
        Cleans the trash in the cell
        """
        trash = self.model.grid.get_cell_list_contents([self.pos])
        for i in trash:
            if(isinstance(i, TrashAgent)):
                self.model.grid.remove_agent(i)
                
        print("Trash cleaned")

    def step(self):
        """
        Determines the new direction it will take, and then moves
        """
        self.direction = self.random.randint(0,8)
        #print(f"Agente: {self.unique_id} movimiento {self.direction}")
        self.clean()
        self.move()

class ObstacleAgent(Agent):
    """
    Obstacle agent. Just to add obstacles to the grid.
    """
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        pass  

class TrashAgent(Agent):
    """
    Trash agent. Just to add trash to the grid.
    """
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        pass