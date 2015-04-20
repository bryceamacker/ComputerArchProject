from myhdl import *
from memoryDictionaries import *

def IF_ID(clk,  pcIncrementedIn,    instructionIn,  stallIn,
                pcIncrementedOut,   instructionOut, stallOut):
    """
    clk -- input, clock line
    pcIncrementedIn -- input, pc after increment
    instructionIn -- input, raw instruction
    pcIncrementedOut -- output, pc after increment
    instructionOut -- output, raw instruction
    """

    @always(clk.posedge)
    def IF_IDLogic():
        pcIncrementedOut.next = pcIncrementedIn
        instructionOut.next = instructionIn
        stallOut.next = stallIn

        if not stallIn:
            print "################################################"
            print
            print
            print "################################################"

            opcode = instructionIn[:12]
            # print("Opcode: %s" % (bin(opcode, 4)))
            if opcode == r_type:
                func = bin(instructionIn[3:0], 3)
                rd = bin(instructionIn[6:3], 3)
                rt = bin(instructionIn[9:6], 3)
                rs = bin(instructionIn[12:9], 3)
                print("%s %s %s %s" % (func_dict[func], registers_dict[rd], registers_dict[rs], registers_dict[rt]))

            elif opcode == jump:
                address = bin(instructionIn[12:], 12)
                print("%s %s" % (opcode_dict[bin(opcode, 4)], address))

            else:
                imm = bin(instructionIn[6:], 6)
                rt = bin(instructionIn[9:6], 3)
                rs = bin(instructionIn[12:9], 3)
                print("%s %s %s %s" % (opcode_dict[bin(opcode, 4)], registers_dict[rt], registers_dict[rs], imm))

    return IF_IDLogic

def ID_EX(clk,  pcIncrementedIn,    regData1In,     regData2In,     rtIn,   rdIn,   immediateIn,    RegWriteIn,     BranchIn,   RegDstIn,   ALUOpIn,    ALUSrcIn,   MemToRegIn,     MemReadIn,  MemWriteIn,     JumpIn,     JumpAddressIn,  stallIn,
                pcIncrementedOut,   regData1Out,    regData2Out,    rtOut,  rdOut,  immediateOut,   RegWriteOut,    BranchOut,  RegDstOut,  ALUOpOut,   ALUSrcOut,  MemToRegOut,    MemReadOut, MemWriteOut,    JumpOut,    JumpAddressOut, stallOut):
    """
    clk -- input, clock line
    pcIncrementedIn -- input, pc after increment
    regData1In -- input, data from reg1
    regData2In -- input, data from reg2
    rtIn -- input, rt from instruction
    rdIn -- input, rd from instruction
    immediateIn -- input, immediate from instruction
    RegWriteIn -- input, control line
    Branch -- input, control line
    RegDstIn -- input, control line
    ALUOpIn -- input, operation for ALU
    ALUSrcIn -- input, source for ALU in 2
    pcIncrementedOut -- output, pc after increment
    regData1Out -- output, data from reg1
    regData2Out -- output, data from reg2
    rtOut -- output, rt from instruction
    rdOut -- output, rd from instruction
    immediateOut -- output, immediate from instruction
    RegWriteOut -- output, control line
    BranchOut -- output, control line
    RegDstOut -- output, control line
    ALUOpOut -- output, operation for ALU
    ALUSrcOut -- output, source for ALU in 2
    """

    @always(clk.posedge)
    def ID_EXLogic():
        pcIncrementedOut.next = pcIncrementedIn
        regData1Out.next =regData1In
        regData2Out.next = regData2In
        rtOut.next = rtIn
        rdOut.next = rdIn
        immediateOut.next = immediateIn
        RegWriteOut.next = RegWriteIn
        BranchOut.next = BranchIn
        RegDstOut.next = RegDstIn
        ALUOpOut.next = ALUOpIn
        ALUSrcOut.next = ALUSrcIn
        MemToRegOut.next = MemToRegIn
        MemReadOut.next = MemReadIn
        MemWriteOut.next = MemWriteIn
        JumpOut.next = JumpIn
        JumpAddressOut.next = JumpAddressIn
        stallOut.next = stallIn

    return ID_EXLogic

def EX_MEM(clk, pcIncrementedImmediateIn,   zeroIn,     ALUResultIn,    regData2In,     regDstOutIn,    RegWriteIn,     BranchIn,   MemReadIn,  MemWriteIn,     MemToRegIn,     JumpIn,     JumpAddrIn,     stallIn,
                pcIncrementedImmediateOut,  zeroOut,    ALUResultOut,   regData2Out,    regDstOutOut,   RegWriteOut,    BranchOut,  MemReadOut, MemWriteOut,    MemToRegOut,    JumpOut,    JumpAddrOut,    stallOut):
    """
    clk -- input, clock input
    pcIncrementedIn -- input, pc incremented and added with immediate
    zeroIn -- input, zero line from ALU
    ALUResultIn -- input, result from ALU
    regData2In -- input, data from reg 2
    regDstOutIn -- input, control line
    RegWriteIn -- input, control line
    Branch -- input, control line
    MemReadIn -- input, control line
    MemWriteIn -- input, control line
    pcIncrementedOut -- output, pc incremented and added with immediate
    zeroOut -- output, zero line from ALU
    ALUResultOut -- output, result from ALU
    regData2Out -- output, data from reg 2
    regDstOutOut -- output, control line
    RegWriteOut -- output, control line
    BranchOut -- output, control line
    MemReadOut -- output, control line
    MemWriteOut -- output, control line
    """

    @always(clk.posedge)
    def EX_MEMLogic():
        pcIncrementedImmediateOut.next = pcIncrementedImmediateIn
        zeroOut.next = zeroIn
        ALUResultOut.next = ALUResultIn
        regData2Out.next = regData2In
        regDstOutOut.next = regDstOutIn
        RegWriteOut.next = RegWriteIn
        BranchOut.next = BranchIn
        MemReadOut.next = MemReadIn
        MemWriteOut.next = MemWriteIn
        MemToRegOut.next = MemToRegIn
        JumpOut.next = JumpIn
        JumpAddrOut.next = JumpAddrIn
        stallOut.next = stallIn

    return EX_MEMLogic

def MEM_WB(clk, dataMemoryReadDataIn,   ALUResultIn,    regDstOutIn,    RegWriteIn,     MemToRegIn,     stallIn,
                dataMemoryReadDataOut,  ALUResultOut,   regDstOutOut,   RegWriteOut,    MemToRegOut,    stallOut):
    """
    clk -- input, clock input
    dataMemoryReadDataIn -- input, data from memory read
    ALUResultIn -- input, result from ALU
    regDstOutIn -- input, control line
    RegWriteIn -- input, control line
    MemtoRegIn -- input, control line
    dataMemoryReadDataOut -- output, data from memory read
    ALUResultOut -- output, result from ALU
    regDstOutOut -- output, control line
    RegWriteOut -- output, control line
    MemtoRegOut -- output, control line
    """

    @always(clk.posedge)
    def MEM_WBLogic():
        dataMemoryReadDataOut.next = dataMemoryReadDataIn
        ALUResultOut.next = ALUResultIn
        regDstOutOut.next = regDstOutIn
        RegWriteOut.next = RegWriteIn
        MemToRegOut.next = MemToRegIn
        stallOut.next = stallIn

        # if not stallIn:
            # print "################################################"
            # print

    return MEM_WBLogic
