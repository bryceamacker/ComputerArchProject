from myhdl import *

# Two input muxes
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

# Three input muxes
def mux3(in1, in2, in3, control, out):
    """
    in1         -- input, input 0
    in2         -- input, input 1
    in3         -- input, input 2
    control     -- input, control ine
    out         -- output, output
    """

    @always_comb
    def muxLogic():
        if (control == 0):
            out.next = in1
        elif (control == 1):
            out.next = in2
        elif (control == 2):
            out.next = in3

    return muxLogic

# Two input adder
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

# Two input and
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
