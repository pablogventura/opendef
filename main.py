# -*- coding: utf-8 -*-
#!/usr/bin/env python   
from minion import is_isomorphic
from parser import stdin_parser
from minion import automorphisms, isomorphisms, is_isomorphic_to_any
from itertools import chain

class Counterexample(Exception):
    def __init__(self,ce):
        self.ce = ce

def main():
    g=stdin_parser()
    print(is_open_rel(g,("T0",)))
    

class GenStack(object):
    def __init__(self, generator):
        self.stack = [generator]
    
    def add(self,generator):
        self.stack.append(generator)
    
    def next(self):
        result = None
        while result is None:
            try:
                result = next(self.stack[-1])
            except IndexError:
                raise StopIteration
            except StopIteration:
                del self.stack[-1]
        return result
            
        


def is_open_rel(model, target_rels):
    
    base_rels = tuple((r for r in model.relations if r not in target_rels))
    print(base_rels)
    spectrum = sorted(model.spectrum(target_rels),reverse=True)
    size = spectrum[0]

    S = set()
    
    genstack = GenStack(model.substructures(size))
    
    while True:
        try:
            current = genstack.next()
            print("avanza")
        except StopIteration:
            break
        except:
            print (type(subsgen))
            assert False
        iso = is_isomorphic_to_any(current, S, base_rels)
        if iso:
            if not iso.iso_wrt(target_rels):
                raise Counterexample(iso)
        else:
            for aut in automorphisms(current,base_rels):
                if not aut.aut_wrt(target_rels):
                    raise Counterexample(aut)
            S.add(current)
            try:
                size = next(x for x in spectrum if x < len(current)) # EL SIGUIENTE EN EL ESPECTRO QUE SEA MAS CHICO QUE LEN DE SUBUNIVERSE
                genstack.add(current.substructures(size))
                print("enganchado")
            except StopIteration:
                # no tiene mas hijos
                pass
    return True




if __name__ == "__main__":
    main()
