'''
Created on 11 Feb 2018

@author: Bryan
'''
from .continuous_variable import ContinuousVariable
from sortedcontainers import SortedSet
import collections
from .singular_continuous_variable import SingularContinuousVariable

class JointContinuousVariable(ContinuousVariable):
    '''
    classdocs
    '''
    def __init__(self, name, variables):
        '''
        Constructor
        '''
        super().__init__(name)
        if isinstance(variables, collections.Iterable):
            for v in variables:
                assert isinstance(v, SingularContinuousVariable)
            self._variables = SortedSet(variables)
        elif isinstance(variables, SingularContinuousVariable):
            self._variables = SortedSet([variables])
        else:
            raise ValueError("Invalid Argument Type!")
        self.setName(self.constructName)
        
    def constructName(self):
        name = ",".join(self._variables)
        return name
    
    def variables(self):
        return self._variables
            