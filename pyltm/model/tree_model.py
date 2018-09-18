'''
Created on 12 Feb 2018

@author: Bryan
'''
from .bayes_net import BayesNet

class TreeModel(BayesNet):
    '''
    classdocs
    '''
    def __init__(self, name):
        '''
        Constructor
        '''
        super().__init__(name)
        
    def getRoot(self):
        allnodes = self.nodes
        if allnodes is None:
            return None
        node = allnodes[0]
        while(not node.isRoot()):
            node = node.getParent()
        return node
    
    def getInternalNodes(self):
        internals = []
        for node in self.nodes:
            if len(node.children)!=0:
                internals.append(node)
        return internals
    
    def getLeafNodes(self):
        leafs = []
        for node in self.nodes:
            if len(node.children)==0:
                leafs.append(node)
        return leafs
    
    def getLeafVariables(self):
        leafs = self.getLeafNodes()
        variables = [n.variable for n in leafs]
        return variables
    
    def getInternalVariables(self):
        internalNodes = self.getInternalNodes()
        return [n.variable for n in internalNodes]
    
    