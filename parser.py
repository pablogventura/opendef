# -*- coding: utf-8 -*-
#!/usr/bin/env python

from models import RelationalModel
from relations import Relation

#new parser
from itertools import count

class ParserError(Exception):
    """
    Sintax error while parsing
    """
    def __init__(self, line, message):
        self.line = line
        self.message = message

def c_input():
    """
    Clean input
    """
    line = input()
    if "#" in line:
        line = line[:line.find("#")]
    return line.strip()


def parse_universe(line):
    # el universo puede estar hecho de strings, de tuplas,etc
    return [eval(i) for i in line.split()]

def parse_defrel(line):
    sym, ntuples, arity = line.split()
    ntuples,arity = int(ntuples),int(arity)
    return Relation(sym,arity),ntuples


def parse_tuple(line):
    return tuple(map(eval,line.split()))

def stdin_parser():
    """
    New parser
    """
    relations={}
    current_rel = None
    rel_missing_tuples= 0
    universe=None
    for linenumber in count(1):
        try:
            line = c_input()
            if line:
                if universe is None:
                    # tiene que ser el universo!
                    universe =parse_universe(line)
                elif current_rel is None:
                    # empieza una relacion
                    current_rel,rel_missing_tuples=parse_defrel(line)
                    print("%s density: %f" % (current_rel.sym, float(rel_missing_tuples)/(len(universe)**current_rel.arity)))
                else:
                    # continua una relacion
                    current_rel.add(parse_tuple(line))
                    rel_missing_tuples-=1
                    if not rel_missing_tuples:
                        relations[current_rel.sym] = current_rel
                        current_rel = None
        except EOFError:
            if universe is None:
                raise ParserError(linenumber,"Universe not defined")
            if current_rel is not None:
                raise ParserError(linenumber,"Missing tuples for relation %s" % current_rel.sym)
            return RelationalModel(universe,relations)
        except:
            raise ParserError(linenumber,"")

def stdin_parser_old():
    """
    Returns parsed Rel_Model from stdin
    """
    linenumber = 1
    relations = {}
    try:
        universe = [int(i) for i in input().split()] # first line, universe
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
            print("%s density: %f" % (sym, float(ntuples)/(len(universe)**arity)))
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
