from myhdl import *

memory=[i for i in range(65535)]

def dataMemory(clk, address, writeData, readData, memRead, memWrite):
    """
    clk -- input
    address -- input
    writeData -- input
    readData -- output
    memRead  -- input
    memWrite -- input
    """

    @always(clk.posedge)
    def dataMemoryLogic():
        if(memRead == 1):
            readData = memory[address]
        elif(memWrite == 1):
            memory[address] = writeData

    return dataMemoryLogic
