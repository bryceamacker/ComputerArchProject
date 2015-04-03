from myhdl import *
from memoryDictionaries import *

def control(instruction, clk, RegDst, jumpSig, branch, memRead, memToReg, ALUOp, memWrite, ALUSrc, regWrite):
    """ 
    opcode -- input 
    clk -- input
    RegDst    -- output
    jumpSig      -- output
    branch    -- output
    memRead   -- output
    memToReg  -- output
    ALUOp     -- output
    memWrite  -- output
    ALUSrc    -- output
    regWrite  -- output
    """

    @always_comb
    def controlLogic():   
        opcode = instruction[:12]  
        if opcode == r_type:
            ALUOp.next = 2
            ALUSrc.next = 0
            branch.next = 0
            memRead.next = 0
            memWrite.next = 0
            memToReg.next = 0
            RegDst.next = 1
            regWrite.next = 1
            jumpSig.next = 0

        if opcode == addi:
            pass
        if opcode == subi:
            pass
        if opcode == andi:
            pass
        if opcode == ori:
            pass
        if opcode == lw:
            ALUOp.next = 0
            ALUSrc.next = 1
            branch.next = 0
            memRead.next = 1
            memWrite.next = 0
            memToReg.next = 1
            RegDst.next = 0
            regWrite.next = 1
            jumpSig.next = 0

        if opcode == sw:
            ALUOp.next = 0
            ALUSrc.next = 1
            branch.next = 0
            memRead.next = 0
            memWrite.next = 1
            memToReg.next = 0
            RegDst.next = 0
            regWrite.next = 0
            jumpSig.next = 0

        if opcode == sll:
            pass

        if opcode == srl:
            pass

        if opcode == jump:
            ALUOp.next = 0
            ALUSrc.next = 0
            branch.next = 0
            memRead.next = 0
            memWrite.next = 0
            memToReg.next = 0
            RegDst.next = 0
            regWrite.next = 0
            jumpSig.next = 1

        if opcode == beq:
            ALUOp.next = 1
            ALUSrc.next = 0
            branch.next = 1
            memRead.next = 0
            memWrite.next = 0
            memToReg.next = 0
            RegDst.next = 0
            regWrite.next = 0
            jumpSig.next = 0


    return controlLogic

def aluControl(instruction, ALUOp, ALUCommand):
    """
    instruction -- input
    ALUOp -- input
    ALUCommand -- output
    """

    @always_comb
    def aluControlLogic():
        func = instruction[2:]
        if ALUOp == 2:
            print("r_type")
            print("Func: %s" % (bin(func, 3)))

    return aluControlLogic