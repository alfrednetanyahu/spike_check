import os
import sys

pathname = os.path.dirname(sys.argv[0])

#default fiducial file is in same directory as original file
fid_file=pathname+"/fiducial.txt"

#if fiducial file already existed, then remove it
if os.path.isfile(fid_file)==True:
    os.remove(fid_file)

#get fiducial points
myfile=open(str(sys.argv[1]))
for line in myfile:
    ll=line.split()
    if ll[0].find("FD")!=-1:
        with open(fid_file,'a') as g:
            g.write(repr(str(ll[0]))+" "+repr(float(ll[1]))+" "+repr(float(ll[2]))+"\n")
    else:
        continue
myfile.close()

