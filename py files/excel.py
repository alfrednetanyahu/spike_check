import os.path
import os
import sys
import xlrd

pathname = os.path.dirname(sys.argv[0])

#default pin info file is in same directory as original file
file_name=pathname+"/pin_info.txt"

#if simplified position file already existed, then remove it
if os.path.isfile(file_name)==True:
    os.remove(file_name)

print str(sys.argv[1])
print str(sys.argv[2])

workbook=xlrd.open_workbook(str(sys.argv[1]))
sh=workbook.sheet_by_name(str(sys.argv[2]))
print sh.nrows
print sh.ncols
n=4
i=3

myfile=open(file_name,"w")
while n<sh.nrows-1:
    data =str(sh.cell_value(n,2))+" "+str(sh.cell_value(n,3))+" "+str(sh.cell_value(n,4))
    print  data,
    myfile.write(data+" ")
    print
    myfile.write("\n")
    n=n+1
myfile.close()

with open(file_name) as f:
    for i, l in enumerate(f):
        pass
print i+1
