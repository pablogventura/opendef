import os

path = "positives/"
timeout = "30m"


import glob, os
for f in glob.glob(path + "*.model"):
    print ("Processing %s" % f)
    out = f[:-6]+".result"
    os.system("{ /usr/bin/time -v timeout --signal=SIGINT %s python main.py < %s;} >%s 2>>%s" % (timeout,f,out,out))

print("PROCESSING FINISHED")
