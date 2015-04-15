from myhdl import *

ALUAddOp = 3
ALUSubOp = 4
ALUAndOp = 5
ALUOrOp  = 6
ALUXorOp = 7
ALUSltOp = 8
ALUSllOp = 9
ALUSlrOp = 10

def alu(instruction, ALUOp, ALUIn1, ALUIn2, ALUOut, zero):
    """
    instruction -- input
    ALUOp -- input
    ALUIn1 -- input
    ALUIn2 -- input
    ALUOut -- output
    zero -- output
    """

    @always_comb
    def aluLogic():
        func = instruction[2:]
        if ALUOp == ALUAddOp:
            ALUOutVal = ALUIn1 + ALUIn2
        # elif ALUOp == ALUSubOp:
        #     ALUOutVal = ALUIn1 - ALUIn2
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

        ALUOut.next = ALUOutVal

        if ALUOutVal == 0:
            zero.next = 1
        else:
            zero.next = 0

    return aluLogic
