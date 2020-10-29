import os
import sys

#default simplified position file is in same directory as original file
position_file="position.txt"

#if simplified position file already existed, then remove it
if os.path.isfile(position_file)==True:
    os.remove(position_file)

#default fiducial file is in same directory as original file
fid_file="fiducial.txt"

#if fiducial file already existed, then remove it
if os.path.isfile(fid_file)==True:
    os.remove(fid_file)

#get fiducial points
myfile=open(str(sys.argv[1]))
for line in myfile:
    ll=line.split()
    if (ll[0].find("FD2")!=-1) or (ll[0].find("FD4")!=-1) or (ll[0].find("FD6")!=-1):
        with open(fid_file,'a') as g:
            g.write(repr(str(ll[0]))+" "+repr(float(ll[1]))+" "+repr(float(ll[2]))+"\n")
    else:
        continue
myfile.close()

#go through each site
i=1
for i in range(1,9):
    #open original coordinate files
    myfile=open(str(sys.argv[1]))
    
    #go through each line in original file
    for line in myfile:
        
        #split words in line
        ll=line.split()

        #if pin matches needed pin
        if ll[0].find("X")!=-1 and ll[0].find("GND")==-1:

            findva="_"+str(i)
            if ll[0].find(findva)!=-1:
                with open(position_file, 'a') as f:
                    f.write(repr(str(ll[0]))+" "+repr(float(ll[1]))+" "+repr(float(ll[2]))+"\n")
            else:
                continue
        else:
            continue

    myfile.close()
    i=i+1
