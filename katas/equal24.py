"""
A game I played when I was young: Draw 4 cards from playing cards, use + - * / and () to make the final results equal to 24.

You will coding in function equalTo24. Function accept 4 parameters a b c d(4 numbers), value range is 1-100.

The result is a string such as "2*2*2*3" ,(4+2)*(5-1); If it is not possible to calculate the 24, please return "It's not possible!"

All four cards are to be used, only use three or two cards are incorrect; Use a card twice or more is incorrect too.

You just need to return one correct solution, don't need to find out all the possibilities.

The different between "challenge version" and "simple version":

1) a,b,c,d range:  In "challenge version" it is 1-100, 
                   In "simple version" it is 1-13.
2) "challenge version" has 1000 random testcases,
   "simple version" only has 20 random testcases.
Some examples:
equalTo24(1,2,3,4) //can return "(1+3)*(2+4)" or "1*2*3*4"
equalTo24(2,3,4,5) //can return "(5+3-2)*4" or "(3+4+5)*2"
equalTo24(3,4,5,6) //can return "(3-4+5)*6"
equalTo24(1,1,1,1) //should return "It's not possible!"
equalTo24(13,13,13,13) //should return "It's not possible!"
"""

class Graph24():
    def __init__(self,a,b,c,d):
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.nodes = { #need to make this dynamic for the general case, just hardcoding it for a 4-root application
            1:{
                'a':[],
                'b':[],
                'c':[],
                'd':[],
            },
            2:{
                'ab':[],
                'ac':[],
                'ad':[],
                'bc':[],
                'bd':[],
                'cd':[]
            },
            3:{
                'abc':[],
                'abd':[],
                'acd':[],
                'bcd':[]
            },
            4:{
                'abcd':[]
            },
        }
        for value,label in zip([a,b,c,d],['a','b','c','d']):
            self.add_node(value,1,None,None,None,label)
    
    def add_node(self,value,weight,left,right,operator,roots):
        node = Node(value,weight,left,right,operator,roots)
        self.nodes[weight][roots].append(node)

    def build(self):
        


class Node():
    def __init__(self,value,weight,left,right,operator,roots):
        self.value = value # numeric value of this node
        self.weight  = weight # how many roots went into this? 1+1 gives a node of weight 2, 24 should be weight 4
        self.left = left # None or the left parent node
        self.right = right # None or the right parent node
        self.operator = operator # None or ths operator (str) used to make this node
        self.roots = sorted(''+roots) # a string of the original labels, can be used to check that an invalid node is not made

    def get_expression(self):
        if self.weight == 1:
            return str(self.value)
        else:
            return f"({left.get_expression()}{self.operator}{right.get_expression()})"


def equal_to_24(a,b,c,d):
    graph24 = Graph24(a,b,c,d)
    solution = graph24.build()
    if solution:
        return solution
    else:
        return "It's not possible!"
    
    # if a*b*c*d == 24:
    #     return f"{a}*{b}*{c}*{d}"
    # # solve the no bracket case:
    # elif (b+c+d)*a == 24:
    #     return f"({b}+{c}+{d})*{a}"
    # else:
    #     return "It's not possible!"

if __name__ == "__main__":
    assert eval(equal_to_24(1,2,3,4))==24
    assert eval(equal_to_24(2,3,4,5))==24
    assert eval(equal_to_24(3,4,5,6))==24