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


class ParserError(Exception):
    """
    Sintax error while parsing
    """
    def __init__(self, line, message):
        self.line = line
        self.message = message



            


def stdin_parser():
    """
    Returns parsed Rel_Model from stdin
    """
    linenumber = 1
    relations = {}
    try:
        universe = map(int,input().split()) # first line, universe
        linenumber += 1
        assert input() == "", ("Line #%s must be empty"%linenumber)
        linenumber += 1
        while True:
            # parsing relations
            # format:
            #   symbol number_of_tuples arity
            #   tuples
            #   empty line
            try:
                sym, ntuples, arity = input().split()
                linenumber += 1
            except EOFError:
                # no more relations found
                break

            ntuples,arity = int(ntuples),int(arity)
            relation = Relation(sym,arity)
            for i in range(ntuples):
                relation.add(tuple(map(int,input().split())))
                linenumber += 1
            assert input() == "", ("Relation must finish with empty line at #%s line"%linenumber) # relation MUST finish with empty line
            linenumber += 1
            relations[sym] = relation
    except EOFError:
        raise ParserError(linenumber,"Unexpected EOF")
    
    return RelationalModel(universe,relations)
            
            
        

def main():
    g=stdin_parser()
    print(g)
    

    

if __name__ == "__main__":
    main()
