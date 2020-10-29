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

workbook=xlrd.open_workbook("pin_info.xlsm")
sh=workbook.sheet_by_name("Sheet1")
print sh.nrows
print sh.ncols
n=4
i=3

myfile=open(file_name,"w")

if str(sh.cell_value(4,1))!="X101":
    print "Error - file not sorted"
else:
    print "Start"
    while n<sh.nrows:
        data =str(sh.cell_value(n,2))+" "+str(sh.cell_value(n,3))+" "+str(sh.cell_value(n,4)) # should add an instance of the pin name i.e. str(sh.cell_value(n,1))
        myfile.write(data+" ")
        myfile.write("\n")
        n=n+1
    myfile.close()
