import os

path = "positives12/"
timeout = "30m"


import glob, os
for f in glob.glob(path + "*.model"):
    print ("Processing %s" % f)
    out = f[:-6]+".result"
    if not os.path.isfile(out) :
        os.system("{ /usr/bin/time -v timeout --signal=SIGINT %s python main.py < %s;} >%s 2>>%s" % (timeout,f,out,out))
    else:
        print ("File %s already exists" % out)

print("PROCESSING FINISHED")
