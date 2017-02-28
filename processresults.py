from collections import namedtuple, defaultdict
import os
import glob, os
from types import SimpleNamespace


path = "positives/"

data = defaultdict(lambda : defaultdict(lambda : defaultdict(lambda : SimpleNamespace(max_s=float("-inf"),
                                                                                      min_s=float("inf"),
                                                                                      average_s=0,
                                                                                      max_time=float("-inf"),
                                                                                      min_time=float("inf"),
                                                                                      average_time=0,
                                                                                      succesfull=0,
                                                                                      timeouts=0))))

for f in glob.glob(path + "*.result"):
    print ("Processing %s" % f)
    #p10_30_2_0.2.result
    file=open(f,"r")
    timeout = False
    s = file.readline()
    while s:
        if "Diversity=" in s:
            diversity = int(s[len("Diversity="):])
        elif "KeyboardInterrupt" in s:
            timeout = True
        elif " seconds time elapsed" in s:
            time = float(s.split()[0])
        s = file.readline()
    
    file.close()
    i,size,arity,density = f[len(path)+1:-len(".result")].split("_")
    i=int(i)
    size=int(size)
    arity=int(arity)
    density = float(density)
    
    #exit_status 124
    
    s=s.splitlines()

        
    if timeout:
        #timeout case
        #data[arity][density].max_s=None
        #data[arity][density].min_s=None
        #data[arity][density].average_s=None
        
        #data[arity][density].max_time=None
        #data[arity][density].min_time=None
        #data[arity][density].average_time=None
        
        #data[arity][density].succesfull=0
        data[size][arity][density].timeouts+=1
    else:
        #succesful case 
        if data[size][arity][density].max_s <= diversity:
            data[size][arity][density].max_s=diversity
        if data[size][arity][density].min_s >= diversity:
            data[size][arity][density].min_s=diversity
        data[size][arity][density].average_s+=diversity
        
        if data[size][arity][density].max_time <= time:
            data[size][arity][density].max_time=time
        if data[size][arity][density].min_time >= time:
            data[size][arity][density].min_time=time
        data[size][arity][density].average_time+=time
        
        data[size][arity][density].succesfull+=1
        
    
for size in [10000,20000,30000,40000]:
    for arity in range(2,5):
        for density in [0.1,0.3,0.5]:
            try:
                data[size][arity][density].average_s/=data[size][arity][density].succesfull
                data[size][arity][density].average_time/=data[size][arity][density].succesfull
            except ZeroDivisionError:
                data[size][arity][density].average_s=None
                data[size][arity][density].average_time=3600


print("PROCESSING FINISHED")
print("")


import numpy as np
import matplotlib.pyplot as plt

#from mpl_toolkits.mplot3d import Axes3D
#fig = plt.figure()
#ax = fig.add_subplot(111, projection='3d')



arity=3
x=[]
y=[]
density = 0.1
for size in [10000,20000,30000,40000]:
    x.append(size)
    y.append(data[size][arity][density].average_time)

plt.plot(x, y, color="red", linewidth=1.0, linestyle="-")
x=[]
y=[]
density = 0.3
for size in [10000,20000,30000,40000]:
    x.append(size)
    y.append(data[size][arity][density].average_time)
plt.plot(x, y, color="green", linewidth=1.0, linestyle="-")
x=[]
y=[]
density = 0.5
for size in [10000,20000,30000,40000]:
    x.append(size)
    y.append(data[size][arity][density].average_time)
plt.plot(x, y, color="blue", linewidth=1.0, linestyle="-")


#plt.yscale('log')
plt.show()

