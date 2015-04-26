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
            print "**************** Memory Update ****************"
            print "New Mem[" + str(address) + "]: " + "{0:#0{1}x}".format(int(writeData), 6)
            print

            memory[address] = copy(writeData.val)

    return dataMemoryLogic

def printDataMemory():
    print "Data Memory:"
    print "    a0: " + "{0:#0{1}X}".format(int(memory[a0]), 6)
    print "a0 + 2: " + "{0:#0{1}X}".format(int(memory[a0 + 2]), 6)
    print "a0 + 4: " + "{0:#0{1}X}".format(int(memory[a0 + 4]), 6)
    print "a0 + 6: " + "{0:#0{1}X}".format(int(memory[a0 + 6]), 6)
    print "a0 + 8: " + "{0:#0{1}X}".format(int(memory[a0 + 8]), 6)
    print

def checkDataMemory():
    expectedValues = ["0xff00", "0xff00", "0xff", "0xff", "0xff"]

    print "........................Final Memory......................."
    print "Address" + "  " + "Actual" + " " * 15 + "Expected" + " " * 15 + "Result"

    memResult = u'\u2713' if hex(int(memory[a0])) == expectedValues[0] else "X"
    print "    a0:  " + "{0:#0{1}x}".format(int(memory[a0]), 6) + " " * 15 + "{0:#0{1}x}".format(int(expectedValues[0], 16), 6) + " " * 17 + memResult

    memResult = u'\u2713' if hex(int(memory[a0 + 2])) == expectedValues[1] else "X"
    print "a0 + 2:  " + "{0:#0{1}x}".format(int(memory[a0 + 2]), 6) + " " * 15 + "{0:#0{1}x}".format(int(expectedValues[1], 16), 6) + " " * 17 + memResult

    memResult = u'\u2713' if hex(int(memory[a0 + 4])) == expectedValues[2] else "X"
    print "a0 + 4:  " + "{0:#0{1}x}".format(int(memory[a0 + 4]), 6) + " " * 15 + "{0:#0{1}x}".format(int(expectedValues[2], 16), 6) + " " * 17 + memResult

    memResult = u'\u2713' if hex(int(memory[a0 + 6])) == expectedValues[3] else "X"
    print "a0 + 6:  " + "{0:#0{1}x}".format(int(memory[a0 + 6]), 6) + " " * 15 + "{0:#0{1}x}".format(int(expectedValues[3], 16), 6) + " " * 17 + memResult

    memResult = u'\u2713' if hex(int(memory[a0 + 8])) == expectedValues[4] else "X"
    print "a0 + 8:  " + "{0:#0{1}x}".format(int(memory[a0 + 8]), 6) + " " * 15 + "{0:#0{1}x}".format(int(expectedValues[4], 16), 6) + " " * 17 + memResult

    print
