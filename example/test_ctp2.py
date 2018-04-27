'''
Created on 14 Feb 2018

@author: Bryan
'''
import sys
sys.path.append("..")

from pyltm.model import Gltm
from pyltm.model import DiscreteVariable, SingularContinuousVariable
from pyltm.reasoner import NaturalCliqueTreePropagation, Evidence
from pyltm.io import BifParser
from pyltm.data import ContinuousDatacase
import numpy as np

if __name__ == '__main__':
#     modelfile = "glass.bif"
#     varNames = ["RI","Na","Mg","Al","Si","K","Ca","Ba","Fe"]
#     data = [1.51793,12.79,3.5,1.12,73.03,0.64,8.77,0,0]
    modelfile = "continuoustoy.bif"
    varNames = ["x"]
    data = [0]
    
    bifparser = BifParser()
    net = bifparser.parse(modelfile)
    
    # set up evidence
    datacase = ContinuousDatacase.create(varNames)
    datacase.synchronize(net)
    datacase.putValues(data)
    evidence = datacase.getEvidence()
    
    ctp = NaturalCliqueTreePropagation(net)
    print(ctp._tree)
    ctp.use(evidence)
    ctp.propagate()
    loglikelihood = ctp.loglikelihood
    print("Loglikelihood: ", loglikelihood)