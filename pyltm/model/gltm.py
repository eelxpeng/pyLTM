'''
Created on 12 Feb 2018

@author: Bryan
'''
from .tree_model import TreeModel

class Gltm(TreeModel):
    '''
    classdocs
    '''

    def __init__(self, name):
        '''
        Constructor
        '''
        super().__init__(name)
        
    def clone(self):
        pass