import os

path = "positives12/"
timeout = "30m"


running = []
waiting = []

for p in running:
    if p.poll() is not None:
        running.remove(p)
        running.append(In [119]: p=sp.Popen(["pi","9999"],stdout=sp.PIPE)
        

import glob, os
for f in glob.glob(path + "*.model"):
    print ("Processing %s" % f)
    out = f[:-6]+".result"
    if not os.path.isfile(out) :
        os.system("{ /usr/bin/time -v timeout --signal=SIGINT %s python main.py < %s;} >%s 2>>%s" % (timeout,f,out,out))
    else:
        print ("File %s already exists" % out)

print("PROCESSING FINISHED")
