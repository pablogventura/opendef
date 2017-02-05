from collections import namedtuple, defaultdict
import os
from types import SimpleNamespace


path = "positives/"

data = defaultdict(lambda : defaultdict(lambda : SimpleNamespace(max_s=float("-inf"),
                                                                 min_s=float("inf"),
                                                                 average_s=0,
                                                                 max_time=float("-inf"),
                                                                 min_time=float("inf"),
                                                                 average_time=0,
                                                                 succesfull=0,
                                                                 timeouts=0)))

import glob, os
for f in glob.glob(path + "*.result"):
    print ("Processing %s" % f)
    #p10_30_2_0.2.result
    file=open(f,"r")
    s = file.readline()
    while s:
        if "Diversity=" in s:
            diversity = int(s[len("Diversity="):])
        if "\tExit status: " in s:
            exit_status = int(s[len("\tExit status: "):])
            print(exit_status)
        elif "\tUser time (seconds): " in s:
            time = float(s[len("\tUser time (seconds): "):])
        elif "\tSystem time (seconds): " in s:
            time += float(s[len("\tSystem time (seconds): "):])
        s = file.readline()
    
    file.close()
    i,universe,arity,density = f[len(path)+1:-len(".result")].split("_")
    i=int(i)
    universe=int(universe)
    arity=int(arity)
    density = float(density)
    
    #exit_status 124
    
    s=s.splitlines()
    
    
    if exit_status == 124:
        #timeout case
        #data[arity][density].max_s=None
        #data[arity][density].min_s=None
        #data[arity][density].average_s=None
        
        #data[arity][density].max_time=None
        #data[arity][density].min_time=None
        #data[arity][density].average_time=None
        
        #data[arity][density].succesfull=0
        data[arity][density].timeouts+=1
    elif exit_status == 0:
        #succesful case 
        if data[arity][density].max_s <= diversity:
            data[arity][density].max_s=diversity
        if data[arity][density].min_s >= diversity:
            data[arity][density].min_s=diversity
        data[arity][density].average_s+=diversity
        
        if data[arity][density].max_time <= time:
            data[arity][density].max_time=time
        if data[arity][density].min_time >= time:
            data[arity][density].min_time=time
        data[arity][density].average_time+=time
        
        data[arity][density].succesfull+=1
    else:
        #error
        raise ValueError
        
    
    
for arity in range(2,5):
    for density in [0.1,0.2,0.3,0.4,0.5]:
        try:
            data[arity][density].average_s/=data[arity][density].succesfull
            data[arity][density].average_time/=data[arity][density].succesfull
        except ZeroDivisionError:
            data[arity][density].average_s=None
            data[arity][density].average_time=None


print (data)
print("PROCESSING FINISHED")
