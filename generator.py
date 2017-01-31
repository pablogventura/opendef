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
        

if __name__ == "__main__":
    generator(10,[(2,2)],[(2,2)])
