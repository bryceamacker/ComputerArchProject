from myhdl import *
from memoryDictionaries import *

def registers(clk, read1, read2, writeReg, writeData, writeSig, data1, data2):
    """ Stores all instructions and outputs appropriate signals after decoding them
    clk         -- clock input
    read1       -- input (read reg2)
    read2       -- input (read reg1)
    write       -- input (write reg)
    wd          -- input (write data)
    regWrite    -- input
    data1       -- output
    data2       -- output
    """

    # This basically means this function will run every time there is a
    # rising clock edge from the clk signal
    @always_comb
    def registersLogic():
        data1.next = int(registers_mem[int(read1)], 2)
        data2.next = int(registers_mem[int(read2)], 2)

        if writeSig:
            registers_mem[int(writeReg.val)] = bin(writeData, 16)
            print "New " + str(registers_dict[bin(writeReg, 3)]) + ": " +"{0:#0{1}x}".format(int(writeData), 6)

    return registersLogic

def printRegisters():
    print "Register File:"
    for register in registers_mem:
        print str(registers_dict[bin(register, 3)]) + ": " + "{0:#0{1}x}".format(int(registers_mem[register], 2), 6) #hex(int(registers_mem[register], 2))
    print

def checkRegisters():
    incorrectRegisters = []
    expectedValues = ["0x1a", "0x0", "0x1", "0x1019", "0x0", "0x0", "0x3c0", "0x3fc"]

    for regNum in range(0, 7):
        if hex(int(registers_mem[regNum], 2)) != expectedValues[regNum]:
            incorrectRegisters.append(regNum)

    if len(incorrectRegisters) == 0:
        print "Registers all good"

    else:
        for register in incorrectRegisters:
            print "Register " + registers_dict[bin(register, 3)] + " had value " + hex(int(registers_mem[register], 2)) + " expected " + expectedValues[register]
