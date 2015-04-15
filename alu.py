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
    ALUCommand -- output
    """

    @always_comb
    def aluLogic():
        func = instruction[2:]
        if ALUOp == ALUAddOp:
            ALUOut = ALUIn1 + ALUIn2
        elif ALUOp == ALUSubOp:
            ALUOut = ALUIn1 - ALUIn2
        elif ALUOp == ALUAndOp:
            ALUOut = ALUIn1 & ALUIn2
        elif ALUOp == ALUOrOp:
            ALUOut = ALUIn1 | ALUIn2
        elif ALUOp == ALUXorOp:
            ALUOut = ALUIn1 ^ ALUIn2
        elif ALUOp == ALUSltOp:
            if (ALUIn1 < ALUIn2):
                ALUOut = 1
            else:
                ALUOut = 0
        elif ALUOp == ALUSllOp:
            ALUOut = ALUIn1 << ALUIn2
        elif ALUOp == ALUSlrOp:
            ALUOut = ALUIn1 >> ALUIn2
        else:
            ALUOut = 0

        if ALUOut == 0:
            zero = 1

    return aluLogic
