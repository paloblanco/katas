"""
You are given a ASCII diagram , comprised of minus signs -, plus signs +, vertical bars | and whitespaces . Your task is to write a function which breaks the diagram in the minimal pieces it is made of.

For example, if the input for your function is this diagram:

+------------+
|            |
|            |
|            |
+------+-----+
|      |     |
|      |     |
+------+-----+
the returned value should be the list of:

+------------+
|            |
|            |
|            |
+------------+
(note how it lost a + sign in the extraction)

as well as

+------+
|      |
|      |
+------+
and

+-----+
|     |
|     |
+-----+
The diagram is given as an ordinary Javascript multiline string. The pieces should not have trailing spaces at the end of the lines. However, it could have leading spaces if the figure is not a rectangle. For instance:

    +---+
    |   |
+---+   |
|       |
+-------+
However, it is not allowed to use more leading spaces than necessary. It is to say, the first character of some of the lines should be different than a space.

Finally, note that only the explicitly closed pieces are considered. Spaces "outside" of the shape are part of the background . Therefore the diagram above has a single piece.

Have fun!
"""
from typing import List
from itertools import chain
from sys import setrecursionlimit
# from copy import deepcopy

def copy(mapp):
    mapp = mapp.copy()
    for i,row in enumerate(mapp):
        mapp[i] = row.copy()
    return mapp
    

setrecursionlimit(10**6)

class ShapeMap():
    def __init__(self, shape: str):
        self.mapp: List[str] = self.str_to_map(shape)
        self.width: int = max([len(each) for each in self.mapp])
        for i,each in enumerate(self.mapp):
            while(len(self.mapp[i])) < self.width:
                self.mapp[i].append(" ")
        self.mapp = self.expand_map(self.mapp)
        self.width: int = max([len(each) for each in self.mapp])
        self.height: int = len(self.mapp)

    def expand_map(self, mapp):
        # double map size so it can be filled properly
        mapp = copy(mapp)
        # widen rows
        for i in range(len(mapp)):
            newrow = [[each]+[" "] for each in mapp[i]]
            mapp[i] = list(chain(*newrow))[:-1]
            for j in range(1,len(mapp[i])-1,2):
                neighbors = [mapp[i][j-1], mapp[i][j+1]]
                if "|" in neighbors: continue
                elif "-" in neighbors: mapp[i][j] = "-"
                elif "+"==neighbors[0]==neighbors[1]: mapp[i][j] = "-"
        #increase height
        for i in range(1,len(mapp)*2-1,2):
            newrow = [" " for each in mapp[i-1]]
            mapp.insert(i,newrow)
            for j in range(len(mapp[i])):
                neighbors = [mapp[i-1][j], mapp[i+1][j]]
                if "-" in neighbors: continue
                elif "|" in neighbors: mapp[i][j] = "|"
                elif "+"==neighbors[0]==neighbors[1]: mapp[i][j] = "|"
        return mapp

    def shrink_map(self, mapp):
        # shrink a map to regular size
        mapp = copy(mapp)
        # kill every other row
        mapp = [row for i,row in enumerate(mapp) if i%2==0]
        # kill every other column
        for i in range(len(mapp)):
            mapp[i] = [each for j,each in enumerate(mapp[i]) if j%2==0]
        return mapp

    def str_to_map(self,map_string: str):
        mapp: List[List[str]] = map_string.split('\n')
        for i,row in enumerate(mapp):
            mapp[i] = [letter for letter in mapp[i]]
        return mapp
        
    def map_to_str(self, mapp):
        string_version = "\n".join(["".join([str(letter) for letter in row]) for row in mapp])
        return string_version

    def mget(self,row: int,col: int) -> str:
        try:
            return self.mapp[row][col]
        except:
            return "X"

    def mset(self, row: int, col: int, val: str):
        self.mapp[row][col] = str(val)


    def __str__(self) -> str:
        return self.map_to_str(self.mapp)

    def build_single_shape(self, ix, mapp):
        mapp = copy(mapp)
        minx = self.flood_dict[ix]["minx"]-1
        miny = self.flood_dict[ix]["miny"]-1
        maxx = self.flood_dict[ix]["maxx"]+1
        maxy = self.flood_dict[ix]["maxy"]+1
        for i in range(miny,maxy+1):
            for j in range(minx,maxx+1):
                if self.mget(i,j) == ix:
                    mapp[i][j] = " "
                else:
                    if ix == self.mget(i-1,j-1): continue
                    if ix == self.mget(i-1,j): continue
                    if ix == self.mget(i-1,j+1): continue
                    if ix == self.mget(i,j-1): continue
                    if ix == self.mget(i,j+1): continue
                    if ix == self.mget(i+1,j-1): continue
                    if ix == self.mget(i+1,j): continue
                    if ix == self.mget(i+1,j+1): continue
                    mapp[i][j] = " "
                    # checked = []
                    # for ki in [-1,0,1]:
                    #     for kj in [-1,0,1]:
                    #         if ki == kj == 0:
                    #             checked.append(" ")
                    #         else:
                    #             checked.append(self.mget(i+ki,j+kj))
                    
                    # if ix not in checked:
                    #     mapp[i][j] = " "

        # trim the array
        mapp = mapp[miny:maxy+1]
        for i, row in enumerate(mapp):
            mapp[i] = mapp[i][minx:maxx+1]
        # correct bad joints
        for i in range(len(mapp)):
            for j in range(len(mapp[0])):
                cell = mapp[i][j]
                if cell != "+": continue
                checks = []
                for ki,kj in [[-1,0],[1,0],[0,-1],[0,1]]:
                    try:
                        check_val = mapp[i+ki][j+kj]
                        if check_val in ["-","|"]: checks.append(check_val)
                    except:
                        pass
                if (len(set(checks)) < 2):
                    mapp[i][j] = checks[0]
                
        # trim trailing whitespace
        for i, row in enumerate(mapp):
            row_str = "".join(mapp[i])
            row_str = row_str.rstrip(" ")
            mapp[i] = [letter for letter in row_str]
        mapp = self.shrink_map(mapp)
        mapp_str = self.map_to_str(mapp)
        return mapp_str


    def build_shapes(self):
        self.shapes = []
        for i in range(self.flood_index):
            this_shape = self.build_single_shape(str(i), self.mapp)
            self.shapes.append(this_shape)

    def fill_shapes(self):
        # flood fill with integers to get shapes
        # first check boundaries and fill with X to indicate out of bounds
        self.flood_dict = {}
        for i, cell in enumerate(self.mapp[0]):
            if cell == " ":
                self.floodfill(0, i, 'X',0)
        for i, cell in enumerate(self.mapp[-1]):
            if cell == " ":
                self.floodfill(-1, i, 'X',0)
        for j in range(self.height):
            cell = self.mget(j,0)
            if cell == " ":
                self.floodfill(j, 0, 'X',0)
            cell = self.mget(j,-1)
            if cell == " ":
                self.floodfill(j, -1, 'X',0)
        self.flood_index = 0
        
        for i in range(self.height):
            for j in range(self.width):
                cell = self.mget(i,j)
                if cell == " ":
                    self.flood_dict[str(self.flood_index)] = {
                        "minx": self.width,
                        "miny": self.height,
                        "maxx": 0,
                        "maxy": 0,
                    }
                    self.floodfill(i,j,str(self.flood_index), 4)
                    self.flood_index += 1

    def floodfill(self,row: int,col: int, val: str, vec: int):
        # cell = self.mget(row,col)
        if self.mget(row,col) == " ":
            self.mapp[row][col] = val
            self.floodfill(row-1,col,val, 2)
            self.floodfill(row+1,col,val, 3)
            self.floodfill(row,col-1,val, 0)
            self.floodfill(row,col+1,val, 1)
            if val == "X": return
            elif vec == 0: self.flood_dict[val]["minx"] = min(self.flood_dict[val]["minx"],col)
            elif vec == 1: self.flood_dict[val]["maxx"] = max(self.flood_dict[val]["maxx"],col)
            elif vec == 2: self.flood_dict[val]["miny"] = min(self.flood_dict[val]["miny"],row)
            elif vec == 3: self.flood_dict[val]["maxy"] = max(self.flood_dict[val]["maxy"],row)
            elif vec == 4:
                self.flood_dict[val]["minx"] = min(self.flood_dict[val]["minx"],col)
                self.flood_dict[val]["miny"] = min(self.flood_dict[val]["miny"],row)
                self.flood_dict[val]["maxx"] = max(self.flood_dict[val]["maxx"],col)
                self.flood_dict[val]["maxy"] = max(self.flood_dict[val]["maxy"],row)

    def get_shapes_as_str(self):
        self.fill_shapes()
        
        self.build_shapes()
        return self.shapes


def break_pieces(shape: str) -> List[str]:
    shape_map: ShapeMap = ShapeMap(shape)
    return sorted(shape_map.get_shapes_as_str())


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
    tests = [shape,shape2,shape3,shape4,shape5,shape6,shape7,shape8,shape9,shape10,shape11]
    # for s in tests:
    #     print("Problem")
    #     print(s)
    #     print("solution:")
    #     for each in break_pieces(s):
    #         print(each)
    #         print("*****")
    for each in break_pieces(shape12):
        print(each)
        print("*****")
    import cProfile
    cProfile.run('break_pieces(shape12)')
