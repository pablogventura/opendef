# -*- coding: utf-8 -*-
#!/usr/bin/env python   
from counterexample import Counterexample
from minion import is_isomorphic
from parser import stdin_parser
from minion import automorphisms, isomorphisms, is_isomorphic_to_any, MinionSol
from itertools import chain
from misc import indent

def main():
    model = stdin_parser()
    targets_rel = tuple(sym for sym in model.relations.keys() if sym[0]=="T")
    if not targets_rel:
        print("ERROR: NO TARGET RELATIONS FOUND")
        return
    is_open_rel(model,targets_rel)
        

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
    if spectrum:
        size = spectrum[0]
    else:
        size = 0
    print ("Spectrum = %s"%spectrum)
    isos_count = 0
    auts_count = 0
    S = set()
    
    genstack = GenStack(model.substructures(size))
    try:
        while True:
            try:
                current = genstack.next()
            except StopIteration:
                break
            iso = is_isomorphic_to_any(current, S, base_rels)
            if iso:
                isos_count += 1
                if not iso.iso_wrt(target_rels):
                    raise Counterexample(iso)
            else:
                for aut in automorphisms(current,base_rels):
                    auts_count += 1
                    if not aut.aut_wrt(target_rels):
                        raise Counterexample(aut)
                S.add(current)

                try:
                    # EL SIGUIENTE EN EL ESPECTRO QUE SEA MAS CHICO QUE LEN DE SUBUNIVERSE
                    size = next(x for x in spectrum if x < len(current)) 
                    genstack.add(current.substructures(size))
                except StopIteration:
                    # no tiene mas hijos
                    pass
        print("DEFINABLE")
        print("\nFinal state: ")
        
    except Counterexample as ce:
        print("NOT DEFINABLE")
        print("Counterexample:")
        print(indent(repr(ce.ce)))
        print("\nState before abort: ")
    except KeyboardInterrupt:
        print("CANCELLED")
        print("\nState before abort: ")
    
    print ("  Diversity = %s"%len(S))
    if S:
        for k in range(1,max(map(len,S))+1):
            print("    %s-diversity = %s"%(k,len(list(filter(lambda s: len(s)==k,S)))))
    print("  #Auts = %s" % auts_count)
    print("  #Isos = %s" % isos_count)
    print("  %s calls to Minion" % MinionSol.count)



if __name__ == "__main__":
    main()
