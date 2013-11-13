'''
Created on Nov 12, 2013

@author: alex
'''
import sys
from arff import arff

# filename = sys.argv[1]

def chdir():
    import os
    os.chdir('/Users/alex/Documents/workspace/classifier/')
chdir()
    
weather = arff('Data/weather.nominal.arff')
