"""
The following figure shows a cell grid with 6 cells (2 rows by 3 columns), each cell separated from the others by walls:

+--+--+--+
|  |  |  |
+--+--+--+
|  |  |  |
+--+--+--+
This grid has 6 connectivity components of size 1. We can describe the size and number of connectivity components by the list [(1, 6)], since there are 6 components of size 1.

If we tear down a couple of walls, we obtain:

+--+--+--+
|  |     |
+  +--+--+
|  |  |  |
+--+--+--+
, which has two connectivity components of size 2 and two connectivity components of size 1. The size and number of connectivity components is described by the list [(2, 2), (1, 2)].

Given the following grid:

+--+--+--+
|     |  |
+  +--+--+
|     |  |
+--+--+--+
we have the connectivity components described by [(4, 1), (1, 2)].

Your job is to define a function components(grid) that takes as argument a string representing a grid like in the above pictures and returns a list describing the size and number of the connectivity components. The list should be sorted in descending order by the size of the connectivity components. The grid may have any number of rows and columns.

Note: The grid is always rectangular and will have all its outer walls. Only inner walls may be missing. The + are considered bearing pillars, and are always present.

"""

# Strategy - use a graph. each 1x1 "cell" is a node, and the absence of a wall is an edge.
# Once we build the graph, just calculate the number and size of neighborhoods

def grid_to_array(grid):
    # return a list of lists representing the "cells"
    # 0 means no walls, 1 means door to right,
    # 2 means door down, and 3 means both doors
    rows = grid.splitlines()
    row_count = (len(rows)-1)//2
    column_count = rows[0].count('+') - 1
    array = [[0 for c in range(column_count)] for r in range(row_count)]
    for i,row in enumerate(rows[:-1]):
        if i == 0: continue
        elif i%2==1: # vertical walls
            ix = (i-1)//2
            walls = row[::3][1:-1]
            for ic, wall in enumerate(walls):
                if wall =="|":
                    array[ix][ic] += 1
        else:
            ix = (i-2)//2
            walls = row.split('+')[1:-1]
            for ic, wall in enumerate(walls):
                if wall == "--":
                    array[ix][ic] += 2
    # fix ends
    for row in array:
        row[-1] +=1
    for i,_ in enumerate(array[-1]):
        array[-1][i] += 2
    return array


class Vertex():
    def __init__(self,row,column):
        self.siblings = set()
        self.row = row
        self.column = column

    def add_sibling(self, other):
        self.siblings |= set([other])

    def repr(self):
        name = f"Row:{self.row} Col:{self.column} #siblings:{len(self.siblings)}"
        return name

    def __str__(self):
        return self.repr()

    def __repr__(self):
        return self.repr()


class Graph():
    def __init__(self,array):
        self.array_vertices={}
        # make all vertices
        for ir,row in enumerate(array):
            for ic,cell in enumerate(row):
                self.add_vertex(ir,ic)
        # add edges
        for ir,row in enumerate(array):
            for ic,cell in enumerate(row):
                if cell == 3: continue
                elif cell == 2:
                    self.add_edge(ir,ic,ir,ic+1)
                elif cell == 1:
                    self.add_edge(ir,ic,ir+1,ic)
                elif cell == 0:
                    self.add_edge(ir,ic,ir,ic+1)
                    self.add_edge(ir,ic,ir+1,ic)

    def get_components(self):
        self.components = []
        visited_cells = []
        for cell in self.array_vertices.values():
            # this_component = []
            if cell not in visited_cells:
                this_component = self.get_connected_vertices(cell)
                visited_cells += this_component
                self.components.append(this_component)
        component_lens = [len(each) for each in self.components]
        self.component_tuples = []
        for each in set(component_lens):
            self.component_tuples.append((each,component_lens.count(each)))
        self.component_tuples = sorted(self.component_tuples, key=lambda x: x[0], reverse=True)
        return self.component_tuples


    def get_connected_vertices(self,vertex):
        visited_vertices = []
        def recurse_through_vertices(v):
            if v not in visited_vertices:
                visited_vertices.append(v)
                for s in v.siblings:
                    if s not in visited_vertices: recurse_through_vertices(s)
        recurse_through_vertices(vertex)
        return visited_vertices

    def add_vertex(self,row,column):
        v = Vertex(row,column)
        self.array_vertices[(row,column)] = v

    def add_edge(self,row1,column1,row2,column2):
        self.array_vertices[(row1,column1)].add_sibling(self.array_vertices[(row2,column2)])
        self.array_vertices[(row2,column2)].add_sibling(self.array_vertices[(row1,column1)])

def components(grid):
    array = grid_to_array(grid)
    graph = Graph(array)
    return graph.get_components()


if __name__ == "__main__":

    print('Example Test Cases')
    print('''\
+--+--+--+
|  |  |  |
+--+--+--+
|  |  |  |
+--+--+--+''',grid_to_array('''\
+--+--+--+
|  |  |  |
+--+--+--+
|  |  |  |
+--+--+--+'''))

    print('''\
+--+--+--+
|  |     |
+--+  +--+
|  |  |  |
+--+--+--+''',grid_to_array('''\
+--+--+--+
|  |     |
+--+  +--+
|  |  |  |
+--+--+--+'''))

    g = Graph(grid_to_array('''\
+--+--+--+
|  |     |
+--+  +--+
|  |  |  |
+--+--+--+'''))

    for k,v in g.array_vertices.items():
        print(k,v)

    print(g.get_components())
    for each in g.components:
        print(each)


    newgrid = """\
+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
|     |              |  |     |     |  |  |     |        |  |
+--+  +  +  +  +  +  +--+  +--+  +--+  +--+--+--+--+--+  +--+
|     |  |  |           |     |           |  |  |     |     |
+  +  +--+--+  +--+--+  +--+  +--+  +--+--+--+--+  +  +--+--+
|  |     |  |  |           |  |        |  |  |        |     |
+--+--+  +  +  +--+--+--+--+  +--+  +  +  +--+  +  +  +  +--+
|                 |           |  |  |           |           |
+--+  +--+  +--+  +--+--+  +  +--+  +  +  +  +--+  +--+--+  +
|                 |  |           |  |           |           |
+--+--+--+  +--+--+--+  +--+--+  +  +  +  +--+  +  +  +  +  +
|                          |     |  |  |  |  |  |        |  |
+--+  +  +--+  +  +--+  +--+  +--+  +  +--+--+--+--+--+  +  +
|           |  |  |              |  |  |  |  |  |  |     |  |
+--+  +--+  +  +  +--+  +  +--+--+  +--+  +--+  +--+--+  +--+
|  |           |  |     |           |  |  |  |  |     |  |  |
+  +  +--+--+  +--+  +  +--+  +  +  +--+--+--+  +--+  +--+--+
|  |     |  |     |  |     |     |           |  |     |     |
+  +  +  +--+  +--+--+--+  +  +  +--+--+  +--+  +  +  +  +  +
|  |        |     |  |     |  |           |                 |
+--+  +--+  +  +  +  +--+  +  +  +  +  +--+  +  +--+  +  +  +
|  |           |     |     |     |     |                    |
+  +  +--+  +--+--+--+  +  +--+--+--+  +--+--+--+  +  +--+  +
|        |              |  |  |     |        |  |  |  |  |  |
+  +  +  +  +--+--+--+  +  +--+--+  +  +--+  +  +--+--+  +--+
|  |              |     |        |  |     |  |     |     |  |
+--+--+  +--+--+--+  +--+--+  +--+  +--+--+--+  +  +  +--+  +
|     |  |  |  |           |        |     |  |     |  |     |
+--+  +--+  +--+--+  +--+--+--+--+--+--+--+  +--+--+--+--+--+
|  |  |     |  |  |  |           |  |     |     |  |  |  |  |
+  +--+--+--+--+  +  +--+--+--+--+  +  +  +--+--+  +  +  +  +
|  |  |  |  |     |  |        |  |  |  |  |  |  |  |  |  |  |
+--+  +--+  +--+--+--+--+--+--+  +--+--+  +--+  +--+  +--+--+
|  |                 |  |  |  |        |  |              |  |
+--+  +  +  +  +  +--+--+  +  +  +--+  +--+  +--+  +  +  +--+
|           |     |  |     |     |     |  |           |  |  |
+  +  +--+--+  +--+--+--+--+  +--+  +--+  +  +--+--+  +  +  +
|                    |                                |     |
+--+  +--+  +--+  +--+  +--+  +--+--+  +  +--+--+  +--+--+--+
|           |           |  |  |  |     |  |              |  |
+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+"""
    print(components(newgrid))

    newgrid2 = """\
+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
|              |     |           |  |  |  |  |           |  |
+  +  +  +  +  +  +--+  +--+--+  +  +  +--+  +  +--+--+--+  +
|  |     |  |     |  |           |  |        |  |  |  |  |  |
+--+--+  +  +  +  +  +  +  +  +  +--+  +--+--+--+  +--+  +  +
|           |  |  |  |  |     |  |  |     |     |  |  |  |  |
+--+  +  +  +--+--+  +--+--+  +--+  +--+  +  +  +  +--+--+  +
|     |     |     |  |     |  |     |  |  |  |  |     |  |  |
+--+  +  +  +--+  +  +  +  +--+--+--+  +--+  +  +--+  +--+--+
|  |  |  |     |           |                             |  |
+  +--+  +--+  +--+--+  +--+  +--+  +--+  +--+--+--+  +  +--+
|     |  |        |  |           |  |  |  |           |     |
+  +--+--+  +  +  +--+--+  +  +--+--+  +--+--+  +--+--+--+  +
|  |        |  |  |  |        |  |        |              |  |
+--+--+  +--+  +--+  +--+--+  +  +--+--+  +  +--+--+  +  +  +
|              |  |        |  |        |     |  |  |     |  |
+  +  +  +  +--+  +  +--+  +--+  +--+  +  +--+--+--+  +  +  +
|        |  |        |     |     |     |  |        |        |
+--+--+--+--+  +--+  +  +--+  +--+  +  +--+--+  +--+  +--+  +
|        |  |     |  |     |  |  |     |     |  |        |  |
+  +--+  +--+  +  +  +  +  +--+--+  +--+  +  +  +  +--+  +  +
|  |           |  |              |  |     |     |  |     |  |
+  +  +  +--+--+  +  +  +  +  +  +--+  +--+  +--+--+  +  +--+
|  |        |  |  |     |        |     |     |     |        |
+  +  +  +  +  +  +--+  +--+--+  +  +  +--+  +  +  +  +  +--+
|     |           |     |     |              |  |        |  |
+  +  +  +  +  +  +--+--+  +--+  +  +  +--+  +  +  +  +--+  +
|  |     |  |  |     |        |     |              |     |  |
+--+  +--+--+--+--+--+  +--+--+--+  +--+--+  +  +  +  +--+--+
|        |                 |           |  |  |  |  |  |     |
+--+--+--+  +  +  +--+  +--+  +--+--+--+--+--+--+--+--+--+--+
|     |  |  |  |     |        |  |  |  |                    |
+  +  +  +--+  +  +  +  +  +  +  +--+--+--+--+--+--+  +  +  +
|     |  |  |  |        |  |        |     |     |        |  |
+  +--+--+  +  +  +  +--+--+--+--+  +  +  +  +  +--+--+--+  +
|     |     |  |  |  |     |     |  |  |  |  |  |  |  |  |  |
+--+  +  +  +  +--+  +  +  +  +  +--+--+  +--+  +  +--+  +  +
|  |  |  |  |     |  |        |        |  |  |     |     |  |
+  +--+--+  +--+--+  +--+  +--+  +--+--+  +--+  +--+  +--+--+
|  |           |        |  |     |  |  |  |  |  |        |  |
+  +  +  +  +  +  +--+  +--+--+  +  +  +--+  +  +--+--+--+  +
|  |     |  |     |  |           |  |        |  |  |  |  |  |
+--+--+  +  +  +  +  +  +  +  +  +--+  +--+--+--+  +--+  +  +
|           |  |  |  |  |     |  |  |     |     |  |  |  |  |
+--+  +  +  +--+--+  +--+--+  +--+  +--+  +  +  +  +--+--+  +
|     |     |     |  |     |  |     |  |  |  |  |     |  |  |
+--+  +  +  +--+  +  +  +  +--+--+--+  +--+  +  +--+  +--+--+
|  |  |  |     |           |                             |  |
+  +--+  +--+  +--+--+  +--+  +--+  +--+  +--+--+--+  +  +--+
|     |  |        |  |           |  |  |  |           |     |
+  +--+--+  +  +  +--+--+  +  +--+--+  +--+--+  +--+--+--+  +
|  |        |  |  |  |        |  |        |              |  |
+--+--+  +--+  +--+  +--+--+  +  +--+--+  +  +--+--+  +  +  +
|              |  |        |  |        |     |  |  |     |  |
+  +  +  +  +--+  +  +--+  +--+  +--+  +  +--+--+--+  +  +  +
|        |  |        |     |     |     |  |        |        |
+--+--+--+--+  +--+  +  +--+  +--+  +  +--+--+  +--+  +--+  +
|        |  |     |  |     |  |  |     |     |  |        |  |
+  +--+  +--+  +  +  +  +  +--+--+  +--+  +  +  +  +--+  +  +
|  |           |  |              |  |     |     |  |     |  |
+  +  +  +--+--+  +  +  +  +  +  +--+  +--+  +--+--+  +  +--+
|  |        |  |  |     |        |     |     |     |        |
+  +  +  +  +  +  +--+  +--+--+  +  +  +--+  +  +  +  +  +--+
|     |           |     |     |              |  |        |  |
+  +  +  +  +  +  +--+--+  +--+  +  +  +--+  +  +  +  +--+  +
|  |     |  |  |     |        |     |              |     |  |
+--+  +--+--+--+--+--+  +--+--+--+  +--+--+  +  +  +  +--+--+
|        |                 |           |  |  |  |  |  |     |
+--+--+--+  +  +  +--+  +--+  +--+--+--+--+--+--+--+--+--+--+
|     |  |  |  |     |        |  |  |  |                    |
+  +  +  +--+  +  +  +  +  +  +  +--+--+--+--+--+--+  +  +  +
|     |  |  |  |        |  |        |     |     |        |  |
+  +--+--+  +  +  +  +--+--+--+--+  +  +  +  +  +--+--+--+  +
|     |     |  |  |  |     |     |  |  |  |  |  |  |  |  |  |
+--+  +  +  +  +--+  +  +  +  +  +--+--+  +--+  +  +--+  +  +
|  |  |  |  |     |  |        |        |  |  |     |     |  |
+  +--+--+  +--+--+  +--+  +--+  +--+--+  +--+  +--+  +--+--+
|  |           |        |  |     |  |  |  |  |  |        |  |
+  +  +  +  +  +  +--+  +--+--+  +  +  +--+  +  +--+--+--+  +
|  |     |  |     |  |           |  |        |  |  |  |  |  |
+--+--+  +  +  +  +  +  +  +  +  +--+  +--+--+--+  +--+  +  +
|           |  |  |  |  |     |  |  |     |     |  |  |  |  |
+--+  +  +  +--+--+  +--+--+  +--+  +--+  +  +  +  +--+--+  +
|     |     |     |  |     |  |     |  |  |  |  |     |  |  |
+--+  +  +  +--+  +  +  +  +--+--+--+  +--+  +  +--+  +--+--+
|  |  |  |     |           |                             |  |
+  +--+  +--+  +--+--+  +--+  +--+  +--+  +--+--+--+  +  +--+
|     |  |        |  |           |  |  |  |           |     |
+  +--+--+  +  +  +--+--+  +  +--+--+  +--+--+  +--+--+--+  +
|  |        |  |  |  |        |  |        |              |  |
+--+--+  +--+  +--+  +--+--+  +  +--+--+  +  +--+--+  +  +  +
|              |  |        |  |        |     |  |  |     |  |
+  +  +  +  +--+  +  +--+  +--+  +--+  +  +--+--+--+  +  +  +
|        |  |        |     |     |     |  |        |        |
+--+--+--+--+  +--+  +  +--+  +--+  +  +--+--+  +--+  +--+  +
|        |  |     |  |     |  |  |     |     |  |        |  |
+  +--+  +--+  +  +  +  +  +--+--+  +--+  +  +  +  +--+  +  +
|  |           |  |              |  |     |     |  |     |  |
+  +  +  +--+--+  +  +  +  +  +  +--+  +--+  +--+--+  +  +--+
|  |        |  |  |     |        |     |     |     |        |
+  +  +  +  +  +  +--+  +--+--+  +  +  +--+  +  +  +  +  +--+
|     |           |     |     |              |  |        |  |
+  +  +  +  +  +  +--+--+  +--+  +  +  +--+  +  +  +  +--+  +
|  |     |  |  |     |        |     |              |     |  |
+--+  +--+--+--+--+--+  +--+--+--+  +--+--+  +  +  +  +--+--+
|        |                 |           |  |  |  |  |  |     |
+--+--+--+  +  +  +--+  +--+  +--+--+--+--+--+--+--+--+--+--+
|     |  |  |  |     |        |  |  |  |                    |
+  +  +  +--+  +  +  +  +  +  +  +--+--+--+--+--+--+  +  +  +
|     |  |  |  |        |  |        |     |     |        |  |
+  +--+--+  +  +  +  +--+--+--+--+  +  +  +  +  +--+--+--+  +
|     |     |  |  |  |     |     |  |  |  |  |  |  |  |  |  |
+--+  +  +  +  +--+  +  +  +  +  +--+--+  +--+  +  +--+  +  +
|  |  |  |  |     |  |        |        |  |  |     |     |  |
+  +--+--+  +--+--+  +--+  +--+  +--+--+  +--+  +--+  +--+--+
|  |           |        |  |     |  |  |  |  |  |        |  |
+  +  +  +  +  +  +--+  +--+--+  +  +  +--+  +  +--+--+--+  +
|  |     |  |     |  |           |  |        |  |  |  |  |  |
+--+--+  +  +  +  +  +  +  +  +  +--+  +--+--+--+  +--+  +  +
|           |  |  |  |  |     |  |  |     |     |  |  |  |  |
+--+  +  +  +--+--+  +--+--+  +--+  +--+  +  +  +  +--+--+  +
|     |     |     |  |     |  |     |  |  |  |  |     |  |  |
+--+  +  +  +--+  +  +  +  +--+--+--+  +--+  +  +--+  +--+--+
|  |  |  |     |           |                             |  |
+  +--+  +--+  +--+--+  +--+  +--+  +--+  +--+--+--+  +  +--+
|     |  |        |  |           |  |  |  |           |     |
+  +--+--+  +  +  +--+--+  +  +--+--+  +--+--+  +--+--+--+  +
|  |        |  |  |  |        |  |        |              |  |
+--+--+  +--+  +--+  +--+--+  +  +--+--+  +  +--+--+  +  +  +
|              |  |        |  |        |     |  |  |     |  |
+  +  +  +  +--+  +  +--+  +--+  +--+  +  +--+--+--+  +  +  +
|        |  |        |     |     |     |  |        |        |
+--+--+--+--+  +--+  +  +--+  +--+  +  +--+--+  +--+  +--+  +
|        |  |     |  |     |  |  |     |     |  |        |  |
+  +--+  +--+  +  +  +  +  +--+--+  +--+  +  +  +  +--+  +  +
|  |           |  |              |  |     |     |  |     |  |
+  +  +  +--+--+  +  +  +  +  +  +--+  +--+  +--+--+  +  +--+
|  |        |  |  |     |        |     |     |     |        |
+  +  +  +  +  +  +--+  +--+--+  +  +  +--+  +  +  +  +  +--+
|     |           |     |     |              |  |        |  |
+  +  +  +  +  +  +--+--+  +--+  +  +  +--+  +  +  +  +--+  +
|  |     |  |  |     |        |     |              |     |  |
+--+  +--+--+--+--+--+  +--+--+--+  +--+--+  +  +  +  +--+--+
|        |                 |           |  |  |  |  |  |     |
+--+--+--+  +  +  +--+  +--+  +--+--+--+--+--+--+--+--+--+--+
|     |  |  |  |     |        |  |  |  |                    |
+  +  +  +--+  +  +  +  +  +  +  +--+--+--+--+--+--+  +  +  +
|     |  |  |  |        |  |        |     |     |        |  |
+  +--+--+  +  +  +  +--+--+--+--+  +  +  +  +  +--+--+--+  +
|     |     |  |  |  |     |     |  |  |  |  |  |  |  |  |  |
+--+  +  +  +  +--+  +  +  +  +  +--+--+  +--+  +  +--+  +  +
|  |  |  |  |     |  |        |        |  |  |     |     |  |
+  +--+--+  +--+--+  +--+  +--+  +--+--+  +--+  +--+  +--+--+
|  |           |        |  |     |  |  |  |  |  |        |  |
+  +  +  +  +  +  +--+  +--+--+  +  +  +--+  +  +--+--+--+  +
|  |     |  |     |  |           |  |        |  |  |  |  |  |
+--+--+  +  +  +  +  +  +  +  +  +--+  +--+--+--+  +--+  +  +
|           |  |  |  |  |     |  |  |     |     |  |  |  |  |
+--+  +  +  +--+--+  +--+--+  +--+  +--+  +  +  +  +--+--+  +
|     |     |     |  |     |  |     |  |  |  |  |     |  |  |
+--+  +  +  +--+  +  +  +  +--+--+--+  +--+  +  +--+  +--+--+
|  |  |  |     |           |                             |  |
+  +--+  +--+  +--+--+  +--+  +--+  +--+  +--+--+--+  +  +--+
|     |  |        |  |           |  |  |  |           |     |
+  +--+--+  +  +  +--+--+  +  +--+--+  +--+--+  +--+--+--+  +
|  |        |  |  |  |        |  |        |              |  |
+--+--+  +--+  +--+  +--+--+  +  +--+--+  +  +--+--+  +  +  +
|              |  |        |  |        |     |  |  |     |  |
+  +  +  +  +--+  +  +--+  +--+  +--+  +  +--+--+--+  +  +  +
|        |  |        |     |     |     |  |        |        |
+--+--+--+--+  +--+  +  +--+  +--+  +  +--+--+  +--+  +--+  +
|        |  |     |  |     |  |  |     |     |  |        |  |
+  +--+  +--+  +  +  +  +  +--+--+  +--+  +  +  +  +--+  +  +
|  |           |  |              |  |     |     |  |     |  |
+  +  +  +--+--+  +  +  +  +  +  +--+  +--+  +--+--+  +  +--+
|  |        |  |  |     |        |     |     |     |        |
+  +  +  +  +  +  +--+  +--+--+  +  +  +--+  +  +  +  +  +--+
|     |           |     |     |              |  |        |  |
+  +  +  +  +  +  +--+--+  +--+  +  +  +--+  +  +  +  +--+  +
|  |     |  |  |     |        |     |              |     |  |
+--+  +--+--+--+--+--+  +--+--+--+  +--+--+  +  +  +  +--+--+
|        |                 |           |  |  |  |  |  |     |
+--+--+--+  +  +  +--+  +--+  +--+--+--+--+--+--+--+--+--+--+
|     |  |  |  |     |        |  |  |  |                    |
+  +  +  +--+  +  +  +  +  +  +  +--+--+--+--+--+--+  +  +  +
|     |  |  |  |        |  |        |     |     |        |  |
+  +--+--+  +  +  +  +--+--+--+--+  +  +  +  +  +--+--+--+  +
|     |     |  |  |  |     |     |  |  |  |  |  |  |  |  |  |
+--+  +  +  +  +--+  +  +  +  +  +--+--+  +--+  +  +--+  +  +
|  |  |  |  |     |  |        |        |  |  |     |     |  |
+  +--+--+  +--+--+  +--+  +--+  +--+--+  +--+  +--+  +--+--+
|  |           |        |  |     |  |  |  |  |  |        |  |
+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+"""
    print(components(newgrid2))