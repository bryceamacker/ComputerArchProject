from myhdl import *
from alu import *
from memoryDictionaries import *

def control(instruction, RegDst, Jump, Branch, MemRead, MemToReg, ALUOp, MemWrite, ALUSrc, RegWrite, stall):
    """
    instruction -- input, current instruction
    RegDst      -- output, mux input
    Jump        -- output, mux input
    Branch      -- output, mux input
    MemRead     -- output, read line for data memory
    MemToReg    -- output, mux input
    ALUOp       -- output, ALU operation to perform
    MemWrite    -- output, write line for data memory
    ALUSrc      -- output, mux input
    RegWrite    -- output, write line for register file
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
            Branch.next = 0
            MemRead.next = 0
            MemWrite.next = 0
            MemToReg.next = 0
            RegDst.next = 1
            RegWrite.next = 1
            Jump.next = 0

        if opcode == addi:
            ALUOp.next = ALUAddOp
            ALUSrc.next = 1
            Branch.next = 0
            MemRead.next = 0
            MemWrite.next = 0
            MemToReg.next = 0
            RegDst.next = 0
            RegWrite.next = 1
            Jump.next = 0

        if opcode == subi:
            ALUOp.next = ALUSubOp
            ALUSrc.next = 1
            Branch.next = 0
            MemRead.next = 0
            MemWrite.next = 0
            MemToReg.next = 0
            RegDst.next = 0
            RegWrite.next = 1
            Jump.next = 0

        if opcode == andi:
            ALUOp.next = ALUAndOp
            ALUSrc.next = 1
            Branch.next = 0
            MemRead.next = 0
            MemWrite.next = 0
            MemToReg.next = 0
            RegDst.next = 0
            RegWrite.next = 1
            Jump.next = 0

        if opcode == ori:
            ALUOp.next = ALUOrOp
            ALUSrc.next = 1
            Branch.next = 0
            MemRead.next = 0
            MemWrite.next = 0
            MemToReg.next = 0
            RegDst.next = 0
            RegWrite.next = 1
            Jump.next = 0

        if opcode == lw:
            ALUOp.next = ALUAddOp
            ALUSrc.next = 1
            Branch.next = 0
            MemRead.next = 1
            MemWrite.next = 0
            MemToReg.next = 1
            RegDst.next = 0
            RegWrite.next = 1
            Jump.next = 0

        if opcode == sw:
            ALUOp.next = ALUAddOp
            ALUSrc.next = 1
            Branch.next = 0
            MemRead.next = 0
            MemWrite.next = 1
            MemToReg.next = 0
            RegDst.next = 0
            RegWrite.next = 0
            Jump.next = 0

        if opcode == sll:
            ALUOp.next = ALUSllOp
            ALUSrc.next = 1
            Branch.next = 0
            MemRead.next = 0
            MemWrite.next = 0
            MemToReg.next = 0
            RegDst.next = 0
            RegWrite.next = 1
            Jump.next = 0

        if opcode == srl:
            ALUOp.next = ALUSlrOp
            ALUSrc.next = 1
            Branch.next = 0
            MemRead.next = 0
            MemWrite.next = 0
            MemToReg.next = 0
            RegDst.next = 0
            RegWrite.next = 1
            Jump.next = 0

        if opcode == jump:
            ALUOp.next = 0
            ALUSrc.next = 0
            Branch.next = 0
            MemRead.next = 0
            MemWrite.next = 0
            MemToReg.next = 0
            RegDst.next = 0
            RegWrite.next = 0
            Jump.next = 1

        if opcode == beq:
            ALUOp.next = ALUSubOp
            ALUSrc.next = 0
            Branch.next = 1
            MemRead.next = 0
            MemWrite.next = 0
            MemToReg.next = 0
            RegDst.next = 0
            RegWrite.next = 0
            Jump.next = 0

        if stall:
            ALUOp.next = 0
            ALUSrc.next = 0
            Branch.next = 0
            MemRead.next = 0
            MemWrite.next = 0
            MemToReg.next = 0
            RegDst.next = 0
            RegWrite.next = 0
            Jump.next = 0



    return controlLogic
