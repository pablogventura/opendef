# -*- coding: utf-8 -*-
#!/usr/bin/env python   
from minion import is_isomorphic
from parser import stdin_parser

def main():
    g=stdin_parser()
    
    print(is_isomorphic(g,g))
    

if __name__ == "__main__":
    main()
