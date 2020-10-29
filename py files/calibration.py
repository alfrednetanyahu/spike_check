import sys
import time
from pymodbus.client.sync import ModbusTcpClient as ModbusClient

print "\n",sys.argv[1], sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5],sys.argv[6]
print "Calibration start"

movement_sent=False

while movement_sent==False:
    print "START"
    # initiate connection
    client=ModbusClient('10.0.2.250', port=502)
    client.connect()
    
    # change status to calibration mode
    print "Calibration"
    rq=client.write_registers(0,[1],unit=1)

    # save previous values
    rr=client.read_holding_registers(2,8,unit=1)
    time.sleep(0.2)
    print rr.registers[0],rr.registers[1],rr.registers[2],rr.registers[3],rr.registers[4],rr.registers[5]
    re=[rr.registers[0],rr.registers[1],rr.registers[2],rr.registers[3],rr.registers[4],rr.registers[5]]

    # read coil 1 to check if controller has finished movement
    rr=client.read_coils(100,1,unit=1)
    print rr.bits[0], "movement finished"

    # if controller has finished movement
    if rr.bits[0]==False:

        # put X position in array
        if sys.argv[1]=="X_value":
            re[0]=int(sys.argv[2])
            re[1]=int(sys.argv[3])
            re[2]=int(sys.argv[4])

        # put Y position in array
        elif sys.argv[1]=="Y_value":
            re[3]=int(sys.argv[2])
            re[4]=int(sys.argv[3])

        # put Z position in array
        elif sys.argv[1]=="Z_value":
            re[5]=int(sys.argv[2])

        # put X -Y position into an array
        elif sys.argv[1]=="Move":
            re[0]=int(sys.argv[2])
            re[1]=int(sys.argv[3])
            re[2]=int(sys.argv[4])
            re[3]=int(sys.argv[5])
            re[4]=int(sys.argv[6])
        
        print re
        
        # send position to server
        rq=client.write_registers(2,re,unit=1)
            
        #close client
        client.close()
        print "Close \n"
        movement_sent=True
    
    #if controller is  moving
    else:
        #close client
        client.close()
