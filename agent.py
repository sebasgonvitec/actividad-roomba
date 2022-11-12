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
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,
            include_center=True)
        
        #Checks which grid cell is empty
        freeSpaces = list(map(self.model.grid.is_cell_empty, possible_steps))

        next_moves = [p for p, f in zip(possible_steps, freeSpaces) if f==True]

        next_move = self.random.choice(next_moves)
        print("Next move is: ", next_move)
        
        if self.random.random() < 0.1:
            self.model.grid.move_agent(self, next_move)
            self.steps_taken += 1

        # If the cell is empty, moves the agent to that cell; otherwise, it stays at the same position
        # if freeSpaces[self.direction]:
        #     self.model.grid.move_agent(self, possible_steps[self.direction])
        #     print(f"Se mueve de {self.pos} a {possible_steps[self.direction]}; direction {self.direction}")
        # else:
        #     print(f"No se puede mover de {self.pos} en esa direccion.")
        
    def step(self):
        """
        Determines the new direction it will take, and then moves
        """
        self.direction = self.random.randint(0,8)
        print(f"Agente: {self.unique_id} movimiento {self.direction}")
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