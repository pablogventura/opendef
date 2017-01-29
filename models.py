# -*- coding: utf-8 -*-
#!/usr/bin/env python


from itertools import combinations


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


    def __repr__(self):
        return ("RelationalModel(universe=%s,relations=%s)"%(self.universe,self.relations))

