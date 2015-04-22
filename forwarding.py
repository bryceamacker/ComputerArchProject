from myhdl import *
from memoryDictionaries import *

def forwarding(clk, ID_EX_rs, ID_EX_rt, EX_MEM_registerRd, MEM_WB_registerRd, EX_MEM_regWrite, MEM_WB_regWrite, ALUSrc,
                ALUIn1MuxControl, ALUIn2MuxControl):
    """
    clk                 -- input, clock line
    ID_EX_rs            -- input, rs from decode stage
    ID_EX_rt            -- input, rt from decode stage
    EX_MEM_registerRd   -- input, rd from mem stage
    MEM_WB_registerRd   -- input, rd from WB stage
    EX_MEM_regWrite     -- input, control from WB stage for RegWrite
    MEM_WB_regWrite     -- input, control from WB stage for RegWrite
    ALUIn1MuxControl    -- output, mux control line for input 1 on ALU
    ALUIn2MuxControl    -- output, mux control line for input 2 on ALU
    """

    @always_comb
    def forwardingLogic():
        if ((EX_MEM_registerRd.val == ID_EX_rs.val) and (EX_MEM_regWrite.val == 1)):
            ALUIn1MuxControl.next = 1
        elif ((MEM_WB_registerRd.val == ID_EX_rs.val) and (MEM_WB_regWrite.val == 1)):
            ALUIn1MuxControl.next = 2
        else:
            ALUIn1MuxControl.next = 0

        if ((EX_MEM_registerRd.val == ID_EX_rt.val) and (EX_MEM_regWrite.val == 1)):
            ALUIn2MuxControl.next = 1
        elif ((MEM_WB_registerRd.val == ID_EX_rt.val) and (MEM_WB_regWrite.val == 1)):
            ALUIn2MuxControl.next = 2
        else:
            ALUIn2MuxControl.next = 0

    return forwardingLogic
