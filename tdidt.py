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
    
arff_data = arff('Data/betterZoo.arff')

class Node:
    
    def __init__(self, data, y_name, x_names, attr_map, 
                 build = True, name = ''):
        self.name = name
        self.data = data
        self.y_name = y_name
        self.x_names = x_names
        self.attr_map = attr_map
        self.T = float(len(data))
        
        if self.T:
            self.entropy = 0
            self.__calc_entropy()
        else:
            self.entropy = None
        
        self.split_on = None
        self.children = None
        if build and self.entropy:
            self.split_on = self.__argmax_gain_info()
            self.children = self.__split(self.split_on)
        
        self.CLASS = None
        if self.entropy == 0:
            self.CLASS = self.data[0][self.y_name]
    
    def __calc_entropy(self):
        C = {}
        for c in self.attr_map[self.y_name]:
            C[c] = 0
        for ob in self.data:
            y_value = ob[self.y_name]
            C[y_value] += 1.
        for freq in C.values():
            if freq > 0:
                self.entropy -= freq/self.T * math.log(freq/self.T, 2)
    
    def __split(self, x_name, build = True):
        values = self.attr_map[x_name]
        split_data = {}
        child_nodes = {}
        for v in values:
            split_data[v] = []
        for d in self.data:
            split_data[d[x_name]].append(d) 
        for v in split_data:
            d = split_data[v]
            x_names = [name for name in self.x_names if name != x_name]
            if len(d) > 0:
                node = Node(d, self.y_name, x_names, self.attr_map, 
                            build, self.name + '->' + x_name + '=' + str(v))
                child_nodes[v] = node
        return child_nodes
    
    def __gain_info(self, x_name):
        Eentropy = 0
        child_nodes = self.__split(x_name, build = False)
        for child_node in child_nodes.values():
            Eentropy +=  child_node.T/self.T * child_node.entropy
        return self.entropy - Eentropy
    
    def __argmax_gain_info(self):
        argmax = None
        max_gain = -float('inf')
        for x_name in self.x_names:
            tmp_gain = self.__gain_info(x_name)
            if tmp_gain > max_gain:
                argmax = x_name
                max_gain = tmp_gain
        return argmax
    
    def classify(self, datapoint):
        if self.children:
            attr_value = datapoint[self.split_on]
            print self.split_on, ':', attr_value
            child = self.children[attr_value]
            child.classify(datapoint)
        else:
            print self.y_name, ':', self.CLASS
    
    def print_tree(self):
        if self.children:
            for child_name in self.children:
                child = self.children[child_name]
                child.print_tree()
        else:
            print self.name[2:] + '->' + self.CLASS

root = Node(arff_data.data, arff_data.y_name, arff_data.x_names, arff_data.attr_value_map)
root.print_tree()
    




