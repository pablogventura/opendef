import os

universe = 30
path = "positives/"



import glob, os
for f in glob.glob(path + "p6_30_2_0.1.model"):
    print ("Processing %s" % f)
    out = f[:-6]+".result"
    os.system("{ /usr/bin/time -v python main.py < %s;} >%s"% (f,out))# 2>>%s" % (f,out,out))

print("PROCESSING FINISHED")
