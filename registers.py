from myhdl import *
from memoryDictionaries import *

def registers(rd, rt, rs, wd, regWrite, clk, data1, data2):
    """ Stores all instructions and outputs appropriate signals after decoding them
    rd -- input (read reg2)
    rt -- input (read reg1)
    rs -- input (write reg)
    wd -- input (write data)
    clk -- clock input
    regWrite -- input
    data1 -- output
    data2 -- output
    """

    # This basically means this function will run every time there is a
    # rising clock edge from the clk signal   
    @always(clk.posedge)
    def registersLogic():        
        data1.next = int(registers_mem[int(rt)], 2)
        data2.next = int(registers_mem[int(rd)], 2)

        if regWrite:
            registers_mem[int(rs.val)] = bin(wd, 16)


    return registersLogic