'''
Created on 10 Feb 2018

@author: Bryan
'''
from abc import ABCMeta, abstractmethod
from .abstract_node import AbstractNode

class AbstractGraph(metaclass=ABCMeta):
    '''
    Abstract class for all graphs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self._nodes = list() # node list
        self._edges = list() # edge list
        self._names = dict() # HashMap: str : node
    
    @abstractmethod
    def addNode(self, name):
        '''
        Add a node to the graph with specified name
        '''
        pass
    @abstractmethod
    def addEdge(self, head, tail):
        pass
        
    def containsEdge(self, edge):
        return edge.getHead().getGraph() is self
    
    def containsNode(self, node):
        if isinstance(node, AbstractNode):
            return node.getGraph() is self
        elif isinstance(node, str):
            return node in self._names
        else:
            raise ValueError("Argument to Abstractgraph.containsNode error!")
        
    @property
    def edges(self):
        return self._edges
    
    @property
    def nodes(self):
        return self._nodes
    
    @property
    def names(self):
        return self._names.keys()
    
    def getNode(self, name):
        return self._names.get(name)
    
    def getNumberOfNodes(self):
        return len(self._nodes)
    
    def getNumberOfEdges(self):
        return len(self._edges)
    
    
    