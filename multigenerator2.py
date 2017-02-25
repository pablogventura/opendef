import os

path = "positives/"
for arity in [2,3,4]:
    for density in [0.1,0.3,0.5]:
        for size in [10000,20000,30000,40000]:
        for i in range(50):
            s = "python generator2.py"
            s += " -s%s -a%s -d%s > %s" % (size,arity,density,path)
            s += "p%s_%s_%s_%s.model" % (i,universe,arity,density)
            print("Generating %sp%s_%s_%s_%s.model" % (path,i,universe,arity,density))
            os.system(s)
print("GENERATION FINISHED")
