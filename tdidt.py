'''
Created on Nov 12, 2013

@author: alex
'''
import sys
import math
from arff import arff

# filename = sys.argv[1]

def chdir():
    import os
    os.chdir('/Users/alex/Documents/workspace/classifier/')
chdir()
    
arff_data = arff('Data/weather.nominal.arff')

class Node:
    
    def __init__(self, data, y_name, x_names, attr_map):
        self.data = data
        self.y_name = y_name
        self.x_names = x_names
        self.attr_map = attr_map
        self.T = float(len(data))
        
        self.entropy = 0
        self.__calc_entropy()
                
    def __calc_entropy(self):
        C = {}
        for c in self.attr_map[self.y_name]:
            C[c] = 0
        for o in self.data:
            y_value = o[self.y_name]
            C[y_value] += 1.
        for freq in C.values():
            if freq > 0:
                self.entropy -= freq/self.T * math.log(freq/self.T)
    
    def __split(self, x_name):
        values = self.attr_map[x_name]
        split_data = {}
        child_nodes = []
        for v in values:
            split_data[v] = []
        for d in self.data:
            split_data[d[x_name]].append(d) 
        for d in split_data.values():
            x_names = [name for name in self.x_names if name != x_name]
            if len(d) > 0:
                node = Node(d, self.y_name, x_names, self.attr_map)
                child_nodes.append(node)
        return child_nodes
    
    def gain_info(self, x_name):
        e_entropy = 0
        child_nodes = self.__split(x_name)
        for child_node in child_nodes:
            e_entropy -=  child_node.T/self.T * child_node.entropy
        return self.entropy - e_entropy
    
    def argmax_gain_info(self):
        argmax = None
        max_gain = -float('inf')
        for x_name in self.x_names:
            tmp_gain = self.gain_info(x_name)
            if tmp_gain > max_gain:
                argmax = x_name
                max_gain = tmp_gain
        return argmax
            
root = Node(arff_data.data, arff_data.y_name, arff_data.x_names, arff_data.attr_value_map)
root.argmax_gain_info()
    




