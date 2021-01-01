"""
A sliding puzzle is a combination puzzle that challenges a player to slide (frequently flat) pieces along certain routes (usually on a board) to establish a certain end-configuration.

Your goal for this kata is to write a function that produces a sequence of tile movements that solves the puzzle.

Input
An n x n array/list comprised of integer values ranging from 0 to n^2 - 1 (inclusive), which represents a square grid of tiles. Note that there will always be one empty tile (represented by 0) to allow for movement of adjacent tiles.

Output
An array/list comprised of any (but not necessarily all) of the integers from 1 to n^2 - 1, inclusive. This represents the sequence of tile moves for a successful transition from the initial unsolved state to the solved state. If the puzzle is unsolvable, return null(JavaScript, Java, PHP) or None(Python) or the vector {0} (C++).

Test Example
simple_example = [
    [ 1, 2, 3, 4],
    [ 5, 0, 6, 8],
    [ 9,10, 7,11],
    [13,14,15,12]
]
slide_puzzle(simple_example) #[6,7,11,12]

# TRANSITION SEQUENCE:
[ 1, 2, 3, 4]    [ 1, 2, 3, 4]    [ 1, 2, 3, 4]    [ 1, 2, 3, 4]    [ 1, 2, 3, 4]
[ 5, 0, 6, 8]    [ 5, 6, 0, 8]    [ 5, 6, 7, 8]    [ 5, 6, 7, 8]    [ 5, 6, 7, 8]
[ 9,10, 7,11] -> [ 9,10, 7,11] -> [ 9,10, 0,11] -> [ 9,10,11, 0] -> [ 9,10,11,12]
[13,14,15,12]    [13,14,15,12]    [13,14,15,12]    [13,14,15,12]    [13,14,15, 0]

# NOTE: Your solution does not need to follow this exact sequence to pass
Technical Details
Input will always be valid.
The range of values for n are: 10 >= n >= 3
If you enjoyed this kata, be sure to check out my other katas.
"""

from heapq import heappop, heappush
from copy import deepcopy
import time

def make_scorer(ar, ix=100):
    n = len(ar[0]) # assume ar is valid
    coordinates = [(i,j) for i in range(n) for j in range(n)][:-1]
    locations = {n+1:coordinates[n] for n in range(len(coordinates)) if n+1<=ix}
    def scorer(arg):
        score = 0
        for i in range(n):
            for j in range(n):
                number = arg[i][j]
                if number in locations:
                    row, col = locations[number]
                    score += abs(i-row) + abs(j-col)
        return 2*score
    return scorer

class PQueue():
    def __init__(self):
        self._container = []

    def pop(self):
        return heappop(self._container)

    def push(self, item):
        heappush(self._container, item)

    def __repr__(self):
        return repr(self._container)

    @property
    def empty(self):
        return not self._container


class Node(): #holds a state of the puzzle
    def __init__(self, config, cost, score, parent = None, mymove = None):
        self.config = config
        self.size = len(config)
        self.cost = cost
        self.score = score
        self.children = []
        self.parent = parent
        self.mymove = mymove

    def get_moves(self, movelist):
        for i in range(self.size):
            for j in range(self.size):
                if self.config[i][j] == 0:
                    i0=i
                    j0=j
        return [self.config[i][j] for i,j in movelist[i0,j0]]

    def get_sequence(self):
        yield self.mymove
        if self.parent:
            yield from self.parent.get_sequence()

    def report_sequence_to_me(self):
        sequence = [each for each in self.get_sequence()][::-1]
        return sequence        

    def __lt__(self, other):
        return (self.score+self.cost) < (other.score+other.cost)
        # return (self.score) < (other.score)

    def __repr__(self):
        return repr(self.config)


class Puzzle(): #holds the puzzle initial state and all nodes, scores and makes new nodes
    def __init__(self, ar):
        self.nodes = [] #PQueue()
        self._initial_state = ar
        self.size = len(ar)
        self._calculate_moves()
        self._scorer = make_scorer(ar)
        self.make_node(ar,0)     

    def _calculate_moves(self):
        moves_by_location = {}
        for i in range(self.size):
            for j in range(self.size):
                moves = []
                imoves = [ii for ii in [i-1,i+1] if ((ii >= 0) and (ii < self.size))]
                jmoves = [jj for jj in [j-1,j+1] if ((jj >= 0) and (jj < self.size))]
                moves = moves + [(i,jj) for jj in jmoves] + [(ii,j) for ii in imoves]
                moves_by_location[i,j] = moves
        self.moves = moves_by_location

    def make_node(self, config, cost, parent=None, mymove=None):
        score = self._scorer(config)
        node = Node(config,cost,score, parent=parent, mymove=mymove)
        self.nodes.append(node)
        return node

    def get_children(self, node):
        if node.children:
            return node.children
        moves = node.get_moves(self.moves)
        ar = node.config
        nodes = []
        for move in moves:
            newar = deepcopy(ar)
            for i in range(len(newar)):
                for j in range(len(newar)):
                    if newar[i][j] == 0:
                        newar[i][j] = move
                    elif newar[i][j] == move:
                        newar[i][j] = 0
            newcost = node.cost + 1
            newnode = self.make_node(newar, newcost, parent=node, mymove=move)
            nodes.append(newnode)
        return nodes


def astar(puzzle: Puzzle):
    frontier = PQueue() # where we will search next
    explored = {} # have we searched this node? if so, what is its cost?
    impossible = False # if the cost exceeds n*n, its probably impossible
    solution = []
    #initialize the frontier
    frontier.push(puzzle.nodes[0])
    steps=0
    explored[str(puzzle.nodes[0].config)]=0
    lowscore = 200
    while (not frontier.empty) and (not impossible):
        current_node: Node = frontier.pop()
        if current_node.score == 0:            
            return current_node.report_sequence_to_me()[1:], current_node.config
        new_nodes = puzzle.get_children(current_node)
        for new_node in new_nodes:
            if (str(new_node.config) not in explored) or (new_node.cost < explored[str(new_node.config)]):
                explored[str(new_node.config)] = new_node.cost
                frontier.push(new_node)                
    return None

def solve_slider(ar):
    # will use astar as a series of steps
    puzzle = Puzzle(ar)
    solution,_ = astar(puzzle)
    return solution
    

def astar_race(puzzle: Puzzle, puzzle_bad: Puzzle):
    frontier = PQueue() # where we will search next
    frontier_bad = PQueue() # where we will search next on the broken puzzle
    explored = {} # have we searched this node? if so, what is its cost?
    explored_bad = {}
    impossible = False # if the cost exceeds n*n, its probably impossible
    impossible_bad = False
    solution = []
    #initialize the frontiers
    frontier.push(puzzle.nodes[0])
    frontier_bad.push(puzzle_bad.nodes[0])
    explored[str(puzzle.nodes[0].config)]=0
    explored_bad[str(puzzle_bad.nodes[0].config)]=0
    while (not frontier.empty) and (not impossible):
        current_node: Node = frontier.pop()
        if current_node.score == 0:
            return current_node.report_sequence_to_me()[1:]
        new_nodes = puzzle.get_children(current_node)
        for new_node in new_nodes:
            if (str(new_node.config) not in explored) or (new_node.cost < explored[str(new_node.config)]):
                explored[str(new_node.config)] = new_node.cost
                frontier.push(new_node)
        # bad puzzle loop. if this solves, the original is unsolvable
        current_node: Node = frontier_bad.pop()
        if current_node.score == 0:
            return None
        new_nodes = puzzle_bad.get_children(current_node)
        for new_node in new_nodes:
            if (str(new_node.config) not in explored_bad) or (new_node.cost < explored_bad[str(new_node.config)]):
                explored_bad[str(new_node.config)] = new_node.cost
                frontier_bad.push(new_node)
    return None

def best_first(ar, puzzle: Puzzle): # must modify __lt__ in Nodes! not ideal, i know...
    frontier = PQueue() # where we will search next
    explored = [] # have we searched this node? 
    impossible = False # if the cost exceeds n*n, its probably impossible
    solution = []
    #initialize the frontier
    frontier.push(puzzle.nodes[0])
    steps=0
    while (not frontier.empty) and (not impossible):
        current_node: Node = frontier.pop()
        steps+=1
        if steps > 10000000:
            impossible = True
        if (current_node not in explored):
            if current_node.score == 0:
                return current_node.report_sequence_to_me()[1:]
            else:
                explored.append(current_node)
                new_nodes = puzzle.get_children(current_node)
                for new_node in new_nodes:
                    frontier.push(new_node)
    return None
      
def slide_puzzle(ar):
    # puzzle = Puzzle(ar)
    # solution = astar(puzzle)
    solution = solve_slider(ar)
    # solution = best_first(ar, puzzle)
    return solution


if __name__ == "__main__":
    puzzle1 = [
        [4,1,3],
        [2,8,0],
        [7,6,5]
    ]
    puzzle2 = [
        [10, 3, 6, 4],
        [ 1, 5, 8, 0],
        [ 2,13, 7,15],
        [14, 9,12,11]
    ]
    puzzle21 = [
        [3, 10, 6, 4],
        [ 1, 5, 7, 0],
        [ 2,13, 8,15],
        [14, 9,12,11]
    ]
    puzzle22 = [
        [3, 10, 6, 4],
        [ 1, 5, 8, 0],
        [ 2,13, 7,15],
        [14, 9,12,11]
    ] 
    puzzle3 = [
        [ 3, 7,14,15,10],
        [ 1, 0, 5, 9, 4],
        [16, 2,11,12, 8],
        [17, 6,13,18,20],
        [21,22,23,19,24]
    ]
    puzzle4 = [
        [ 0,2,3,4,5],
        [ 1,7,8,9,10],
        [6,12,13,14,15],
        [11,17,18,19,20],
        [16,21,22,23,24]
    ]
    n = Node(puzzle1,0,0)
    # print(n,n.get_moves())
    # puz = Puzzle(puzzle1)
    # print(puz.nodes[0])
    # print(puzzle1,slide_puzzle(puzzle1))
    # print(puzzle2,slide_puzzle(puzzle2))
    # print(puzzle21,slide_puzzle(puzzle21))
    # print(puzzle22,slide_puzzle(puzzle22))
    # print(puzzle3,slide_puzzle(puzzle3))
    # print(puzzle4,slide_puzzle(puzzle4))
    start = time.time()
    for puz in [puzzle1,puzzle2,puzzle3,puzzle4]:
        slide_puzzle(puz)
    end = time.time()
    print(f"Time for heuristic = {end-start}")
    start = time.time()
    for puz in [puzzle1,puzzle2,puzzle3,puzzle4]:
        puzzle = Puzzle(puz)
        astar(puzzle)
    end = time.time()
    for puz in [puzzle1,puzzle2,puzzle3,puzzle4]:
        puzzle = Puzzle(puz)
        result,_ = astar(puzzle)
        result2 = slide_puzzle(puz)
        print(result==result2)
    
    print(f"Time for astar = {end-start}")
    
