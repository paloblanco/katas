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
        self.solutions = []
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

    def build_old(self):
        operations = [
            self._make_nodes_adding,
            self._make_nodes_subtracting,
            self._make_nodes_multiplying,
            self._make_nodes_dividing
        ]
        # make all level 2s
        for op in operations:
            op(1,1)
        # all level 3s:
        for op in operations:
            op(2,1)
            op(1,2)
        # all 2x2s
        for op in operations:
            op(2,2)
        #all 3x1s
        for op in operations:
            op(3,1)
            op(1,3)
        
        return self.fetch_solution()

    def build(self):
        operations = [
            self._make_nodes_adding_explicit,
            self._make_nodes_subtracting_explicit,
            self._make_nodes_multiplying_explicit,
            self._make_nodes_dividing_explicit
        ]
        operations_non_comutative = [
            self._make_nodes_subtracting_explicit,
            self._make_nodes_dividing_explicit
        ]
        # make all level 2s
        for op in operations:
            op(self.nodes[1]['a'],self.nodes[1]['b'],'ab')
            op(self.nodes[1]['a'],self.nodes[1]['c'],'ac')
            op(self.nodes[1]['a'],self.nodes[1]['d'],'ad')
            op(self.nodes[1]['b'],self.nodes[1]['c'],'bc')
            op(self.nodes[1]['b'],self.nodes[1]['d'],'bd')
            op(self.nodes[1]['c'],self.nodes[1]['d'],'cd')
        # all level 3s:
        for op in operations:
            op(self.nodes[2]['ab'],self.nodes[1]['c'],'abc')
            op(self.nodes[2]['ab'],self.nodes[1]['d'],'abd')
            op(self.nodes[2]['ac'],self.nodes[1]['b'],'abc')
            op(self.nodes[2]['ac'],self.nodes[1]['d'],'acd')
            op(self.nodes[2]['ad'],self.nodes[1]['b'],'abd')
            op(self.nodes[2]['ad'],self.nodes[1]['c'],'acd')
            op(self.nodes[2]['bc'],self.nodes[1]['a'],'abc')
            op(self.nodes[2]['bc'],self.nodes[1]['d'],'bcd')
            op(self.nodes[2]['bd'],self.nodes[1]['a'],'abd')
            op(self.nodes[2]['bd'],self.nodes[1]['c'],'bcd')
            op(self.nodes[2]['cd'],self.nodes[1]['a'],'acd')
            op(self.nodes[2]['cd'],self.nodes[1]['b'],'bcd')
        # all 2x2s
        for op in operations:
            op(self.nodes[2]['ab'],self.nodes[2]['cd'],'abcd')
            op(self.nodes[2]['ac'],self.nodes[2]['bd'],'abcd')
            op(self.nodes[2]['ad'],self.nodes[2]['bc'],'abcd')
        #all 3x1s
        for op in operations:
            op(self.nodes[3]['abc'],self.nodes[1]['d'],'abcd')
            op(self.nodes[3]['abd'],self.nodes[1]['c'],'abcd')
            op(self.nodes[3]['acd'],self.nodes[1]['b'],'abcd')
            op(self.nodes[3]['bcd'],self.nodes[1]['a'],'abcd')
        return self.fetch_solution()
    
    def fetch_solution(self):
        # check completed graph for a solution
        for node in self.nodes[4]['abcd']:
            if node.value == 24:
                return node.get_expression()
        return "It's not possible!"

    def _make_nodes_operation_explicit(self,left_nodes,right_nodes,operation,operation_string,roots):
        weight = left_nodes[0].weight + right_nodes[0].weight
        for left_node in left_nodes:
            for right_node in right_nodes:
                try:
                    value = operation(left_node.value, right_node.value)
                    self.add_node(value,weight,left_node,right_node,operation_string,roots)
                except:
                    pass

    def _make_nodes_subtracting_explicit(self,left_nodes,right_nodes,roots):
        self._make_nodes_operation_explicit(left_nodes,right_nodes,lambda x,y: x-y, '-', roots)
        self._make_nodes_operation_explicit(right_nodes,left_nodes,lambda x,y: x-y, '-', roots)

    def _make_nodes_dividing_explicit(self,left_nodes,right_nodes,roots):
        self._make_nodes_operation_explicit(left_nodes,right_nodes,lambda x,y: x/y, '/', roots)
        self._make_nodes_operation_explicit(right_nodes,left_nodes,lambda x,y: x/y, '/', roots)
    
    def _make_nodes_multiplying_explicit(self,left_nodes,right_nodes,roots):
        self._make_nodes_operation_explicit(left_nodes,right_nodes,lambda x,y: x*y, '*', roots)
    
    def _make_nodes_adding_explicit(self,left_nodes,right_nodes,roots):
        self._make_nodes_operation_explicit(left_nodes,right_nodes,lambda x,y: x+y, '+', roots)

    def _make_nodes_operation(self,left_level,right_level,operation,operation_string):
        left_lookup = self.nodes[left_level]
        right_lookup = self.nodes[right_level]
        weight = left_level+right_level
        for left_roots,left_nodes in left_lookup.items():
            for right_roots,right_nodes in right_lookup.items():
                if len(set(left_roots).intersection(set(right_roots))) == 0:
                    roots = ''.join(sorted(left_roots+right_roots))
                    for left_node in left_nodes:
                        for right_node in right_nodes:
                            try:
                                value = operation(left_node.value, right_node.value)
                                self.add_node(value,weight,left_node,right_node,operation_string,roots)
                            except:
                                pass
    
    def _make_nodes_subtracting(self,left_level,right_level):
        self._make_nodes_operation(left_level,right_level,lambda x,y: x-y, '-')

    def _make_nodes_dividing(self,left_level,right_level):
        self._make_nodes_operation(left_level,right_level,lambda x,y: x/y, '/')
    
    def _make_nodes_multiplying(self,left_level,right_level):
        self._make_nodes_operation(left_level,right_level,lambda x,y: x*y, '*')
    
    def _make_nodes_adding(self,left_level,right_level):
        self._make_nodes_operation(left_level,right_level,lambda x,y: x+y, '+')


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
            return f"({self.left.get_expression()}{self.operator}{self.right.get_expression()})"


def equal_to_24(a,b,c,d):
    graph24 = Graph24(a,b,c,d)
    return graph24.build()
    
if __name__ == "__main__":
    print(f"1,2,3,4 is {equal_to_24(1,2,3,4)}")
    print(f"2,3,4,5 is {equal_to_24(2,3,4,5)}")
    print(f"3,4,5,6 is {equal_to_24(3,4,5,6)}")
    print(f"1,1,1,1 is {equal_to_24(1,1,1,1)}")
    print(f"69,7,64,2 is {equal_to_24(69,7,64,2)}")
    print(f"69,64,2,7 is {equal_to_24(69,64,2,7)}")
       