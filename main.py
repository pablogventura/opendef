# -*- coding: utf-8 -*-
#!/usr/bin/env python   
from minion import is_isomorphic
from parser import stdin_parser
from minion import automorphisms, isomorphisms, is_isomorphic_to_any, MinionSol
from itertools import chain

class Counterexample(Exception):
    def __init__(self,ce):
        self.ce = ce

def main():
    g=stdin_parser()
    try:
        is_open_rel(g,("T0",))
        print("DEFINABLE")
    except Counterexample as ce:
        print("NOT DEFINABLE")
        print("Counterexample=%s" % ce.ce)
        

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
    spectrum = sorted(model.spectrum(target_rels),reverse=True)
    size = spectrum[0]
    print ("Spectrum=%s"%spectrum)
    isos_count = 0
    auts_count = 0
    S = set()
    
    genstack = GenStack(model.substructures(size))

    while True:
    
        #if auts_count % 50 == 0:
        #    print("#Auts=%s Diversity=%s" % (auts_count,len(S)))
        #if isos_count:
        #    print("#Isos=%s" % isos_count)
        try:
            current = genstack.next()
        except StopIteration:
            break
        iso = is_isomorphic_to_any(current, S, base_rels)
        if iso:
            isos_count += 1
            if not iso.iso_wrt(target_rels):
                print ("Diversity=%s"%len(S)) # TODO las k-diversidades por separado
                raise Counterexample(iso)
        else:
            for aut in automorphisms(current,base_rels):
                auts_count += 1
                if not aut.aut_wrt(target_rels):
                    print ("Diversity=%s"%len(S)) # TODO las k-diversidades por separado
                    raise Counterexample(aut)
            S.add(current)

            try:
                size = next(x for x in spectrum if x < len(current)) # EL SIGUIENTE EN EL ESPECTRO QUE SEA MAS CHICO QUE LEN DE SUBUNIVERSE
                genstack.add(current.substructures(size))
            except StopIteration:
                # no tiene mas hijos
                pass
    print ("Diversity=%s"%len(S)) # TODO las k-diversidades por separado
    for k in range(max(map(len,S))+1):
        print("%s-diversity=%s"%(k,len(list(filter(lambda s: len(s)==k,S)))))
    
    print("*"*80)
    for h in list(filter(lambda s: len(s)==2,S)):
        print(h)
    print("*"*80)
    print("%s calls to Minion" % MinionSol.count)
    print("#Auts=%s Diversity=%s" % (auts_count,len(S)))
    print("#Isos=%s" % isos_count)
    return True




if __name__ == "__main__":
    main()
