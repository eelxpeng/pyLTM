'''
Created on 11 Feb 2018

@author: Bryan
'''
from .variable import Variable
class DiscreteVariable(Variable):
    '''
    classdocs
    '''
    STATE_PREFIX = "state"

    def __init__(self, name, states):
        '''
        Constructor:
        name: name of this variable
        states: str[] list of states of the variable to be created.
        '''
        super().__init__(name)
        if isinstance(states, list):
            assert len(states)!=0
            self._states = states
        elif isinstance(states, int):
            self._states = DiscreteVariable.createDefaultStates(states)
            
    @staticmethod
    def createDefaultStates(cardinality):
        states = list()
        for i in range(cardinality):
            states.append(DiscreteVariable.STATE_PREFIX+str(i))
        return states
    @staticmethod
    def getCardinalities(variables):
        cardinality = 1
        for variable in variables:
            cardinality *= variable.getCardinality()
        return cardinality
    
    def getCardinality(self):
        return len(self._states)
    @property
    def states(self):
        return self._states
    def indexOf(self, state):
        return self._states.index(state)
        
        