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

    @always_comb
    def registersLogic():
        data1.next = int(registers_mem[int(read1)], 2)
        data2.next = int(registers_mem[int(read2)], 2)

        if writeSig:
            registers_mem[int(writeReg.val)] = bin(writeData, 16)

            print "**************** Register Update ****************"
            print "New " + str(registers_dict[bin(writeReg, 3)]) + ": " +"{0:#0{1}x}".format(int(writeData), 6)
            print

    return registersLogic

def printRegisters():
    print "Register File:"
    for register in registers_mem:
        print str(registers_dict[bin(register, 3)]) + ": " + "{0:#0{1}X}".format(int(registers_mem[register], 2), 6) #hex(int(registers_mem[register], 2))
    print

def checkRegisters():
    expectedValues = ["0x1a", "0x0", "0x1", "0x1019", "0x0", "0x0", "0x3c0", "0x3fc"]

    print "....................Final Registers...................."
    print "Reg" + "  " + "Actual" + " " * 15 + "Expected" + " " * 15 + "Result"

    for regNum, register in enumerate(registers_mem):
        if hex(int(registers_mem[regNum], 2)) != expectedValues[regNum]:
            regResult = "X"
        else:
            regResult = u'\u2713'

        print str(registers_dict[bin(register, 3)]) + ":  " + "{0:#0{1}x}".format(int(registers_mem[register], 2), 6) + " " * 15 + "{0:#0{1}x}".format(int(expectedValues[regNum], 16), 6) + " " * 17 + regResult

    print
