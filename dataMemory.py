from myhdl import *

memory=[i for i in range(65535)]

def dataMemory(clk, address, writeData, readData, memRead, memWrite):
    """
    clk         -- input, clk line
    address     -- input, address for memory operation
    writeData   -- input, data for write
    readData    -- output, out data for read
    memRead     -- input, whether or not to read
    memWrite    -- input, whether or not to write
    """

    @always(clk.posedge)
    def dataMemoryLogic():
        if(memRead == 1):
            readData = memory[address]
        elif(memWrite == 1):
            memory[address] = writeData

    return dataMemoryLogic
