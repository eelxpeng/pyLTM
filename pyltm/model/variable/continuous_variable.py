'''
Created on 11 Feb 2018

@author: Bryan
'''
from .variable import Variable
from abc import abstractmethod
class ContinuousVariable(Variable):
    '''
    classdocs
    '''


    def __init__(self, name=None):
        '''
        Constructor
        '''
        super().__init__(name)
        
    @abstractmethod
    def variables(self):
        pass