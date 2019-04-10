"""
Maze Agent Base Class
---------------------
agent_base.py

"""

class Maze:
    """
    # - wall
    . - floor
    S - start
    E - end
    * - agent path
    """

    def __init__(self):
        file = open("mazes.txt", "r")
        self.mazes = []
        lines = file.readlines()
        i = 0
        while i < len(lines):
            line = lines[i].rstrip()
            if line == '': 
                i += 1
                continue
            maze = {}
            # First line of maze - width height
            maze['w'] = int(line.split(' ')[0])
            maze['h'] = int(line.split(' ')[1])
            mapLines = []
            for x in range(maze['h']):
                i += 1
                line = lines[i].rstrip()
                mapLines.append(list(line))
            maze['map'] = mapLines
            self.mazes.append(maze)
            i += 1

        print(self.mazes)
        file.close()

maze = Maze()

class UpdatePathError(Exception):
    """Errors in updating the path
    """
    pass

class Agent:
    '''Base class for intelligent agents'''

    def __init__(self, team, environment):
        self.percepts = []
        self.team = team
        self.environment = Environment(environment.width, environment.height)
        # self.nextMove = (0, 0, 0)
        # self.available_moves = []
        # self.lastMove = (0, 0, 0)


        self.available_moves = []
        self.new_pos = None
        self.last_pos = None
        
        self.path = []

    def update_path (self, new_pos, last_pos):
        """Update the current maze path
        
        Parameters
        ----------
        new_pos: tuple(row,col)
            the new position in the maze
        last_pos: tuple(row,col)
            the previous position in the maze   
        """
        #Bounds checking
        if not(abs(new_pos[0] - last_pos[0]) <= 1 and \
               abs(new_pos[1] - last_pos[1]) <= 1):
            #--start if
            print(new_pos[0] - last_pos[0], new_pos[1] - last_pos[1])
            raise UpdatePathError("new_pos, and last_pos are too far apart")
        if abs(new_pos[0] - last_pos[0]) == 1 and \
           abs(new_pos[1] - last_pos[1]) == 1:
            #--start if
            raise UpdatePathError("Cannot move diagonally.")

        # insert in to the path with the ability to specify where 
        # its coming from
        if last_pos in self.path: 
            index = self.path.index(last_pos)
            self.path = self.path[:index+1] + [new_pos]
        else: ## this should only add the first item
            self.path += [new_pos]
     


    def sense(self, percepts, environment):
        '''process environment percepts'''
        self.percepts.append(percepts)

        # percepts contain the available move choices
        self.availableMoves = environment.getPossibleMoves()
        # self.lastMove = environment.lastMove
        # if self.lastMove[2] != 0:
        #     self.environment.put(
        #         self.lastMove[0], self.lastMove[1], self.lastMove[2])

    def think(self):
        '''think about what action to take'''
        # print("thinking...rattle, rattle, rattle")

    def action(self):
        '''return action agent decided on'''
        # return self.nextMove
        self.update_path(self.new_pos, self.last_pos)
