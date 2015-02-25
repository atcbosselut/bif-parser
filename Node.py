'''
This is a class that implements a node in a Bayesian network. 

The distribution field is a dictionary containing the conditional probability distribution of the node given its parents.
The keys to the dictionary are tuples containing the names of the possible states of the node and the evidence of the parents
for each line in the CPD table. If a node has no parents, the distribution will store the marginal distribution.

This is my implementation for a node. Feel free to alter it based on your own design for what a node should look like.
If you change the node constructor parameters, however, remember to change the BIF parse script so that the number of variables
received by the constructor is the same as the number of variables given to the constructor. 

'''

import numpy

__author__ = "Antoine Bosselut"
__version__ = "1.0.3"
__maintainer__ = "Antoine Bosselut"
__email__ = "antoine.bosselut@uw.edu"
__status__ = "Prototype"

class Node:
    def __init__(self, theName, theType, numberStates, theStates, theProperty):
        self.name =  theName
        self.myType = theType
        self.numStates = numberStates
        self.states = theStates
        self.parents = []
        self.children = []
        self.information = []
        self.dist = None
        self.myProperty = theProperty
        self.marginal = None
    
    #Add children when building the BN
    def addChildren(self, theChildren):
        for a in theChildren:
            self.children.append(a)

    
    #Add parents to a state when building the BN
    def addParent(self, theParents):
        for a in theParents:
            self.parents.append(a)
    
    #Check whether this is a root state with no parents
    def isRoot(self):
        return self.numParents()==0
        
    #Check whether this is a leaf state with no parents    
    def isLeaf(self):
        return self.numChildren()==0
    
    #Get the name of the node
    def getName(self):
        return self.name
    
    #Return the number of children of this node
    def numChildren(self):
        return len(self.children)
    
    #Return the possible states of the node
    def getStates(self):
        return self.states

    #Return the number of states this node has
    def numStates(self):
        return self.numStates
    
    #Return the number of parents of this node
    def numParents(self):
        return len(self.parents)

    #Return the parents of the node
    def getParents(self):
        return self.parents

    #Return the children of the node
    def getChildren(self):
        return self.children
    
    #Set the Probability Distribution of this node
    def setDist(self, distribution):
        self.dist = distribution
        if self.isRoot():
            self.marginal = {}
            for key, value in distribution.iteritems():
                i=0
                while i<len(value):
                    self.marginal[key[i]] = value[i]
                    i+=1
    
    #Return the probability distribution of thise node
    def getDist(self):
        return self.dist

    #receive the information from a factor based on new information. 
    #Organize this information where it belongs in the information vector
    def receiveMarginal(self, message, factor):
        if not self.information:
            self.information = [0]*(self.numChildren()+(not self.isRoot()))
        #If this node is the child in the CPD for the factor, set the information index to 0.
        if factor.getIndex(self.getName()) == 0:
            self.information[0] = message
        else:
            childName = factor.getFields()[0].getName()
            i=0
            while i<len(self.children):
                if childName == self.children[i].getName():
                    break
                i+=1
            self.information[i+(not self.isRoot())] = message

    def updateMarginal(self):
        if self.isRoot():
            pass
        else:
            thesum=0
            vals = {}
            vals = {(state,): 1 for state in self.states}
            #for state in self.states:
             #   vals[state] = 1
            #For each factor we receive information from
            for a in self.information:
                #For this evidence in the message
                print("Keys: ")
                print a.keys()
                for ev in a.keys():
                    #print ("Information: ")
                    #print a
                    #print("States: ")
                    #print vals
                    #print ev
                    #print vals[ev]
                    vals[ev] = vals[ev]*a[ev]
            print("vals: ")
            print vals
            for val in vals.itervalues():
                thesum+=val
            for key in vals.keys():
                if thesum != 0:
                    vals[key] = vals[key]/thesum
            self.marginal = vals


    #Return marginal distribution of node variable in node 
    def getMarginal(self):
        return self.marginal

    def sendMarginal(self, targetFactor):
        #TODO: Remove contribution of target factor from marginal and then send factor to
        index = -1
        cacheQuery = targetFactor.getFields()[0].getName()
        if self.isRoot():
            return self.marginal
        if (cacheQuery == self.name) and (not self.isRoot()):
            index=0
        else:
            j=0
            while j < len(self.children):
                if cacheQuery == self.getChildren()[j].getName():
                    index = j + (not self.isRoot())
                j+=1
        thesum=0
        vals = {state: 1 for state in self.states}
        i=0
        while i<len(self.information):
            if (i != index):
                for ev in self.information[i].keys():
                    #print ("Information2: ")
                    #print a
                    #print("States2: ")
                    #print vals
                    #print ev
                    #print vals[ev]
                    vals[ev] = vals[ev]*a[ev]
            i+=1
        for val in vals.itervalues():
            thesum+=val
            print("Sum: %s" %thesum)
        for key in vals.keys():
            vals[key] = vals[key]/thesum
        return vals
        #TODO: Send information without index "index"

    def printNode(self):
        print self.getName()
        print "Parents: "
        for b in self.parents:
            print c.getName()
        print "CPD: "
        print self.getDist()
        print "Children: "
        for c in a.children:
            print c.getName()
        print ""

