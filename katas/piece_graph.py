from typing import List

class ShapeGraph():
    

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