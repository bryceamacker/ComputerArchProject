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
            print "Loading Mem[" + str(address) + "]: " + "{0:#0{1}x}".format(int(writeData), 6)
            try:
                readData.next = memory[address]
            except IndexError:
                pass
        elif(memWrite == 1):
            print "New Mem[" + str(address) + "]: " + "{0:#0{1}x}".format(int(writeData), 6)
            print writeData
            try:
                memory[address] = copy(writeData.val)
            except IndexError:
                pass

    return dataMemoryLogic

def printDataMemory():
    print "Data Memory:"
    print "    a0: " + "{0:#0{1}x}".format(int(memory[a0]), 6)
    print "a0 + 2: " + "{0:#0{1}x}".format(int(memory[a0 + 2]), 6)
    print "a0 + 4: " + "{0:#0{1}x}".format(int(memory[a0 + 4]), 6)
    print "a0 + 6: " + "{0:#0{1}x}".format(int(memory[a0 + 6]), 6)
    print "a0 + 8: " + "{0:#0{1}x}".format(int(memory[a0 + 8]), 6)
    print

def checkDataMemory():
    incorrectAddresses = []
    expectedValues = ["0xff00", "0xff00", "0xff", "0xff", "0xff"]

    for address in range(0, 4):
        if hex(memory[(address*2) + 16]).rstrip("L") != expectedValues[address]:
            incorrectAddresses.append(address)

    if len(incorrectAddresses) == 0:
        print "Memory all good"

    else:
        for address in incorrectAddresses:
            print "Address " + str((address*2) + 16) + " had value " + hex(memory[(address*2) + 16]) + " expected " + str(expectedValues[address])
