import os.path
import os
import sys
import xlrd

pathname = os.path.dirname(sys.argv[0])

#default excel sheet file is in same directory as original file
file_name=pathname+"/sheet.txt"

#if simplified position file already existed, then remove it
if os.path.isfile(file_name)==True:
    os.remove(file_name)

workbook=xlrd.open_workbook(str(sys.argv[1]))

sheet_name = workbook.sheet_names()
print sheet_name

myfile=open(file_name,"w")
myfile.write(str(sheet_name))
myfile.close()

