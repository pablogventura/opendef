# -*- coding: utf-8 -*-
#!/usr/bin/env python


class Isomorphism(object):
    def __init__(self,d,source,target, subtype):
        self.values = d
        self.source = source
        self.target = target
        self.subtype = subtype
        
    def __call__(self, x):
        return self.values[x]
    def __repr__(self):
        return "Isomorphism(%s) from {%s} to {%s}" % (self.values,self.source,self.target)
    def iso_wrt(self,subtype):
        if self.source.rels_sizes(subtype) != self.target.rels_sizes(subtype):
            return False
        for r in subtype:
            for t in self.source.relations[r]:
                if not self.target.relations[r](tuple(self(x) for x in t)):
                    return False
        return True


class Automorphism(object):
    def __init__(self,d,model,subtype):
        self.values = d
        self.model = model
        self.subtype = subtype
    def __call__(self, x):
        return self.values[x]
    def __repr__(self):
        return "Automorphism(%s) from {%s} to {%s}" % (self.values,self.source,self.target)
    def aut_wrt(self,subtype):
        for r in subtype:
            for t in self.model.relations[r]:
                if not self.model.relations[r](tuple(self(x) for x in t)):
                    return False
        return True

