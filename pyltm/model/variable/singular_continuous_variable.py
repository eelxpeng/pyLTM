'''
Created on 11 Feb 2018

@author: Bryan
'''
from .continuous_variable import ContinuousVariable
from sortedcontainers import SortedSet

class SingularContinuousVariable(ContinuousVariable):
    '''
    classdocs
    '''
    def __init__(self, name):
        '''
        Constructor
        '''
        super().__init__(name)
        
    def variables(self):
        return SortedSet([self])