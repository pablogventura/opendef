# -*- coding: utf-8 -*-
#!/usr/bin/env python


from itertools import combinations
from functools import lru_cache

class RelationalModel(object):
    def __init__(self,universe,relations):
        """
        Relational Model
        Input: a universe list, relations dict
        """
        self.universe= list(universe)
        self.relations = relations

    def subuniverses(self,size):
        for subu in combinations(self.universe,size):
            yield subu
    
    def substructures(self,size):
        for s in self.subuniverses(size):
            relations={}
            for r in self.relations:
                relations[r]=self.relations[r].restrict(s)
            yield RelationalModel(s,relations)

    def __repr__(self):
        return ("RelationalModel(universe=%s,relations=%s)"%(self.universe,self.relations))
    
    @lru_cache(maxsize=None)
    def rels_sizes(self,base_relations):
        return {r:len(self.relations[r]) for r in base_relations}
    
    @lru_cache(maxsize=None)    
    def minion_tables(self,base_relations):
        result = ""
        for r in base_relations:
            result += "%s %s %s\n" % (r, len(self.relations[r]), self.relations[r].arity)
            for t in self.relations[r]:
                result += " ".join(str(self.universe.index(x)) for x in t) + "\n"
            result += "\n"
        return result[:-1]
        
    def minion_constraints(self,base_relations):
        result = ""
        #table([f[0],f[0],f[0]],bv)
        result = ""
        for r in base_relations:
            for t in self.relations[r]:
                result += "table([f["
                result += "],f[".join(str(self.universe.index(x)) for x in t)
                result += "]],%s)\n" % r
        return result        
    def __len__(self):
        return len(self.universe)
