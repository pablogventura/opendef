# -*- coding: utf-8 -*-
#!/usr/bin/env python


class Isomorphism(object):
    def __init__(self,renaming,values):
        self.renaming = list(renaming)
        self.values = list(values)
    def __call__(self, x):
        return self.renaming[self.values[self.renaming.index(x)]]

class Automorphism(Isomorphism):
    pass

