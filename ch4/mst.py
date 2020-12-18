from typing import TypeVar, List, Optional
from ch4.weighted_graph import WeightedGraph
from ch4.weighted_edge import WeightedEdge
from ch2.generic_search import PriorityQueue

V = TypeVar('V') # type of vertices in the graph
WeightedPath = List[WeightedEdge]

def total_weight(wp: WeightedPath) -> float:
    return sum([e.weight for e in wp])