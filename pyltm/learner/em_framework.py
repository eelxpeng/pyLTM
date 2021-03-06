'''
Created on 11 Sep 2018

@author: Bryan
'''
from pyltm.data import ContinuousDatacase
from pyltm.reasoner import NaturalCliqueTreePropagation, Evidence
from pyltm.model import Gltm, DiscreteBeliefNode, ContinuousBeliefNode
from pyltm.reasoner import DiscreteClique, MixedClique
from .discrete_clique_sufficient_statistics import DiscreteCliqueSufficientStatistics
from .mixed_clique_sufficient_statistics import MixedCliqueSufficientStatistics
from pyltm.model.parameter import cptparameter

class EMFramework(object):
    '''
    Perform EM estimation for latent tree model
    '''


    def __init__(self, model, batch_size):
        '''
        model: Gltm
        '''
        self._model = model
        self.sufficientStatistics, self.batchSufficientStatistics = self.initializeSufficientStatistics(batch_size)
        
    def initializeSufficientStatistics(self, batch_size):
        ctp = NaturalCliqueTreePropagation(self._model)
        ctp.initializePotentials()
        tree = ctp.cliqueTree()
        cliques = tree.cliques
        sufficientStatistics = [None]*len(cliques)
        batchSufficientStatistics = [None]*len(cliques)
        for i in range(len(cliques)):
            if isinstance(cliques[i], DiscreteClique):
                sufficientStatistics[i] = DiscreteCliqueSufficientStatistics(cliques[i], batch_size)
                batchSufficientStatistics[i] = DiscreteCliqueSufficientStatistics(cliques[i], batch_size)
            elif isinstance(cliques[i], MixedClique):
                sufficientStatistics[i] = MixedCliqueSufficientStatistics(cliques[i], batch_size)
                batchSufficientStatistics[i] = MixedCliqueSufficientStatistics(cliques[i], batch_size)
            else:
                raise Exception("unknown type of clique")
        return sufficientStatistics, batchSufficientStatistics
        
    def reset(self):
        for stat in self.batchSufficientStatistics:
            stat.reset()
        
    def stepwise_e_step(self, data, varNames):
        '''collect sufficient statistics for each variable
        data: 2d numpy array
        varNames: list of string
        '''
        ctp = NaturalCliqueTreePropagation(self._model)
        tree = ctp.cliqueTree()
        cliques = tree.cliques

        # set up evidence
        datacase = ContinuousDatacase.create(varNames)
        datacase.synchronize(self._model)
        
        for i in range(len(data)):
            datacase.putValues(data[i])
            evidence = datacase.getEvidence()
            ctp.use(evidence)
            ctp.propagate()
            
            for j in range(len(cliques)):
                self.batchSufficientStatistics[j].add(cliques[j].potential)
                
        # construct variable to statisticMap
        variableStatisticMap = dict()
        for node in self._model.nodes:
            clique = tree.getClique(node.variable)
            index = cliques.index(clique)
            variableStatisticMap[node.variable] = (self.sufficientStatistics[index], self.batchSufficientStatistics[index])
        return variableStatisticMap
    
    def stepwise_m_step(self, variableStatisticMap, learning_rate):
        for node in self._model.nodes:
            statistics, batchStatistics = variableStatisticMap[node.variable]
            statistics.update(batchStatistics, learning_rate)
            if isinstance(node, ContinuousBeliefNode):
                cgparameters = statistics.computePotential(node.variable)
                for i in range(node.potential.size):
                    node.potential.get(i).mu[:] = cgparameters[i].mu
                    node.potential.get(i).covar[:] = cgparameters[i].covar
                    # node.potential.get(i).mu[:] = node.potential.get(i).mu + learning_rate * (cgparameters[i].mu - node.potential.get(i).mu)
                    # node.potential.get(i).covar[:] = node.potential.get(i).covar + learning_rate * (cgparameters[i].covar - node.potential.get(i).covar)
            elif isinstance(node, DiscreteBeliefNode):
                cptparameter = statistics.computePotential(node.variable)
                node.potential.parameter.prob[:] = cptparameter.prob
                # node.potential.parameter.prob[:] = node.potential.parameter.prob + learning_rate * (cptparameter.prob - node.potential.parameter.prob) 
    
    def stepwise_em_step(self, data, varNames, learning_rate):
        self.reset()
        variableStatisticMap = self.stepwise_e_step(data, varNames)
        self.stepwise_m_step(variableStatisticMap, learning_rate)
        
        
        