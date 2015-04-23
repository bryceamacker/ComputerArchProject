from myhdl import *
from memoryDictionaries import *

def IF_ID(clk,  IF_ID_write,    reset, jump,    pcIncrementedIn,    instructionIn,  stallIn,
                                                pcIncrementedOut,   instructionOut, stallOut):
    """
    clk -- input, clock line
    pcIncrementedIn -- input, pc after increment
    instructionIn -- input, raw instruction
    pcIncrementedOut -- output, pc after increment
    instructionOut -- output, raw instruction
    """

    @always(clk.posedge, reset.posedge, jump.posedge)
    def IF_IDLogic():
        if (reset == 1) or (jump == 1):
            instructionOut.next = 32768
            pass
        elif(IF_ID_write == 1):
            if stallIn.val == 0:
                print "################################################"
                print
                print
                print "################################################"

                pcIncrementedOut.next = pcIncrementedIn
                instructionOut.next = instructionIn
                stallOut.next = stallIn
                IF_ID_write.next = 1

                opcode = instructionIn[:12]
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

def ID_EX(clk,  reset, jump,     instructionIn, pcIncrementedIn,    regData1In,     regData2In,     rsIn,   rtIn,   rdIn,   immediateIn,    RegWriteIn,     BranchIn,   RegDstIn,   ALUOpIn,    ALUSrcIn,   MemToRegIn,     MemReadIn,  MemWriteIn,     JumpIn,     JumpAddressIn,  stallIn,
                            instructionOut, pcIncrementedOut,   regData1Out,    regData2Out,    rsOut,  rtOut,  rdOut,  immediateOut,   RegWriteOut,    BranchOut,  RegDstOut,  ALUOpOut,   ALUSrcOut,  MemToRegOut,    MemReadOut, MemWriteOut,    JumpOut,    JumpAddressOut, stallOut):
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

    @always(clk.posedge, reset.posedge, jump.posedge)
    def ID_EXLogic():
        if (reset == 1) or (jump == 1):
            instructionOut.next = 0
            pcIncrementedOut.next = 0
            regData1Out.next =0
            regData2Out.next = 0
            rsOut.next = 0
            rtOut.next = 0
            rdOut.next = 0
            immediateOut.next = 0
            RegWriteOut.next = 0
            BranchOut.next = 0
            RegDstOut.next = 0
            ALUOpOut.next = 0
            ALUSrcOut.next = 0
            MemToRegOut.next = 0
            MemReadOut.next = 0
            MemWriteOut.next = 0
            JumpOut.next = 0
            JumpAddressOut.next = 0
            stallOut.next = 0
        else:
            instructionOut.next = instructionIn
            pcIncrementedOut.next = pcIncrementedIn
            regData1Out.next = regData1In
            regData2Out.next = regData2In
            rsOut.next = rsIn
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

def EX_MEM(clk, reset,  instructionIn, pcIncrementedImmediateIn,   zeroIn,     ALUResultIn,    regData2In,     regDstOutIn,    RegWriteIn,     BranchIn,   MemReadIn,  MemWriteIn,     MemToRegIn,     JumpIn,     JumpAddrIn,     stallIn,
                        instructionOut, pcIncrementedImmediateOut,  zeroOut,    ALUResultOut,   regData2Out,    regDstOutOut,   RegWriteOut,    BranchOut,  MemReadOut, MemWriteOut,    MemToRegOut,    JumpOut,    JumpAddrOut,    stallOut):
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

    @always(clk.posedge, reset.posedge)
    def EX_MEMLogic():
        if (reset == 1):
            instructionOut.next = 0
            pcIncrementedImmediateOut.next = 0
            zeroOut.next = 0
            ALUResultOut.next = 0
            regData2Out.next = 0
            regDstOutOut.next = 0
            RegWriteOut.next = 0
            BranchOut.next = 0
            MemReadOut.next = 0
            MemWriteOut.next = 0
            MemToRegOut.next = 0
            JumpOut.next = 0
            JumpAddrOut.next = 0
            stallOut.next = 0
        else:
            instructionOut.next = instructionIn
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

def MEM_WB(clk, reset,  instructionIn, dataMemoryReadDataIn,   ALUResultIn,    regDstOutIn,    RegWriteIn,     MemToRegIn,     stallIn,
                        instructionOut, dataMemoryReadDataOut,  ALUResultOut,   regDstOutOut,   RegWriteOut,    MemToRegOut,    stallOut, stall):
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

    @always(clk.posedge, reset.posedge)
    def MEM_WBLogic():
        if (reset == 1):
            instructionOut.next = 0
            dataMemoryReadDataOut.next = 0
            ALUResultOut.next = 0
            regDstOutOut.next = 0
            RegWriteOut.next = 0
            MemToRegOut.next = 0
            stallOut.next = 0
        else:
            instructionOut.next = instructionIn
            dataMemoryReadDataOut.next = dataMemoryReadDataIn
            ALUResultOut.next = ALUResultIn
            regDstOutOut.next = regDstOutIn
            RegWriteOut.next = RegWriteIn
            MemToRegOut.next = MemToRegIn
            stallOut.next = stallIn
            stall.next = 0

    return MEM_WBLogic
