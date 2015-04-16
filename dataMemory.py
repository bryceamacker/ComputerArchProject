from myhdl import *

memory=[i for i in range(65536)]
a0 = 16
memory[a0] =     int("0101", 16)
memory[a0 + 2] = int("0110", 16)
memory[a0 + 4] = int("0011", 16)
memory[a0 + 6] = int("00F0", 16)
memory[a0 + 8] = int("00FF", 16)

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
