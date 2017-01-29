# -*- coding: utf-8 -*-
#!/usr/bin/env python

    
class Relation(object):
    """
    Relation
    """
    def __init__(self,sym,arity):
        self.sym = sym
        self.arity = arity
        self.r = set()
    
    def add(self, t):
        self.r.add(t)
    
    def __repr__(self):
        return "Relation " + self.sym + " " + str(self.r)
    
    def __call__(self, *args):
        return args in self.r
    
    def table(self, subuniverse):
        """
        Relation table reducted to subuniverse
        """
        result = []
        subuniverse= set(subuniverse)
        for t in self.r:
            if set(t) <= subuniverse:
                result.append(t)
        return result

