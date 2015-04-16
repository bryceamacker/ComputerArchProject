from myhdl import *

def IF_ID(clk, pcIncrementedIn, decodedInstructionIn, pcIncrementedOut, decodedInstructionOut):
    """
    """

    @always(clk.posedge)
    def IF_IDLogic():
        pcIncrementedOut.next = pcIncrementedIn
        decodedInstructionOut.next = decodedInstructionIn
        pcIncrementedOut.next = pcIncrementedIn
        decodedInstructionOut.next = decodedInstructionIn

    return IF_IDLogic

def ID_EX(clk, pcIncrementedIn, regData1In, regData2In, rtIn, rdIn, immediateIn, RegWriteIn, BranchIn, RegDstIn, ALUOpIn, ALUSrcIn, pcIncrementedOut, regData1Out, regData2Out, rtOut, rdOut, immediateOut, RegWriteOut, BranchOut, RegDstOut, ALUOpOut, ALUSrcOut):
    """
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

    return ID_EXLogic

def EX_MEM(clk, pcIncrementedImmediateIn, ALUResultIn, regData2In, regDstOutIn, RegWriteIn, BranchIn, MemReadIn, MemWriteIn, pcIncrementedImmediateOut, ALUResultOut, regData2Out, regDstOutOut, RegWriteOut, BranchOut, MemReadOut, MemWriteOut):
    """
    """

    @always(clk.posedge)
    def EX_MEMLogic():
        pcIncrementedOut.next = pcIncrementedIn
        ALUResultOut.next = ALUResultIn
        regData2Out.next = regData2In
        regDstOutOut.next = regDstOutIn
        RegWriteOut.next = RegWriteIn
        BranchOut.next = BranchIn
        MemReadOut.next = MemReadIn
        MemWriteOut.next = MemWriteIn

    return EX_MEMLogic

def MEM_WB(clk, dataMemoryReadDataIn, ALUResultIn, regDstOutIn, RegWriteIn, MemtoRegIn, dataMemoryReadDataOut, ALUResultOut, regDstOutOut, RegWriteOut, MemtoRegOut):
    """
    """

    @always(clk.posedge)
    def MEM_WBLogic():
        dataMemoryReadDataOut.next = dataMemoryReadDataIn
        ALUResultOut.next = ALUResultIn
        regDstOutOut.next = regDstOutIn
        RegWriteOut.next = RegWriteIn
        MemtoRegOut.next = MemtoRegIn

    return MEM_WBLogic
