'''
Created on Nov 12, 2013

@author: alex, nico
'''
class arff:
    
    def __init__(self, filename):
        self.attr_value_map = dict()
        self.attrs = []
        self.data = []
        self.__read(filename)
        
        self.x_names = self.attrs[:-1]
        self.y_name = self.attrs[-1]
    
    def __len__(self):
        return len(self.data)
    
    def n_dim(self):
        return len(self.x_names)
    
    def is_relevant(self, s):
        return s != '' and '%' not in s and s[:9].lower() != '@relation' 
        
    def __read(self, filename):
        file = open(filename) 
        raw = file.read().split('\n')
        file.close()
        raw = [s for s in raw if self.is_relevant(s)]

        attributes = [s for s in raw if s[:10].lower() == '@attribute']

        for a in attributes:
            i_real = a.find('real')
            if i_real != -1:
                attr_name = a[10:i_real].replace(' ','')
                attr_name = attr_name.replace('\t', '')
                attr_value = ['real']
                self.attr_value_map[attr_name] = attr_value
                self.attrs.append(attr_name)
            else:
                i_open_curly = a.index('{')
                i_close_curly = a.index('}')
                attr_values = a[i_open_curly+1 : i_close_curly]
                attr_values = attr_values.replace(' ', '')
                attr_values = set(attr_values.split(','))
                attr_name = a[10:i_open_curly].replace(' ','')
                attr_name = attr_name.replace('\t', '')
                self.attr_value_map[attr_name] = attr_values
                self.attrs.append(attr_name)
        
        try:
            i_data = raw.index('@data')
        except ValueError:
            i_data = raw.index('@data'.upper())
        obs = raw[i_data+1:]
        
        for o in obs:
            o = o.replace(' ','')
            o = o.split(',')
            datapoint = {}
            for a, v in zip(self.attrs, o):
                datapoint[a] = v
            self.data.append(datapoint)





