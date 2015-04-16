from myhdl import *
from memoryDictionaries import *

def registers(clk, read1, read2, write, wd, regWrite, data1, data2):
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
    @always(clk.posedge)
    def registersLogic():
        data1.next = int(registers_mem[int(read1)], 2)
        data2.next = int(registers_mem[int(read2)], 2)

        if regWrite:
            registers_mem[int(write.val)] = bin(wd, 16)
            # print "New " + str(write.val) + ": " + str(wd)


    return registersLogic
