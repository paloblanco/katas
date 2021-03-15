from typing import List

class Node():

    def __init__(self, row, column):
        self.row = row
        self.column = column
        self.neighbors = {
            0: None, #right, col + 1
            1: None, #down, row + 1
            2: None, #left, col - 1
            3: None, #up, row - 1
        }

    def __str__(self):
        str_node = ""
        for _,neighbor in self.neighbors.items():
            if neighbor:
                str_node += f"({neighbor[0].row}, {neighbor[0].column})  "
        val = f"({self.row}, {self.column}), neighbors are {str_node}"
        return val

    def __repr__(self):
        return self.__str__()

    def add_neighbor(self, other, direction, distance):
        self.neighbors[direction] = (other, distance)
        back_direction = (direction + 2)%4
        other.neighbors[back_direction] = (self, distance)

    def get_next(self, direction):
        neighbor = self.neighbors[direction]
        while not neighbor:
            direction = (direction - 1)%4
            neighbor = self.neighbors[direction]
        return neighbor[0], direction

    def get_frontier(self, direction):
        pass


class ShapeGraph():

    def __init__(self, shape):
        self.mapp = self.str_to_map(shape)
        self.build_graph()

    def build_shapes(self):
        self.shapes = []
        remaining_nodes = list(self.nodes.values())
        frontier = []
        frontier.append(remaining_nodes[0])
        remaining_nodes.remove(remaining_nodes[0])
        direction = 3
        while len(frontier) > 0:
            node = frontier.pop()
            shape = []
            shape.append(node)
            direction = (direction+1)%4
            neighbor, direction = node.get_next(direction)
            while neighbor != node:
                if neighbor in remaining_nodes: remaining_nodes.remove(neighbor)
                shape.append(neighbor)
                direction = (direction + 1)%4
                neighbor2, direction = neighbor.get_next(direction)
                next_node, next_direction = neighbor.get_next((direction-1)%4)
                if next_node in remaining_nodes:
                    frontier.append(next_node)
                    remaining_nodes.remove(next_node)
                neighbor = neighbor2
            self.shapes.append(shape)
    
    def get_shapes(self):
        self.build_shapes()
        return self.shapes

    def build_graph(self):
        self.nodes = {}
        self.add_all_nodes()
        self.add_all_edges()

    def __str__(self):
        val = ""
        for _,node in self.nodes.items():
            val += str(node) + "\n"
        return val

    def add_all_edges(self):
        self.checked_nodes = []
        for (row,col), node in self.nodes.items():
            self.add_neighbors(node,row,col)

    def add_neighbors(self,node,row,col):
        if node in self.checked_nodes: return
        self.checked_nodes.append(node)
        right_cell = self.mget(row, col+1)
        if right_cell == "+":
            distance = 1
            self.add_and_check_neighbor(node,row,col,distance,0)
        elif right_cell == "-":
            distance = 1
            while True:
                distance += 1
                right_cell = self.mget(row, col + distance)
                if right_cell == "+":
                    self.add_and_check_neighbor(node,row,col,distance,0)
                    break
        down_cell = self.mget(row+1, col)
        if down_cell == "+":
            distance = 1
            self.add_and_check_neighbor(node,row,col,distance,1)
        elif down_cell == "|":
            distance = 1
            while True:
                distance += 1
                down_cell = self.mget(row + distance, col)
                if down_cell == "+":
                    self.add_and_check_neighbor(node,row,col,distance,1)
                    break

    def add_and_check_neighbor(self, node, row, col, distance, direction):
        if direction == 0:
            neighbor = self.nodes[(row,col+distance)]
            node.add_neighbor(neighbor, 0, distance)
            self.add_neighbors(neighbor, row, col+distance)
        elif direction == 1:
            neighbor = self.nodes[(row+distance, col)]
            node.add_neighbor(neighbor, 1, distance)
            self.add_neighbors(neighbor, row+distance, col)

    def add_all_nodes(self):
        for i,row in enumerate(self.mapp):
            for j,cell in enumerate(row):
                if cell == "+":
                    self.add_node(i,j)

    def add_node(self, row, col):
        node = Node(row, col)
        self.nodes[(row,col)] = node

    def str_to_map(self,map_string: str):
        mapp: List[List[str]] = map_string.split('\n')
        for i,row in enumerate(mapp):
            mapp[i] = [letter for letter in mapp[i]]
        return mapp

    def mget(self,row: int,col: int) -> str:
        try:
            return self.mapp[row][col]
        except:
            return "X"

    def map_to_str(self, mapp):
        string_version = "\n".join(["".join([str(letter) for letter in row]).rstrip(" ") for row in mapp])
        return string_version

    

def break_pieces(shape: str) -> List[str]:
    pass

if __name__ == "__main__":
    shape = '\n'.join(["+------------+",
                   "|            |",
                   "|            |",
                   "|            |",
                   "+------+-----+",
                   "|      |     |",
                   "|      |     |",
                   "+------+-----+"])

    solution = ['\n'.join(["+------------+",
                       "|            |",
                       "|            |",
                       "|            |",
                      "+------------+"]),
            '\n'.join(["+------+",
                       "|      |",
                       "|      |",
                       "+------+"]),
            '\n'.join(["+-----+",
                       "|     |",
                       "|     |",
                       "+-----+"])]
    

    # assert break_pieces(shape) == sorted(solution)

    shape2 = """+-+-+
| | |
| | |
+-+-+"""

    shape3 = """+---+
|   |
+---+--+
|      |
+------+"""

    shape4 = """   +--+
   |  |
+--+--+-+
|       |
+-------+"""

    shape5 = """
+------+
|      |
|  ++  |
|  ||  |
|  ++  |
|      |
+------+"""

    shape6 = """
+------------+
|            |
|            |
|            |
+------++----+
|      ||    |
|      ||    |
+------++----+
|            |
+------------+"""

    shape7="""
++
||
|+--+
|   |
+---+"""
    # sm = ShapeMap(shape2)

    shape8 = """
+-----------------+
|                 |
|   +-------------+
|   |
|   |
|   |
|   +-------------+
|                 |
+-----------------+
""".strip('\n')

    shape9 = """
 ++
++++
++++
 ++"""

    shape10= """
 ++                                                                                                             
++++                                                                                                                
++++                                                                                                                
 ++                                                                                                                           
"""

    shape11="""
*  +-----------------+*
*  |+--------++-----+|*
*  ||        ++     ||*
*  |+--------+|     ||*
*+++----------+     ||*
*|++----------------+|*
*|||+----------------+*
*||||*
*|||+------+*
*||+-------+*
*|+--------+*
*+---------+*
**
*+-----------+*
*|+++------++|*
*||++      ++|*
*||        |||*
*|+--------+||*
*+----------+|*
*+-----------+*
""".replace("*","")

    shape12 = """
*************************************************************
*+--------+-+----------------+-+----------------+-+--------+*
*|        +-+                | |                +-+        |*
*|  +-----+ |    ++          | |                           |*
*|  +-++----+    ++     +----+ |                           |*
*|    ++                |+-----+    ++                     |*
*|    ||                ||          ||                     |*
*++   |+-------------+  ||  +-------+| ++                 ++*
*||   |              |  ||  |     +--+ ||                 ||*
*++   +---+ +--------+  ||  |     +---+++                 ++*
*|        | |           ||  +--------+|                    |*
*|        | |           |+-----------+|                    |*
*|        | |           +----+ +------+                    |*
*|        | |                | |                           |*
*|        | |                | |                +-+        |*
*|        | |                +-+                +-+        |*
*|        | |                                              |*
*|   +----+ |                                              |*
*|   |+-----+    ++                                        |*
*|   ||          ||                                        |*
*++  ||  +-------+| ++                 ++                 ++*
*||  ||  |     +--+ ||                 ||                 ||*
*++  ||  |     +---+++                 ++                 ++*
*|   ||  +--------+|                                       |*
*|   |+-----------+|                                       |*
*|   +----+ +------+                                       |*
*|        | |                                              |*
*|        | |                +-+                +-+        |*
*+--------+-+----------------+-+----------------+-+--------+*
*************************************************************""".replace("*","")
    tests = [shape,shape2,shape3,
    shape4,shape5,shape6,shape7,
    shape8,shape9,shape10,shape11,shape12]

    s = ShapeGraph(shape)
    print(s)
    ss = s.get_shapes()
    for each in ss:
        print("---")
        print([(n.row,n.column) for n in each])