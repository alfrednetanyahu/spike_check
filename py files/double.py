import serial   #import serial library
import os
import time
import sys
from pymodbus.client.sync import ModbusTcpClient as ModbusClient
i=0

#default fiducial file is in same directory as original file
off="offset.txt"

#if fiducial file already existed, then remove it
if os.path.isfile(off)==True:
    os.remove(off)

ser=serial.Serial('COM3',9600)          # open serial port
spe=[0,0,0]
click=0

# initiate client
client=ModbusClient('10.0.2.250', port=502)
client.connect()

# calibration from joy stick
rq=client.write_registers(0,[6], unit=1)
time.sleep(0.2)

while i<7:
    try:
        data=ser.readline()   # get the bytes to read first and then read it from buffer
        print(data)
        val=data.split()
        if sys.argv[1]=="X: ":
            click=1
            spe[0]=int(val[1])
        elif sys.argv[1]=="Y:":
            click=2
            spe[1]=int(val[1])
        elif sys.argv[1]=="Z:":
            spe[2]=int(val[1])
            click=3
        elif sys.argv[1]=="Double":
             rq=client.write_registers(1,[1],unit=1)
             time.sleep(0.2)
            
        rq=client.write_registers(2,spe,unit=1)
        rq=client.write_registers(5,click,unit=1)
        time.sleep(0.2)
            
        if(ser.read=="Double "):
            # send position to server
            rq=client.write_registers(1,[1],unit=1)
            time.sleep(0.2)
            rr=client.read_holding_registers(2,8,unit=1)
            time.sleep(0.2)
            print rr.registers[0],rr.registers[1],rr.registers[2],rr.registers[3],rr.registers[4],rr.registers[5]
            x=int(rr.registers[0])+int(rr.registers[1])+int(rr.registers[2])
            y=int(rr.registers[3])+int(rr.registers[4])
            z=int(rr.registers[5])
            tex[i]=x
            tex[i+1]=y
            tex[i+2]=z
            time.sleep(0.2)
            rq=client.write_registers(0,[0], unit=1)
            time.sleep(0.2)
            
    
            #close client
            client.close()
            print "Close \n"

            i=i+3
            with open(off,'a') as g:
                for item in tex:
                    g.write("%s " % item)
    except KeyboardInterrupt:
        ser.close()
