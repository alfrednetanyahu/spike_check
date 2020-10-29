from pymodbus.client.sync import ModbusTcpClient as ModbusClient
import sys
import os
import time

pathname = os.path.dirname(sys.argv[0])
print pathname

re_dir="DIR"
scope_mod="MODEL"
scope_cnt="CONNECTION"
scope_ip="IP"
scope_port="PORT"
scope_channel="CHANNEL"

x=0
y=0
x1=0
x2=0
x3=0
y1=0
y2=0

process=True

#a=open(pathname+'/offset.txt',"r")
a=open('offset.txt',"r")
offs=a.readlines()
offset=offs[0].split()
print offset[0],offset[1],offset[2]

# open position file to read
#f=open(pathname+'/position.txt',"r")
f=open(pos_file,"r")
line_pos=f.readlines()
position_lines=len(line_pos)
print position_lines
f.close()

g=open(pin_file,"r")
line_pin=g.readlines()
pin_lines=len(line_pin)
print len(line_pin)
g.close()

i=0

client=ModbusClient('10.0.2.10', port=5020)
client.connect()

# change status to moving mode
rq=client.write_registers(0,[2],unit=1)
rr=client.read_holding_registers(0,0,unit=1)
#print rr.registers[0]

# send Z-travel to controller
rq=client.write_registers(7,[int(offset[2])],unit=1)
rr=client.read_holding_registers(7,1,unit=1)
print rr.registers[0]
client.close()

# go through the data file
print "Start \n"
while process=True:
    
    # initiate client
    client=ModbusClient('10.0.2.10', port=5020)
    client.connect()
        
    # read coil 0 to check if controller is requesting data
    rr_0=client.read_coils(0,1,unit=1)
    print rr_0.bits[0], "requesting data"

    # read coil 1 to check if controller has finished movement
    rr_1=client.read_coils(1,1,unit=1)
    print rr_1.bits[0], "movement finished"

    # if controller is requesting data
    if rr_0.bits[0]==True:
        print "Sending data"
        
        # go to line and seperate numbers
        ll=line[i]
        ll_split=ll.split()
        x=(int(offset[0]))-int(100*float(ll_split[1]))
        y=(int(offset[1]))-int(100*float(ll_split[2]))
        print ll_split[0], ll_split[1],ll_split[2]
        print x,y, "POSITON SENT"
        if x>32767:
            if x>65534:
                x1=32767
                x2=32767
                x3=x-x1-x2
            else:
                x1=32767
                x2=x-x1
                x3=0
        elif x<32767:
            x1=x
            x2=0
            x3=0
        if y>32767:
            y1=32767
            y2=x-32767
        elif y<32767:
            y1=y
            y2=0
        
        # put the position in a list
        re=[len(line)]
        re.append(x1)
        re.append(x2)
        re.append(x3)
        re.append(y1)
        re.append(y2)
        
        # client send position to server
        rq=client.write_registers(1,re,unit=1)
        rr=client.read_holding_registers(1,8,unit=1)
        print rr.registers[0],rr.registers[1],rr.registers[2],rr.registers[3],rr.registers[4],rr.registers[5]
        
        # client changes status to controller not requesting data
        rq=client.write_coil(0,False,unit=1)
        rr=client.read_coils(0,1,unit=1)
        print rr.bits[0]
        
        # close client
        client.close()
        print "Close \n"
           
    # if controller has finished movement
    elif rr_1.bits[0]==True:
        print "Spike Check tool"

#        var=raw_input("Enter something ")
#        print var
        
#        if var=="0":
            # change status to not moving
        time.sleep(2)
        rq=client.write_coil(1,False,unit=1)
        rr=client.read_coils(1,1,unit=1)
        print rr.bits[0]
        # increment line number
        i=i+1
        print i
        print "done \n"
    
    # if controller is  moving
    else:
        # close client
        client.close()
        print i
        print "next \n"
