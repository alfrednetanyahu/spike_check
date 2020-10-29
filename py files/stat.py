import sys
from pymodbus.client.sync import ModbusTcpClient as ModbusClient

print "\n",sys.argv[1]

client=ModbusClient('10.0.2.10', port=5020)
client.connect()

if sys.argv[1]=="Pause":
    print "Pause"
    rq=client.write_registers(0,[3],unit=1)
    rr=client.read_holding_registers(0,1,unit=1)
    print rr.registers[0]
    
    client.close()
elif sys.argv[1]=="Resume":
    print "Resume"
    rq=client.write_registers(0,[4],unit=1)
    rr=client.read_holding_registers(0,1,unit=1)
    print rr.registers[0]
    
    client.close()
elif sys.argv[1]=="Stop":
    print "Stop"
    rq=client.write_registers(0,[5,0,0,0,0,0,0],unit=1)
    rr=client.read_holding_registers(0,8,unit=1)
    print rr.registers[0]
    
    client.close()