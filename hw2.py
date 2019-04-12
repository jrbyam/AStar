"""
A* Search HW - path finding agents
---------------------
hw2.py

"""

import collections

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

        for i in range(self.height):
            for j in range(self.width):
                if self.map[i][j] == 'S':
                    self.start = (i, j)
                elif self.map[i][j] == 'E':
                    self.end = (i, j)

    def get(self, position):
        return self.map[position[0]][position[1]]
    
    def getPossibleMoves(self, position):
        if self.get(position) not in ['.', 'S']:
            raise UpdatePathError('Current position not valid.')

        legalNext = ['.', 'E']
        moves = []
        row = position[0]
        col = position[1]
        if self.map[row - 1][col] in legalNext: # Top
            moves.append((row - 1, col))
        if self.map[row][col + 1] in legalNext: # Right
            moves.append((row, col + 1))
        if self.map[row + 1][col] in legalNext: # Bottom
            moves.append((row + 1, col))
        if self.map[row][col - 1] in legalNext: # Left
            moves.append((row, col - 1))

        return moves

    def getNextMoves(self, last_position, current_position):
        if self.get(current_position) not in ['.', 'S']:
            raise UpdatePathError('Current position not valid.')

        legalNext = ['.', 'E']
        moves = []
        row = current_position[0]
        col = current_position[1]
        if self.map[row - 1][col] in legalNext and not (last_position[0] == row - 1 and last_position[1] == col): # Top
            moves.append((row - 1, col))
        if self.map[row][col + 1] in legalNext and not (last_position[0] == row and last_position[1] == col + 1): # Right
            moves.append((row, col + 1))
        if self.map[row + 1][col] in legalNext and not (last_position[0] == row + 1 and last_position[1] == col): # Bottom
            moves.append((row + 1, col))
        if self.map[row][col - 1] in legalNext and not (last_position[0] == row and last_position[1] == col - 1): # Left
            moves.append((row, col - 1))

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
        self.current_pos = self.maze.start
        self.last_pos = self.maze.start
        self.new_pos = None
        
        self.path = []
        self.ic = 0
        self.step_x_step = False


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
        self.current = new_pos
     


    def sense(self, percepts):
        '''process maze percepts'''
        self.percepts.append(percepts)

        # percepts contain the available move choices
        self.available_moves = self.maze.getPossibleMoves(self.current_pos)
        # self.lastMove = environment.lastMove
        # if self.lastMove[2] != 0:
        #     self.environment.put(
        #         self.lastMove[0], self.lastMove[1], self.lastMove[2])

    def think(self):
        '''think about what action to take'''
        # print("thinking...rattle, rattle, rattle")
        # Override to set new_pos and last_pos?

    def action(self):
        '''return action agent decided on'''
        # return self.nextMove
        self.update_path(self.new_pos, self.last_pos)
        self.current_pos = self.new_pos

class BreadthFirstAgent(Agent):
    def __init__(self, maze):
        super().__init__(maze)

    def solve_maze(self):
        frontier = [ [ self.maze.start ] ]
        explored = [ ]
        
        found_path = []
        no_skip = True
        while (True):
            if len(frontier) == 0:
                raise UpdatePathError("No valid path found.")
            path = frontier.pop(0)
            if self.step_x_step and no_skip:

                inp = input()
                if inp == "skip":
                    no_skip = False
                print ("BFS iteration:", self.ic, ". Current path length:", len(path))
                
                self.maze.print_path(path)
            self.ic += 1
            explored.append(path)
            node = path[-1]
            node_before = (-1, -1)
            if len(path) > 1: node_before = path[-2]
            if self.maze.get(node) == 'E':
                found_path = path
                break # End found
            children = self.maze.getNextMoves(node_before, node)
            for child in children:
                new_path = list(path)
                new_path.append(child)
                frontier.append(new_path)
        
        print("BFS Summary:")
        print("iterations", self.ic)
        print("length", len(found_path))
        print("length/iterations:", len(found_path)/self.ic)
        self.maze.print_path(found_path)

class DepthFirstAgent(Agent):
    def __init__(self, maze):
        super().__init__(maze)

    def solve_maze(self):
        frontier = [ self.maze.start ]
        explored = [ ]

        end = tuple()
        parentMap = { self.maze.start: None }
        while (True):
            if len(frontier) == 0:
                raise UpdatePathError("No valid path found.")
            if self.step_x_step and False: # self.path is not being updated so don't do step x step
                input()
                print ("DFS iteration:", self.ic, ". Current path length:", len(self.path))
                self.maze.print_path(self.path)
            self.ic += 1
            node = frontier.pop(len(frontier) - 1)
            explored.append(node)
            if self.maze.get(node) == 'E':
                end = node
                break # End found
            children = self.maze.getPossibleMoves(node)
            for child in children:
                if child not in frontier and child not in explored:
                    frontier.append(child)
                    parentMap[child] = node
        
        # Build path after end node found
        found_path = []
        while (end != None):
            found_path = [end] + found_path
            end = parentMap[end]

        print("DFS Summary:")
        print("iterations", self.ic)
        print("length", len(found_path))
        print("length/iterations:", len(found_path)/self.ic)
        self.maze.print_path(found_path)

class RAWS(Agent):
    """Rawser's agent with snake
    """
    def __init__ (self, maze):
        super().__init__(maze)
        self.open_set = set()
        self.closed_set = set()
        
        self.paths_to = {}
        self.no_skip = True
        self.open_set.add(maze.start)
        self.g_score = { maze.start: 0 }
        self.paths_to[maze.start] = []
        self.f_score = { maze.start: self.get_snake_dist(maze.start, maze.end) }
        self.current_pos = maze.start
        
    def break_cond(self):
        """
        is there a special break condition
        """
        return len(self.open_set) == 0

    def get_snake_dist(self, start, end):
        return abs(start[0]-end[0]) +  abs(end[1]-end[1]) 

    def think(self):
        current = self.current_pos
        
        
        if self.step_x_step and self.no_skip: 
            inp = input()
            # print(self.current_pos, self.available_moves)
            print ("RAWS iteration:", self.ic, ". Current path length:", len(self.path))
            maze.print_path(self.path)
            if inp == "skip":
                print ('skip')
                self.no_skip = False
        self.ic += 1
        
        self.new_pos = self.available_moves[0]
        goal = self.maze.end
        
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

    def solve_maze(self):
        s = ""
        try:
            while self.current_pos != maze.end:
                if self.break_cond():
                    break
                self.sense([])
                self.think()
                self.action()
                self.path = self.paths_to[self.current_pos]
        except IndexError: 
            # print("RAWS No Path found")
            s = "Does not reach goal"
            pass
        print("RAWS summary:")
        print("iterations", self.ic)
        print("length", len(self.path), s)
        print("length/iterations:", len(self.path)/self.ic)
        maze.print_path(self.path)

# The simulation code:
import sys

step_x_step = False
if len(sys.argv) == 2:
    step_x_step = True 


environment = Environment()
for mix, maze in enumerate(environment.mazes):
    # Solve each maze with each kind of agent and print out results
    print("Maze:" , mix)
    print(maze.print_path([]))
    print ("START: BFS agent")
    try:
        bfa = BreadthFirstAgent(maze)
        bfa.step_x_step = step_x_step
        bfa.solve_maze()
    except UpdatePathError:
        print("BFA no path found\n")
    
    print ("START: DFS agent")
    try:
        dfa = DepthFirstAgent(maze)
        dfa.step_x_step = step_x_step
        dfa.solve_maze()
    except UpdatePathError:
        print("DFA no path found\n")

    print ("START: Rawser's agent with snake")
    raws = RAWS(maze)
    raws.step_x_step = step_x_step
    raws.solve_maze()

    print('----------------\n\n')
    input()
    pass
