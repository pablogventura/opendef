import numpy as np
from collections import namedtuple, defaultdict
import os
import glob, os
from types import SimpleNamespace
import sys

path = "data/"

data = defaultdict(lambda : defaultdict(lambda : defaultdict(lambda :defaultdict(lambda : SimpleNamespace(diversities=[],
                                                                                          times=[],
                                                                                          cancelled=0,
                                                                                          definable=0,
                                                                                          not_definable=0,
                                                                                          total=0)))))
                                                                                          
errors=[]
num_files=0
for f in glob.glob(path + "*.result"):
    num_files+=1
    print ("Processing %s" % f)

    file=open(f,"r")

    s = file.readline()
    state = None
    while s:
        s=s.strip()
        if "Diversity = " in s:
            diversity = int(s[len("Diversity = "):])
        elif "CANCELLED" in s:
            state = "C"
        elif "DEFINABLE" in s:
            if "NOT" in s:
                state = "ND"
            else:
                state = "D"
        elif " seconds time elapsed" in s:
            time = float(s.split()[0])
        s = file.readline()
    
    file.close()
        
    i,density,arity,universe,quantity = f[len(path)+1:-len(".result")].split("_")
    i=int(i)
    density=float(density)
    arity=int(arity)
    universe = int(universe)
    quantity = int(quantity[1:])

    #state
    if state == "D":
        data[density][arity][universe][quantity].definable+=1
    elif state == "ND":
        data[density][arity][universe][quantity].not_definable+=1
    elif state == "C":
        data[density][arity][universe][quantity].cancelled+=1
    else:
        errors.append(f)
        continue
        
    #counting
    data[density][arity][universe][quantity].total+=1
    
    #diversity
    data[density][arity][universe][quantity].diversities.append(diversity)
    
    #time
    data[density][arity][universe][quantity].times.append(time)

if errors:
    print("PARSE ERROR in:")
    for f in errors:
        print(f)
    sys.exit(1)

    
arity = 2
print("Arity: %s" % arity)
for quantity in range(1,4+1,1):
    print("  Quantity: %s" % quantity)
    for density in [0.1,0.2,0.3,0.4,0.5]:
        print("    Density: %s" % density)
        for universe in range(50,100+1,10):
            print("      Universe: %s" % universe)
            print("        Definables: %.2f" % (data[density][arity][universe][quantity].definable / data[density][arity][universe][quantity].definable *100))
            print("        Not definables: %.2f" % (data[density][arity][universe][quantity].not_definable / data[density][arity][universe][quantity].definable *100))
            print("        Cancelled: %.2f" % (data[density][arity][universe][quantity].cancelled / data[density][arity][universe][quantity].definable *100))
            print("        Diversity: %s" % np.median(data[density][arity][universe][quantity].diversities))
            print("        Time: %s" % np.median(data[density][arity][universe][quantity].times))
arity = 3
print("Arity: %s" % arity)
for quantity in range(1,1+1,1):
    print("  Quantity: %s" % quantity)
    for density in [0.1,0.2,0.3,0.4,0.5]:
        print("    Density: %s" % density)
        for universe in range(23,27+1,1):
            print("      Universe: %s" % universe)
            print("        Definables: %.2f" % (data[density][arity][universe][quantity].definable / data[density][arity][universe][quantity].definable *100))
            print("        Not definables: %.2f" % (data[density][arity][universe][quantity].not_definable / data[density][arity][universe][quantity].definable *100))
            print("        Cancelled: %.2f" % (data[density][arity][universe][quantity].cancelled / data[density][arity][universe][quantity].definable *100))
            print("        Diversity: %s" % np.median(data[density][arity][universe][quantity].diversities))
            print("        Time: %s" % np.median(data[density][arity][universe][quantity].times))



print("PROCESSING FINISHED of %s files" % num_files)
print("")

import sys
sys.exit(0)

import numpy as np
import matplotlib.pyplot as plt

#from mpl_toolkits.mplot3d import Axes3D
#fig = plt.figure()
#ax = fig.add_subplot(111, projection='3d')

fig, ax = plt.subplots()

c=1/len(list(range(200,450,50)))#color
color=c
arity=2
for universe in range(200,450,50):
    x=[]
    y=[]
    for size in range(5000,40000,5000):
        if data[density][arity][universe][quantity].average_time != 3600:
            x.append(size)
            y.append(data[density][arity][universe][quantity].average_time)
        
    ax.plot(x, y, color=(color,0,0), linewidth=2.0, linestyle="-",label="#Universe=%s"%universe)
    color+=c

handles, labels = ax.get_legend_handles_labels()
ax.legend(handles, labels)
legend = ax.legend(loc='lower right')
legend.get_frame().set_alpha(0.5)
ax.set_title('Positive tests, arity=%s' % arity)
ax.set_xlabel('Model Size')
ax.set_ylabel('Time (seconds)')
#plt.yscale('log')
plt.savefig("positive_tests_arity_%s_%s.pdf"%(arity,"time"))
plt.clf()

fig, ax = plt.subplots()

c=1/len(list(range(200,450,50)))#color
color=c
arity=2
for universe in range(200,450,50):
    x=[]
    y=[]
    for size in range(5000,40000,5000):
        if data[density][arity][universe][quantity].average_diversity:
            x.append(size)
            y.append(data[density][arity][universe][quantity].average_diversity)
        
    ax.plot(x, y, color=(color,0,0), linewidth=2.0, linestyle="-",label="#Universe=%s"%universe)
    color+=c

handles, labels = ax.get_legend_handles_labels()
ax.legend(handles, labels)
legend = ax.legend(loc='lower right')
legend.get_frame().set_alpha(0.5)
ax.set_title('Positive tests, arity=%s' % arity)
ax.set_xlabel('Model Size')
ax.set_ylabel('Diversity (#S)')
#plt.yscale('log')
plt.savefig("positive_tests_arity_%s_%s.pdf"%(arity,"diversity"))
plt.clf()


fig, ax = plt.subplots()

c=1/len(list(range(25,45,5)))#color
color=c
arity=3
for universe in range(25,45,5):
    x=[]
    y=[]
    for size in range(5000,40000,5000):
        if data[density][arity][universe][quantity].average_time != 3600:
            x.append(size)
            y.append(data[density][arity][universe][quantity].average_time)
        
    ax.plot(x, y, color=(color,0,0), linewidth=2.0, linestyle="-",label="#Universe=%s"%universe)
    color+=c

handles, labels = ax.get_legend_handles_labels()
ax.legend(handles, labels)
legend = ax.legend(loc='lower right')
legend.get_frame().set_alpha(0.5)
ax.set_title('Positive tests, arity=%s' % arity)
ax.set_xlabel('Model Size')
ax.set_ylabel('Time (seconds)')
plt.savefig("positive_tests_arity_%s_%s.pdf"%(arity,"time"))
plt.clf()

fig, ax = plt.subplots()

c=1/len(list(range(25,45,5)))#color
color=c
arity=3
for universe in range(25,45,5):
    x=[]
    y=[]
    for size in range(5000,40000,5000):
        if data[density][arity][universe][quantity].average_diversity:
            x.append(size)
            y.append(data[density][arity][universe][quantity].average_diversity)
        
    ax.plot(x, y, color=(color,0,0), linewidth=2.0, linestyle="-",label="#Universe=%s"%universe)
    color+=c

handles, labels = ax.get_legend_handles_labels()
ax.legend(handles, labels)
legend = ax.legend(loc='lower right')
legend.get_frame().set_alpha(0.5)
ax.set_title('Positive tests, arity=%s' % arity)
ax.set_xlabel('Model Size')
ax.set_ylabel('Diversity (#S)')
#plt.yscale('log')
plt.savefig("positive_tests_arity_%s_%s.pdf"%(arity,"diversity"))
