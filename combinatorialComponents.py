from myhdl import *

def mux(in1, in2, control, out):
    """
    in1         -- input, input 0
    in2         -- input, input 1
    control     -- input, control ine
    out         -- output, output
    """

    @always_comb
    def muxLogic():
        if (control == 0):
            out.next = in1
        else:
            out.next = in2

    return muxLogic

def adder(in1, in2, out):
    """
    in1 -- input, input 1
    in2 -- input, input 2
    out -- output, output
    """

    @always_comb
    def adderLogic():
        out.next = in1 + in2

    return adderLogic

def andGate(in1, in2, out):
    """
    in1 -- input, input 1
    in2 -- input, input 2
    out -- output, output
    """

    @always_comb
    def andGateLogic():
        out.next = in1 & in2

    return andGateLogic

def shiftLeft(in1, shamt, out):
    """
    in1     -- input, input
    shamt   -- input, shift amount
    out     -- output, output
    """

    @always_comb
    def shiftLeftLogic():
        out.next = in1 << shamt

    return shiftLeftLogic

def signExtend(clk, in1, out):
    """
    in1 -- input, input
    out -- output, output
    """

    @always(clk.posedge)
    def signExtendLogic():
        out.next = in1

    return signExtendLogic
