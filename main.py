# -*- coding: utf-8 -*-
#!/usr/bin/env python   
from counterexample import Counterexample
from minion import is_isomorphic
from parser import stdin_parser
from minion import automorphisms, isomorphisms, is_isomorphic_to_any, MinionSol
from itertools import chain,count
from misc import indent
from collections import defaultdict
import operator as op
from functools import reduce
import resource
import sys

verbose=sys.stdout.isatty()

latex_tree =""

def childrens_time():
    time = resource.getrusage(resource.RUSAGE_CHILDREN)
    time = time[0]+time[1] #user + system
    return time
    
def ncr(n, r):
    r = min(r, n-r)
    if r == 0: return 1
    numer = reduce(op.mul, range(n, n-r, -1))
    denom = reduce(op.mul, range(1, r+1))
    return numer//denom
    
def main():
    model = stdin_parser()
    targets_rel = tuple(sym for sym in model.relations.keys() if sym[0]=="T")
    if not targets_rel:
        print("ERROR: NO TARGET RELATIONS FOUND")
        return
    is_open_rel(model,targets_rel)

class SetSized(object):
    def __init__(self,values=[]):
        self.dict = defaultdict(set)
        for v in values:
            self.add(v)
    
    def add(self,e):
        self.dict[len(e)].add(e)
    
    def __iter__(self):
        print("WARNING: __iter__ SetSized")
        for i in self.sizes():
            for v in self.iterate(i):
                yield v

    def __len__(self):
        return sum(self.len(s) for s in self.sizes())
    def len(self,size):
        return len(self.dict[size])
    def sizes(self):
        return sorted(self.dict.keys())
    def iterate(self,size):
        return iter(self.dict[size])

class GenStack(object):
    def __init__(self, generator,total=None, pp_d=[]):
        self.stack = [(generator,count(1),total)]
        self.history=set()
        self.pp_d=pp_d
        self.tabs = 0
        self.old_total = float("inf")
    def add(self,generator,total=None):
        self.stack.append((generator,count(1),total))
    def next(self):
        global latex_tree
        global verbose
        result = None
        while result is None or frozenset(result.universe) in self.history:
            try:
                result = next(self.stack[-1][0])
            except IndexError:
                raise StopIteration
            except StopIteration:
                del self.stack[-1]
                #print ("\b"*500)#, end="\r")
        self.history.add(frozenset(result.universe))
        i = next(self.stack[-1][1])
        total = self.stack[-1][2]
        agregar=""
        if self.old_total > total:
            self.tabs +=1
        elif self.old_total < total:
            self.tabs -=1
            latex_tree+=("  " * self.tabs)+"]\n"
            latex_tree+=("  " * self.tabs)+"]\n"
        else:
            latex_tree+=("  " * self.tabs)+"]\n"
            
        self.old_total = total
        if verbose:
            latex_tree+=("  " * self.tabs)+"[.\\{%s\\}\n" % ",".join(str(i) for i in sorted(result.universe))
            print (("Subset %s of %s    \tDiversity:%s" % (i,total,len(self.pp_d)))+30*" ", end="\r")
        return result


def is_open_rel(model, target_rels):
    global latex_tree
    base_rels = tuple((r for r in model.relations if r not in target_rels))
    spectrum = sorted(model.spectrum(target_rels),reverse=True)
    if spectrum:
        size = spectrum[0]
    else:
        size = 0
    print ("Spectrum = %s"%spectrum)
    isos_count = 0
    auts_count = 0
    S = SetSized()
    
    genstack = GenStack(model.substructures(size),ncr(len(model), size),S)
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
                    genstack.add(current.substructures(size),ncr(len(current), size))
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
    for size in S.sizes():
        print("    %s-diversity = %s"%(size,S.len(size)))
    print("  #Auts = %s" % auts_count)
    print("  #Isos = %s" % isos_count)
    print("  %s calls to Minion" % MinionSol.count)
    print("  Minion total time = %s secs" % childrens_time())
    print("")
    latex_tree = ("[.\\{%s\\}\n" % ",".join(str(i) for i in sorted(model.universe))) + latex_tree
    latex_tree +="]]\n"
    
    ftarget = open("tree.tex","w")
    base = open("base1.tex","r")
    ftarget.write(base.read())
    base.close()
    ftarget.write(latex_tree)
    base = open("base2.tex","r")
    ftarget.write(base.read())
    base.close()
    ftarget.close()

if __name__ == "__main__":
    main()
