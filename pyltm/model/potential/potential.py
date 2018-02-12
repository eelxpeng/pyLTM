'''
Created on 11 Feb 2018

@author: Bryan
'''
from abc import ABCMeta, abstractmethod, abstractproperty
class Potential(metaclass=ABCMeta):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        pass
    @abstractmethod
    def addParentVariable(self, variable):
        pass
    @abstractmethod
    def removeParentVariable(self, variable):
        pass
    @abstractmethod
    def normalize(self, constant):
        pass
    @abstractmethod
    def clone(self):
        pass
    @abstractproperty
    def function(self):
        pass
    
    @abstractmethod
    def marginalize(self, variable):
        pass
    
    def reorderStates(self, variable, order):
        pass