#!/usr/bin/env python

'''
BeliefPropagation.py

'''

import Node
import Factor
import BIFParser
import numpy as np

__author__ = "Antoine Bosselut"
__version__ = "1.0.1"
__maintainer__ = "Antoine Bosselut"
__email__ = "antoine.bosselut@uw.edu"
__status__ = "Prototype"


f = open("hw3-dist/%s" %sys.argv[1],"r")
BIF = f.readlines()

BIF = BIFParser.fixWhiteSpace(BIF)
BN = BIFParser.parseBIF(BIF)

factors = []
for nodes in BN:
	if not nodes.isRoot():
		factors.append(Factor(nodes.getDist(), [nodes].extend(nodes.getParents()))