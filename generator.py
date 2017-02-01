# -*- coding: utf-8 -*-
#!/usr/bin/env python

import random

def generator(cardinality,base_rels,target_rels):
    print(" ".join(str(i) for i in range(cardinality)))
    print("")
    rindex=0
    for tuples,arity in base_rels:
        r=set()
        print ("R%s %s %s" % (rindex,tuples,arity))
        while tuples != len(r):
            t=tuple((random.randint(0,cardinality-1) for i in range(arity)))
            if t not in r:
                print(" ".join(str(i) for i in t))
                r.add(t)
        print("")
    tindex=0
    for tuples,arity in target_rels:
        r=set()
        print ("T%s %s %s" % (tindex,tuples,arity))
        while tuples != len(r):
            t=tuple((random.randint(0,cardinality-1) for i in range(arity)))
            if t not in r:
                print(" ".join(str(i) for i in t))
                r.add(t)    
        print("")

def positive_generator(cardinality,rels):
    print(" ".join(str(i) for i in range(cardinality)))
    print("")
    rindex=0
    for tuples,arity in rels:
        r=set()
        srel=("%s %s %s\n" % (rindex,tuples,arity))
        while tuples != len(r):
            t=tuple((random.randint(0,cardinality-1) for i in range(arity)))
            if t not in r:
                srel+=" ".join(str(i) for i in t) + "\n"
                r.add(t)
        print("R"+srel)
        print("T"+srel)

if __name__ == "__main__":
    generator(50,[((50**3)//2,3)],[((50**3)//2,3)])
