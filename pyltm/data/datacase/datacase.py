'''
Created on 27 Apr 2018

@author: Bryan
'''
from abc import ABCMeta, abstractmethod
from pyltm.reasoner import Evidence

class Datacase(object):
    '''
    classdocs
    '''
    def __init__(self, vars):
        '''
        Param: list of Variable
        '''
        pass
    
    @abstractmethod
    def getEvidence(self):
        '''return Evidence'''
        pass
    
    @abstractmethod
    def synchronize(self, model):
        pass
    