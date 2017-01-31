# -*- coding: utf-8 -*-
#!/usr/bin/env python   
from minion import is_isomorphic
from parser import stdin_parser
from minion import automorphisms, isomorphisms

def main():
    g=stdin_parser()
    l=g.substructures(3)
    a=next(l)
    b=next(l)
    print(a)
    print(b)
    print(list(isomorphisms(a,b)))
    #print(list(automorphisms(g)))
    #print(is_isomorphic(g,g))
    


def is_open_rel(model, target_rels):
    
    spectrum = calc_spectrum(sum(map(lambda x: x.table(),target_rels),[]))
    size = spectrum[0]

    S = set()
    
    subsgen = model.substructures(size)
    
    while True:
        try:
            current = next(subsgen)
        except StopIteration:
            break
        iso = check_isos(current, S)
        if iso:
            if not iso.iso_wrt(target_rels):
                raise Counterexample(iso)
        else:
            for aut in current.automorphisms():
                if not aut.iso_wrt(target_rels):
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
