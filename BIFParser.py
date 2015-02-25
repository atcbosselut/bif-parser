#!/usr/bin/env python

'''
This is a script that parses a BIF (Bayesian Implementation Format) file passed by the command line.

'''

import Node
import sys
import re

__author__ = "Antoine Bosselut"
__version__ = "1.0.2"
__maintainer__ = "Antoine Bosselut"
__email__ = "antoine.bosselut@uw.edu"
__status__ = "Prototype"


f = open("hw3-dist/%s" %sys.argv[1],"r")
BIF = f.readlines()

def fixWhiteSpace(BIF_white):
    i=0
    while i<len(BIF_white):
        if BIF_white[i] == "\n": #or a[i] == "}\n":
            #Remove whitespace lines
            del BIF_white[i]
        else:
            #Add a space after every piece of punctuation. This will make all distinct words separated only by punctuation
            #distinct entries in the list of values when we split a line
            BIF_white[i]=re.sub('([,])', r'\1 ', BIF_white[i])

            #Get rid of white space at the beginning and end
            BIF_white[i]=BIF_white[i].strip()
            i+=1
    #print BIF_white
    return BIF_white


def parseBIF(BIF):
    i=0
    nodes=[]
    while i<len(BIF):
        lineList = BIF[i].split()
        #If this line is a variable declaration
        if lineList[0] == 'variable':
            name = lineList[1]
            i=i+1
            #While the end of the declaration is not parsed
            while BIF[i]!='}':
                lineList = BIF[i].split()
                if lineList[0] == 'type':
                    #Parse the variable type - will be discrete in most cases
                    theType = lineList[1]

                    #Parse the number of states
                    numStates = int(lineList[3])

                    #Remove commas from the names of possible states for this variable
                    lineList[6:6+numStates] = [x.strip(",") for x in lineList[6:6+numStates]]

                    #Set a tuple containing the states
                    theStates = tuple(lineList[6:6+numStates])

                    #Set property to be null string
                    theProperty=""
                elif lineList[0]=='property':
                    #If there is a property, record it
                    theProperty=" ".join(lineList[1:])
                i+=1
            #Append the new node to the list of nodes
            #THIS IS WHERE YOU MUST CHANGE THE INSTANTIATION OF A NODE IF YOU CHANGE THE CONSTRUCTOR IN THE NODE CLASS
            nodes.append(Node.Node(name,theType,numStates,theStates, theProperty))
        elif lineList[0] == 'probability':
            #If this is declaration is a probability distribution

            #Add spaces before and after parentheses
            BIF[i]=re.sub('([()])', r' \1 ', BIF[i])

            lineList = BIF[i].split()

            #Find the query variable
            for theNode in nodes:
                if theNode.getName() == lineList[2]:
                    temp = theNode
                    break

            #Add parents to the query variables if there are any        
            if lineList[3] == '|':
                j=4
                while lineList[j] != ')':
                    for parent in nodes:
                        #Find the parents in the list of nodes
                        if parent.getName() == lineList[j].strip(","):
                            temp.addParent([parent])
                            parent.addChildren([temp])
                            break;
                    j+=1
            i+=1
            theCPD = {}
            #While the end of the declaration is not parsed
            while BIF[i]!='}':   
                lineList = BIF[i].split()

                if lineList[0] == 'table':
                    #Get rid of the identifier
                    del lineList[0]

                    #Get rid of commas and semicolons
                    prob = [x.translate(None, ",;") for x in lineList]

                    #Store the distribution (this is a marginal distribution)
                    theCPD[temp.getStates()] = tuple([float(h) for h in prob])

                elif lineList[0][0] == "(":
                    #Remove all punctuation from the evidence names and the probability values
                    lineList = [states.translate(None,"(,;)") for states in lineList]

                    #In the CPD dictionary key, the states of the node are stored first. The second tuple is that of the parent values
                    theCPD[(temp.getStates(), tuple(lineList[:temp.numParents()]))] = tuple([float(h) for h in lineList[temp.numParents():]])                    
                i+=1
            print theCPD
            temp.setDist(theCPD)
        else:
            i=i+1
    return nodes

def printNodes(nodes):
    for a in nodes:
        print a.getName()
        print "Parents: "
        for b in a.parents:
            print b.getName()
        print "CPD: "
        print a.getDist()
        print "Children: "
        for c in a.children:
            print c.getName()
        print ""

'''def printFactors(factors):
    for a in factors:
        print a.get'''

BIF = fixWhiteSpace(BIF)
nodes = parseBIF(BIF)
#printNodes(nodes)




