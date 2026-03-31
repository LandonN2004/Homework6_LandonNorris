#region imports
from scipy.optimize import fsolve
import numpy as np
from Fluid import Fluid
from Node import Node
#endregion
# region class definitions
class PipeNetwork():
    #region constructor
    def __init__(self, Pipes=[], Loops=[], Nodes=[], fluid=Fluid()):
        """
        The pipe network is built from pipe, node, loop, and fluid objects.
        :param Pipes: a list of pipe objects
        :param Loops: a list of loop objects
        :param Nodes: a list of node objects
        :param fluid: a fluid object
        """
        #region attributes
        self.loops=Loops
        self.nodes=Nodes
        self.Fluid=fluid
        self.pipes=Pipes
        #endregion
    #endregion

    #region methods
    def findFlowRates(self):
        """
        a method to analyze the pipe network and find the flow rates in each pipe
        given the constraints of: i) no net flow into a node and ii) no net pressure drops in the loops.
        :return: a list of flow rates in the pipes
        """
        # There are 10 unknown pipe flows. One node equation is linearly dependent,
        # so we use (number of nodes - 1) node equations plus all loop equations.
        Q0=np.full(len(self.pipes),10.0)
        def fn(q):
            for i in range(len(self.pipes)):
                self.pipes[i].Q=q[i]
            L=self.getNodeFlowRates()[:-1]
            L+=self.getLoopHeadLosses()
            return L
        FR=fsolve(fn,Q0)
        for i in range(len(self.pipes)):
            self.pipes[i].Q=FR[i]
        return FR

    def getNodeFlowRates(self):
        qNet=[n.getNetFlowRate() for n in self.nodes]
        return qNet

    def getLoopHeadLosses(self):
        lhl=[l.getLoopHeadLoss() for l in self.loops]
        return lhl

    def getPipe(self, name):
        for p in self.pipes:
            if name == p.Name():
                return p

    def getNodePipes(self, node):
        l=[]
        for p in self.pipes:
            if p.oContainsNode(node):
                l.append(p)
        return l

    def nodeBuilt(self, node):
        for n in self.nodes:
            if n.name==node:
                return True
        return False

    def getNode(self, name):
        for n in self.nodes:
            if n.name==name:
                return n

    def buildNodes(self):
        for p in self.pipes:
            if self.nodeBuilt(p.startNode)==False:
                self.nodes.append(Node(p.startNode,self.getNodePipes(p.startNode)))
            if self.nodeBuilt(p.endNode)==False:
                self.nodes.append(Node(p.endNode,self.getNodePipes(p.endNode)))

    def printPipeFlowRates(self):
        for p in self.pipes:
            p.printPipeFlowRate()

    def printNetNodeFlows(self):
        for n in self.nodes:
            print('net flow into node {} is {:0.6f} L/s'.format(n.name, n.getNetFlowRate()))

    def printLoopHeadLoss(self):
        for l in self.loops:
            print('head loss for loop {} is {:0.6f} m'.format(l.name, l.getLoopHeadLoss()))
    #endregion
# endregion
