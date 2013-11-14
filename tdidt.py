'''
Created on Nov 12, 2013

@author: alex, nico
'''
import sys
import math
from arff import arff

# filename = sys.argv[1]

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

        # Recursevily builds its children to create the full tree
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
    
    # Creates a split in the current node by the given attribute name, and returns the children nodes
    # Updates the node and children if build is true
    def __split(self, x_name, build = True):
        values = self.attr_map[x_name]
        split_data = {}
        child_nodes = {}

        # Most frequent y keeps track of the attributes that share the same classification
        # while most frequent al keeps track of the most frequent attribute, since on some cases,
        # there is an item that is the only classification
        most_frequent_y = {}


        for v in values:
            split_data[v] = []
            
        for y_value in self.attr_map[self.y_name]:
            most_frequent_y[y_value] = []

        for d in self.data:
            if d[x_name] != '?':
                most_frequent_y[d[self.y_name]].append(d[x_name])
                    
        for d in self.data:
            # If this is an unkown attribute
            if d[x_name] == '?':
                max_frequency_x = 0
                max_x = None

                # Finds the most frequent attribute that is classified the same,
                # and finds the most frequent attribute in general
                for v in values:
                    if most_frequent_y[d[self.y_name]].count(v) > max_frequency_x:
                        max_frequency_x = most_frequent_y[d[self.y_name]].count(v)
                        max_x = v
                # Uses the most frequent attribute in the same class, except when 
                # it is the only one is it's class
                if max_x != None:
                    split_data[max_x].append(d)


            # For known example
            else:
                split_data[d[x_name]].append(d) 

        # Splits the data and creates the children nodes
        for v in values:
            d = split_data[v]
            x_names = [name for name in self.x_names if name != x_name]
            node = Node(d, self.y_name, x_names, self.attr_map, 
                        build, self.name + '->' + x_name + '=' + str(v))
            child_nodes[v] = node
        return child_nodes

    # Finds the entropy for a given attribute x_name and returns the gain     
    def __gain_info(self, x_name):
        Eentropy = 0
        child_nodes = self.__split(x_name, build = False)
        for child_node in child_nodes.values():
            if child_node.entropy:
                Eentropy +=  child_node.T/self.T * child_node.entropy
        return self.entropy - Eentropy

    # Finds the gain for all remaining attributes and returns attribute causing the most gain    
    def __argmax_gain_info(self):
        argmax = None
        max_gain = -float('inf')
        for x_name in self.x_names:
            tmp_gain = self.__gain_info(x_name)
            if tmp_gain > max_gain:
                argmax = x_name
                max_gain = tmp_gain
        return argmax
    
    # Takes in a datapoint and classifies that datapoint using our tree. 
    # If print steps is true then it prints out the steps it took in classification
    def classify(self, datapoint, print_steps = True):
        if self.children:
            attr_value = datapoint[self.split_on]
            if print_steps: 
                print self.split_on, ':', attr_value
            # Finds the more common branch
            if attr_value == '?':
                frequency = 0
                max_child = None
                for child in self.children:
                    if frequency < self.children[child].T:
                        max_child = self.children[child]
                        frequency = self.children[child].T
                return max_child.classify(datapoint, print_steps)
            else:
                child = self.children[attr_value]
                return child.classify(datapoint, print_steps)
        else:
            if print_steps: 
                print self.y_name, ':', self.CLASS
            return self.CLASS
    
    def print_tree(self):
        if self.children:
            for child_name in self.children:
                child = self.children[child_name]
                child.print_tree()
        else:
            print self.name[2:] + '->' + str(self.CLASS)

def main(arff_file):
    arff_data = arff(arff_file)
    root = Node(arff_data.data, arff_data.y_name, arff_data.x_names, arff_data.attr_value_map)
    
    print '\nTree'
    root.print_tree()
    
    print '\nCLASSIFY: For the first item in the data set'
    a = root.data[0]
    a_class = root.classify(a, True)
    print 'final result:', a_class    
    
    print '\nCROSS VALIDATION: Percent Correct'
    number_correct = 0.
    for data_point in arff_data.data:
        arff_data_copy = list(arff_data.data)
        arff_data_copy.remove(data_point)
        current_root = Node(arff_data_copy, arff_data.y_name, arff_data.x_names, arff_data.attr_value_map)        
        current_class = current_root.classify(data_point, False)
        if data_point[arff_data.y_name] == current_class:
            number_correct += 1.
            
    number_data_points = len(arff_data.data)
    print number_correct/number_data_points


if __name__ == '__main__':
    main(sys.argv[1:][0])

