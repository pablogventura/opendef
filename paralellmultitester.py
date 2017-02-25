import os
import multiprocessing
import glob, os
import subprocess as sp
path = "positives/"
timeout = "30m"

running = []
waiting = []

cores = 3

for filein in glob.glob(path + "*.model"):

    fileout = filein[:-6]+".result"
    if not os.path.isfile(fileout) :
        waiting.append((filein,["perf", "stat", "timeout", "--signal=SIGINT", timeout, "python", "main.py"],fileout))
    else:
        print ("File %s already exists" % fileout)


for i in range(cores):
    try:
        filein,call,fileout = waiting.pop()
    except IndexError:
        break
    print ("Processing %s" % filein)
    filein  = open(filein,"r")
    fileout = open(fileout, "w")
    running.append((sp.Popen(call,stdin=filein,stdout=fileout,stderr=fileout),filein,fileout))
    

while running:
    for p,fi,fo in running:
        if p.poll() is not None:
            #delete finished
            fi.close()
            fo.close()
            running.remove((p,fi,fo))
            #run new
            try:
                filein,call,fileout = waiting.pop()
                print ("Processing %s" % filein)
                filein  = open(filein,"r")
                fileout = open(fileout, "w")
                running.append((sp.Popen(call,stdin=filein,stdout=fileout,stderr=fileout),filein,fileout))
            except IndexError:
                continue
        



print("PROCESSING FINISHED")
