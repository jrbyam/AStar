"""
A* Search HW - path finding agents
---------------------
hw2.py

"""
import numpy as np
import copy

class Maze:
    """
    # - wall
    . - floor
    S - start
    E - end
    * - agent path
    """

    def __init__(self, width, height, maze_map):
        self.width = width
        self.height = height
        self.map = maze_map

    def get(self, position):
        return self.map[position[0]][position[1]]

    def getStartLoc(self):
        """
        gets the start location
        """
        i = np.where(np.array(self.map) == 'S')
        return (i[0][0],i[1][0])

    def getEndLoc(self):
        i = np.where(np.array(self.map) == 'E')
        return (i[0][0],i[1][0])

    def getPossibleMoves(self, position):
        if self.get(position) not in ['.', 'S']:
            raise UpdatePathError('Current position not valid.')

        legalNext = ['.', 'E',]
        moves = []
        row = position[0]
        col = position[1]
        if self.map[row - 1][col] in legalNext: # Top
            moves.append( (row - 1, col) )
        if self.map[row][col + 1] in legalNext: # Right
            moves.append( (row, col + 1) )
        if self.map[row + 1][col] in legalNext: # Bottom
            moves.append( (row + 1, col) )
        if self.map[row][col - 1] in legalNext: # Left
            moves.append( (row, col - 1) )

        return moves

    def print_path(self, path):
        # m = copy.deepcopy(self.map)
        # print(m)
        s = ""
        for rx, row in enumerate(self.map):
            for cx, col in enumerate(row):
                if len(path) > 0 and (rx,cx) == path[-1]:
                    # print(rx,cx)
                    s += '&'
                elif (rx,cx) in path:
                    s += '*'
                else:
                    s += col
            s += '\n'

        print (s)
            
        

class Environment:
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
            w = int(line.split(' ')[0])
            h = int(line.split(' ')[1])
            maze_map = []
            for _ in range(h):
                i += 1
                line = lines[i].rstrip()
                maze_map.append(list(line))
            maze = Maze(w, h, maze_map)
            self.mazes.append(maze)
            i += 1

        file.close()

class UpdatePathError(Exception):
    """Errors in updating the path
    """
    pass

class Agent:
    '''Base class for intelligent agents'''

    def __init__(self, maze):
        self.percepts = []
        self.maze = maze
        # self.nextMove = (0, 0, 0)
        # self.available_moves = []
        # self.lastMove = (0, 0, 0)


        self.available_moves = []
        self.new_pos = None
        self.last_pos = None
        self.current_pos = None
        
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
            # print(new_pos[0] - last_pos[0], new_pos[1] - last_pos[1])
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
     


    def sense(self, percepts, maze):
        '''process maze percepts'''
        self.percepts.append(percepts)

        # percepts contain the available move choices
        self.available_moves = maze.getPossibleMoves(self.current_pos)
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
        self.current_pos = self.new_pos

class RAWS(Agent):
    """Rawser's agent with snake
    """
    def __init__ (self, maze):
        super().__init__(maze)
        self.open_set = set()
        self.closed_set = set()
        
        self.paths_to = {}

        
        start = self.maze.getStartLoc()
        end = self.maze.getEndLoc()
        self.open_set.add(start)
        self.g_score = {start: 0}
        self.paths_to[start] = []
        self.f_score = {start: self.get_snake_dist(start,end)}
        self.current_pos = start

    def break_cond(self):
        """
        is there a special break condition
        """
        return len(self.open_set) == 0

    def get_snake_dist(self, start, end):
        return abs(start[0]-end[0]) +  abs(end[1]-end[1]) 

    def think(self):
        current = self.current_pos
        # input()
        # print(self.current_pos, self.available_moves)
        # maze.print_path(self.path)
        self.new_pos = self.available_moves[0]
        goal = self.maze.getEndLoc()
        
        low_score = self.g_score[current] + self.get_snake_dist(current, self.new_pos) + self.get_snake_dist(self.new_pos, goal)
        
        self.open_set.remove(current)
        self.closed_set.add(current)
       

        for neighbor in self.available_moves:
            if neighbor in self.closed_set:
                continue #Ignore the neighbor which is already evaluated.

            # The distance from start to a neighbor
            tentative_score = self.g_score[current] + self.get_snake_dist(current, neighbor)

            if neighbor not in self.open_set:	#Discover a new node
                self.open_set.add(neighbor)
            elif tentative_score >= self.g_score[neighbor]:
                continue

            # This path is the best until now. Record it!
            # cameFrom[neighbor] := current
            self.paths_to[neighbor] = self.paths_to[current] +[neighbor]
            
            self.g_score[neighbor] = tentative_score
            self.f_score[neighbor] = self.g_score[neighbor] + self.get_snake_dist(neighbor, goal)
            if self.f_score[neighbor] <= low_score:
                low_score = self.g_score[neighbor]
                self.new_pos = neighbor
        self.last_pos = self.current_pos

    def action(self):
        '''return action agent decided on'''
        super().action()
        os = list(self.open_set)
        self.current_pos = os[0]
        ms = self.f_score[os[0]]
        for i in os:
            if self.f_score[i] <= ms:
                ms = self.f_score[i]
                self.current_pos = i

# The simulation code:
environment = Environment()

for maze in environment.mazes:
    raws = RAWS(maze)
    while raws.current_pos != maze.getEndLoc():
        if raws.break_cond():
            break
        raws.sense([],maze)
        raws.think()
        raws.action()
        raws.path = raws.paths_to[raws.current_pos]
    print("RAWS summary:")
    print("length", len(raws.path))
    # print(raws.path)
    maze.print_path(raws.path)

    pass
    # Solve each maze with each kind of agent and print out results
