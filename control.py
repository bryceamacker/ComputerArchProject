from myhdl import *
from alu import *
from memoryDictionaries import *

def control(instruction, RegDst, jumpSig, branch, memRead, memToReg, ALUOp, memWrite, ALUSrc, regWrite):
    """
    instruction -- input, current instruction
    RegDst      -- output, mux input
    jumpSig     -- output, mux input
    branch      -- output, mux input
    memRead     -- output, read line for data memory
    memToReg    -- output, mux input
    ALUOp       -- output, ALU operation to perform
    memWrite    -- output, write line for data memory
    ALUSrc      -- output, mux input
    regWrite    -- output, write line for register file
    """

    @always_comb
    def controlLogic():
        opcode = instruction[16:12]
        if opcode == r_type:
            func = instruction[3:0]
            if (func == add):
              ALUOp.next = ALUAddOp
            elif (func == sub):
              ALUOp.next = ALUSubOp
            elif (func == logical_and):
              ALUOp.next = ALUAndOp
            elif (func == logical_or):
              ALUOp.next = ALUOrOp
            elif (func == xor):
              ALUOp.next = ALUXorOp
            elif (func == slt):
              ALUOp.next = ALUSltOp

            ALUSrc.next = 0
            branch.next = 0
            memRead.next = 0
            memWrite.next = 0
            memToReg.next = 0
            RegDst.next = 1
            regWrite.next = 1
            jumpSig.next = 0

        if opcode == addi:
            ALUOp.next = ALUAddOp
            ALUSrc.next = 1
            branch.next = 0
            memRead.next = 0
            memWrite.next = 0
            memToReg.next = 0
            RegDst.next = 0
            regWrite.next = 1
            jumpSig.next = 0

        if opcode == subi:
            ALUOp.next = ALUSubOp
            ALUSrc.next = 1
            branch.next = 0
            memRead.next = 0
            memWrite.next = 0
            memToReg.next = 0
            RegDst.next = 0
            regWrite.next = 1
            jumpSig.next = 0

        if opcode == andi:
            ALUOp.next = ALUAndOp
            ALUSrc.next = 1
            branch.next = 0
            memRead.next = 0
            memWrite.next = 0
            memToReg.next = 0
            RegDst.next = 0
            regWrite.next = 1
            jumpSig.next = 0

        if opcode == ori:
            ALUOp.next = ALUOrOp
            ALUSrc.next = 1
            branch.next = 0
            memRead.next = 0
            memWrite.next = 0
            memToReg.next = 0
            RegDst.next = 0
            regWrite.next = 1
            jumpSig.next = 0

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
            ALUOp.next = ALUSllOp
            ALUSrc.next = 1
            branch.next = 0
            memRead.next = 0
            memWrite.next = 0
            memToReg.next = 0
            RegDst.next = 0
            regWrite.next = 1
            jumpSig.next = 0

        if opcode == srl:
            ALUOp.next = ALUSlrOp
            ALUSrc.next = 1
            branch.next = 0
            memRead.next = 0
            memWrite.next = 0
            memToReg.next = 0
            RegDst.next = 0
            regWrite.next = 1
            jumpSig.next = 0

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
            ALUOp.next = ALUSubOp
            ALUSrc.next = 0
            branch.next = 1
            memRead.next = 0
            memWrite.next = 0
            memToReg.next = 0
            RegDst.next = 0
            regWrite.next = 0
            jumpSig.next = 0


    return controlLogic
