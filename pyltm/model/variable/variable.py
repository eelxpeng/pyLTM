'''
Created on 11 Feb 2018

@author: Bryan
'''
from abc import ABCMeta
class Variable(metaclass=ABCMeta):
    '''
    classdocs
    '''
    _counter = None

    def __init__(self, name=None):
        '''
        Constructor
        '''
        if name is None:
            name, index = Variable._counter.next()
        else:
            name = name.strip()
            index = Variable._counter.nextIndex()
            Variable._counter.encounterName(name)
        self._name = name
        self._index = index
    
    def compareTo(self, o):
        """
        depends on _index, indicating this object created earlier or later than o
        """
        return self._index - o._index
    
    @property
    def name(self):
        return self._name
    
    def setName(self, name):
        self._name = name.strip()
    
    def __str__(self):
        return self.name
        