from myhdl import *
from memoryDictionaries import *
from copy import *

def dataMemory(clk, address, writeData, readData, memRead, memWrite):
    """
    clk         -- input, clk line
    address     -- input, address for memory operation
    writeData   -- input, data for write
    readData    -- output, out data for read
    memRead     -- input, whether or not to read
    memWrite    -- input, whether or not to write
    """

    @always_comb
    def dataMemoryLogic():
        if(memRead == 1):
            readData.next = memory[address]
        elif(memWrite == 1):
            memory[address] = copy(writeData.val)
            print "New Mem[" + str(address) + "]: " + "{0:#0{1}x}".format(int(writeData), 6)

    return dataMemoryLogic

def printDataMemory():
    print "Data Memory:"
    print "    a0: " + "{0:#0{1}x}".format(int(memory[a0]), 6)
    print "a0 + 2: " + "{0:#0{1}x}".format(int(memory[a0 + 2]), 6)
    print "a0 + 4: " + "{0:#0{1}x}".format(int(memory[a0 + 4]), 6)
    print "a0 + 6: " + "{0:#0{1}x}".format(int(memory[a0 + 6]), 6)
    print "a0 + 8: " + "{0:#0{1}x}".format(int(memory[a0 + 8]), 6)
    print
