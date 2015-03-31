from myhdl import *
from memoryDictionaries import *

def control(opcode, clk, RegDst, jump, branch, memRead, memToReg, ALUOp, memWrite, ALUSrc, regWrite):
    """ 
    opcode -- input 
    clk -- input
    RegDst    -- output
    jump      -- output
    branch    -- output
    memRead   -- output
    memToReg  -- output
    ALUOp     -- output
    memWrite  -- output
    ALUSrc    -- output
    regWrite  -- output
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