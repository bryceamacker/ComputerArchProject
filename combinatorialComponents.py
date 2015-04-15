from myhdl import *

def mux(in1, in2, control, out):
    """
    in1 -- input
    in2 -- input
    control -- input
    out -- output
    """

    @always_comb
    def muxLogic():
        if (control == 0):
            out = in1
        else:
            out = in2

    return muxLogic

def adder(in1, in2, out):
    """
    in1 -- input
    in2 -- input
    out -- output
    """

    @always_comb
    def adderLogic():
        out = in1 + in2

    return adderLogic

def andGate(in1, in2, out):
    """
    in1 -- input
    in2 -- input
    out -- output
    """

    @always_comb
    def andGateLogic():
        out = in1 & in2

    return andGateLogic

def shiftLeft(in1, shamt, out):
    """
    in1 -- input
    shamt -- input
    out -- output
    """

    @always_comb
    def shiftLeftLogic():
        out = in1 << shamt

    return shiftLeftLogic

def signExtend(in1, out):
    """
    in1 -- input
    out -- output
    """

    @always_comb
    def signExtendLogic():
        # out = Signal(intbv(in1)[16:])
        out = out

    return signExtendLogic
