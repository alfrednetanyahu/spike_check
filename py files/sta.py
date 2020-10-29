import sys
from pymodbus.client.sync import ModbusTcpClient as ModbusClient

print "\n",sys.argv[1]

client=ModbusClient('10.0.2.250', port=502)
client.connect()

if sys.argv[1]=="Pause":
    print "Pause"
    rq=client.write_registers(0,[3],unit=1)
    
    client.close()
elif sys.argv[1]=="Resume":
    print "Resume"
    rq=client.write_registers(0,[4],unit=1)
    
    client.close()
elif sys.argv[1]=="Stop":
    print "Stop"
    rq=client.write_registers(0,[5],unit=1)
    
    client.close()
