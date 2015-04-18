from myhdl import *

ALUAddOp = 3
ALUSubOp = 4
ALUAndOp = 5
ALUOrOp  = 6
ALUXorOp = 7
ALUSltOp = 8
ALUSllOp = 9
ALUSlrOp = 10

def alu(clk, ALUOp, ALUIn1, ALUIn2, ALUOut, zero):
    """
    ALUOp   -- input, ALU operation to perform
    func    -- input, function part of the instruction, SHOULDN'T REALLY BE HERE
    ALUIn1  -- input, in 1
    ALUIn2  -- input, in2
    ALUOut  -- output, output
    zero    -- output, whether or not the out is zero
    """

    @always_comb
    def aluLogic():
        if ALUOp == ALUAddOp:
            ALUOutVal = ALUIn1 + ALUIn2
        elif ALUOp == ALUSubOp:
            ALUOutVal = ALUIn1 - ALUIn2
        elif ALUOp == ALUAndOp:
            ALUOutVal = ALUIn1 & ALUIn2
        elif ALUOp == ALUOrOp:
            ALUOutVal = ALUIn1 | ALUIn2
        elif ALUOp == ALUXorOp:
            ALUOutVal = ALUIn1 ^ ALUIn2
        elif ALUOp == ALUSltOp:
            if (ALUIn1 < ALUIn2):
                ALUOutVal = 1
            else:
                ALUOutVal = 0
        elif ALUOp == ALUSllOp:
            ALUOutVal = ALUIn1 << ALUIn2
        elif ALUOp == ALUSlrOp:
            ALUOutVal = ALUIn1 >> ALUIn2
        else:
            ALUOutVal = 0

        if ALUOutVal == 0:
            zero.next = 1
        else:
            zero.next = 0


        #### This shouldn't be here
        if ALUOutVal >= 65536:
            ALUOutVal = 65535
        elif ALUOutVal < 0:
            ALUOutVal = 1
        #### This shouldn't be here

        temp = intbv(ALUOutVal)
        ALUOut.next = temp.signed()

    return aluLogic
