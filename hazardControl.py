from myhdl import *
from memoryDictionaries import *

def hazardControl(clk, IF_ID_rs, IF_ID_rt, ID_EX_rt, ID_EX_MemRead, pcWrite, IF_ID_write, controlEnable):

    @always_comb
    def hazardControlLogic():
        if ID_EX_MemRead == 1 and (ID_EX_rt == IF_ID_rs or ID_EX_rt == IF_ID_rt):
            pcWrite.next = 0
            IF_ID_write.next = 0
            controlEnable.next = 0
        else:
            pcWrite.next = 1
            IF_ID_write.next = 1
            controlEnable.next = 1

    return hazardControlLogic
