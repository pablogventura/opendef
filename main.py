# -*- coding: utf-8 -*-
#!/usr/bin/env python   
from minion import is_isomorphic
from parser import stdin_parser
from minion import automorphisms, isomorphisms, is_isomorphic_to_any

class Counterexample(Exception):
    def __init__(self,ce):
        self.ce = ce

def main():
    g=stdin_parser()
    print(is_open_rel(g,["U"]))
    

def is_open_rel(model, target_rels):
    
    base_rels = [r for r in model.relations if r not in target_rels]
    print(base_rels)
    spectrum = sorted(model.spectrum(target_rels),reverse=True)
    size = spectrum[0]

    S = set()
    
    subsgen = model.substructures(size)
    
    while True:
        try:
            current = next(subsgen)
        except StopIteration:
            break
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
                subsgen = chain(current.substructures, subsgen)
            except StopIteration:
                # no tiene mas hijos
                pass
    return True




if __name__ == "__main__":
    main()
