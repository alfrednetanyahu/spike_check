def ser():
    from pymodbus.server.sync import StartTcpServer
    
    from pymodbus.device import ModbusDeviceIdentification
    from pymodbus.datastore import ModbusSequentialDataBlock
    from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
    
    import logging
    logging.basicConfig()
    log=logging.getLogger()
    log.setLevel(logging.DEBUG)

    store=ModbusSlaveContext(
        di=ModbusSequentialDataBlock(0,[0]*100),
        co=ModbusSequentialDataBlock(0,[0]*100),
        hr=ModbusSequentialDataBlock(0,[0]*100),
        ir=ModbusSequentialDataBlock(0,[0]*100))
    
    identity=ModbusDeviceIdentification()
    
    context=ModbusServerContext(slaves=store, single=True)
    
    StartTcpServer(context,identity=identity, address=("10.0.2.10",5020))
    
if __name__ == '__main__':
    ser()
