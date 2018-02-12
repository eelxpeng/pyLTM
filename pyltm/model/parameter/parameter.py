'''
Created on 12 Feb 2018

@author: Bryan
'''
from abc import ABCMeta, abstractmethod
class Parameter(metaclass=ABCMeta):
    '''
    classdocs
    '''
    def __init__(self):
        '''
        Constructor
        '''
        pass
    
    @abstractmethod
    def copy(self):
        pass

    
        