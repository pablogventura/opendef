# -*- coding: utf-8 -*-
#!/usr/bin/env python


class Isomorphism(object):
    def __init__(self,d):
        self.values = d
    def __call__(self, x):
        return self.d[x]
    def __repr__(self):
        return "Isomorphism(%s)" % self.values
    def iso_wrt(self,target_rels):
        for r in target_rels:
            for t in r:
                if not r(tuple(self(x) for x in t)):
                    return False
        return True


class Automorphism(Isomorphism):
    def __repr__(self):
        return "Automorphism(%s)" % self.values
    def aut_wrt(self,target_rels,model):
        for r in target_rels:
            for t in r.restrict(model.universe):
                if not r(tuple(self(x) for x in t)):
                    return False
        return True

