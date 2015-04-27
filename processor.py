import os

from myhdl import *
from combinatorialComponents import *
from pipeline import *
from control import *
from forwarding import *
from hazardControl import *

from programCounter import *
from instructionMemory import *
from registers import *
from alu import *
from dataMemory import *

init_instruction = programMemory[0]
clockCount = 0
def ClkDriver(clk):
    global clockCount
    halfPeriod = delay(1)

    @always(halfPeriod)
    def driveClk():
        global clockCount, printDebug

        clk.next = not clk

        if clk.val == 0:
            clockCount += 1
            print
            print "====================================================== Clock " + str(clockCount) + " ======================================================"
            print

            try:
                print printDebug["IF_ID"]
                print
            except KeyError:
                pass
            try:
                print printDebug["ID_EX"]
                print
            except KeyError:
                pass
            try:
                print printDebug["EX_MEM"]
                print
            except KeyError:
                pass
            try:
                print printDebug["MEM_WB"]
                print
            except KeyError:
                pass

    return driveClk

def testbench():
    clk = Signal(bool(0))

    # Pipline signals
    # IF_ID
    IF_ID_pcIncremented = Signal(intbv(0)[16:])
    IF_ID_instruction = Signal(intbv(0)[16:])
    IF_ID_write = Signal(0)
    IF_ID_stall = Signal(0)
    # ID_EX
    ID_EX_instruction = Signal(intbv(0)[16:])
    ID_EX_pcIncremented = Signal(intbv(0)[16:])
    ID_EX_regData1 = Signal(intbv(0)[16:])
    ID_EX_regData2 = Signal(intbv(0)[16:])
    ID_EX_rs = Signal(intbv(0)[3:])
    ID_EX_rt = Signal(intbv(0)[3:])
    ID_EX_rd = Signal(intbv(0)[3:])
    ID_EX_immediate = Signal(intbv(0)[6:])
    ID_EX_RegWrite = Signal(0)
    ID_EX_Branch = Signal(0)
    ID_EX_RegDst = Signal(0)
    ID_EX_ALUOp = Signal(intbv(0)[4:])
    ID_EX_ALUSrc = Signal(0)
    ID_EX_MemToReg = Signal(0)
    ID_EX_MemRead = Signal(0)
    ID_EX_MemWrite = Signal(0)
    ID_EX_JUMP = Signal(0)
    ID_EX_address = Signal(intbv(0)[16:])
    ID_EX_stall = Signal(0)
    # EX_MEM
    EX_MEM_instruction = Signal(intbv(0)[16:])
    EX_MEM_pcIncrementedImmediate = Signal(intbv(0)[16:])
    EX_MEM_zero = Signal(0)
    EX_MEM_ALUOut = Signal(intbv(0)[16:])
    EX_MEM_regData2= Signal(intbv(0)[16:])
    EX_MEM_RegDstOut = Signal(intbv(0)[3:])
    EX_MEM_RegWrite = Signal(0)
    EX_MEM_Branch = Signal(0)
    EX_MEM_MemRead = Signal(0)
    EX_MEM_MemWrite = Signal(0)
    EX_MEM_MemToReg = Signal(0)
    EX_MEM_JUMP = Signal(0)
    EX_MEM_address = Signal(intbv(0)[16:])
    EX_MEM_stall = Signal(0)
    # MEM_WB
    MEM_WB_instruction = Signal(intbv(0)[16:])
    MEM_WB_dataMemoryReadData = Signal(intbv(0)[16:])
    MEM_WB_ALUOut = Signal(intbv(0)[16:])
    MEM_WB_RegDstOut = Signal(intbv(0)[3:])
    MEM_WB_RegWrite = Signal(0)
    MEM_WB_MemToReg = Signal(0)
    MEM_WB_stall = Signal(0)

    # Control lines
    RegDst = Signal(0)
    Jump = Signal(0)
    Branch = Signal(0)
    MemRead = Signal(0)
    MemToReg = Signal(0)
    ALUOp = Signal(intbv(0)[4:])
    MemWrite = Signal(0)
    ALUSrc = Signal(0)
    RegWrite = Signal(1)

    # Program counter signals
    pc = Signal(intbv(0)[16:])
    PCAddOut = Signal(intbv(0)[16:])
    pcWrite = Signal(1)
    stall = Signal(0)
    controlEnable = Signal(0)
    reset = Signal(0)

    # Register file signals
    regData1 = Signal(intbv(0)[16:])
    regData2 = Signal(intbv(0)[16:])

    # Memory out line
    memReadData = Signal(intbv(0)[16:])

    # ALU Signals
    ALUOut = Signal(intbv(0)[16:])
    zero = Signal(0)
    ALUIn1MuxControl = Signal(0)
    ALUIn2MuxControl = Signal(0)
    ALUIn1Out = Signal(intbv(0)[16:])
    ALUIn2Out = Signal(intbv(0)[16:])

    # Mux outs signals
    RegDstOut = Signal(intbv(0)[3:])
    memToRegOut = Signal(intbv(0)[16:])
    PCBranchAddOut = Signal(intbv(0)[16:])
    pcMuxOut = Signal(intbv(0)[16:])
    ALUSrcOut = Signal(intbv(0)[16:])
    pcJumpOut = Signal(intbv(0)[16:])

    # Various comb signals
    signExtendOut = Signal(intbv(0)[16:])
    andBranchOut = Signal(0)

    # Decoded instruction signals
    opcode = Signal(intbv()[4:])
    rs = Signal(intbv(0)[3:])
    rt = Signal(intbv(0)[3:])
    rd = Signal(intbv(0)[3:])
    func = Signal(intbv(0)[3:])
    immediate = Signal(intbv(0)[6:])
    address = Signal(intbv(0)[12:])

    # Creates an instruction signal 16 bits wide, init to 0xFFFF
    instruction = Signal(intbv(32768)[16:])

    ###################################### FORWARDING/HAZARD UNIT #####################################
    fu_forwardingUnit = forwarding(clk, ID_EX_rs, ID_EX_rt, EX_MEM_RegDstOut, MEM_WB_RegDstOut, EX_MEM_RegWrite, MEM_WB_RegWrite, ID_EX_ALUSrc, ALUIn1MuxControl, ALUIn2MuxControl)
    hu_hazardControlUnit = hazardControl(clk, rs, rt, ID_EX_rt, ID_EX_MemRead, pcWrite, IF_ID_write, controlEnable)
    ###################################### FORWARDING/HAZARD UNIT #####################################

    ############################################ PROCESSOR ############################################

    # Mux for branch PC
    mux_branch = mux(PCAddOut, EX_MEM_pcIncrementedImmediate, andBranchOut, pcMuxOut)

    # Mux for jump PC
    mux_jump = mux(pcMuxOut, EX_MEM_address, EX_MEM_JUMP, pcJumpOut)

    # Program counter
    seq_programCounter = programCounter(clk, pcJumpOut, pc, pcWrite, stall, Branch)

    # PC incrementer
    adder_PCIncrementer = adder(pc, Signal(intbv(2)), PCAddOut)

    # Instruction memory
    comb_instructionMemory = instructionMemory(clk, pc, instruction)

    ############################################ IF/ID ############################################
    pipeline_IF_ID = IF_ID(clk, IF_ID_write,    andBranchOut,  EX_MEM_JUMP,     PCAddOut,               instruction,        stall,
                                                                                IF_ID_pcIncremented,    IF_ID_instruction,  IF_ID_stall)
    ############################################ IF/ID ############################################

    # Instruction decoder
    comb_instructionDecode = instructionDecode(IF_ID_instruction, opcode, rs, rt, rd, func, immediate, address, stall)

    # Control module
    comb_control = control(IF_ID_instruction, RegDst, Jump, Branch, MemRead, MemToReg, ALUOp, MemWrite, ALUSrc, RegWrite, IF_ID_stall, controlEnable)

    # Register file
    seq_registerFile = registers(clk, rs, rt, MEM_WB_RegDstOut, memToRegOut, MEM_WB_RegWrite, regData1, regData2)

    ############################################ ID/EX ############################################
    pipeline_ID_EX = ID_EX(clk, andBranchOut, EX_MEM_JUMP,      IF_ID_instruction, IF_ID_pcIncremented, regData1,          regData2,       rs,         rt,         rd,         immediate,          RegWrite,       Branch,         RegDst,         ALUOp,          ALUSrc,         MemToReg,       MemRead,        MemWrite,       Jump,       address,        IF_ID_stall,
                                                                ID_EX_instruction, ID_EX_pcIncremented, ID_EX_regData1,    ID_EX_regData2, ID_EX_rs,   ID_EX_rt,   ID_EX_rd,   ID_EX_immediate,    ID_EX_RegWrite, ID_EX_Branch,   ID_EX_RegDst,   ID_EX_ALUOp,    ID_EX_ALUSrc,   ID_EX_MemToReg, ID_EX_MemRead,  ID_EX_MemWrite, ID_EX_JUMP, ID_EX_address,  ID_EX_stall)
    ############################################ ID/EX ############################################

    # Mux in to write register
    mux_regDest = mux(ID_EX_rt, ID_EX_rd, ID_EX_RegDst, RegDstOut)

    # ALU In1 mux
    mux3_ALUIn1 = mux3(ID_EX_regData1, memToRegOut, EX_MEM_ALUOut, ALUIn1MuxControl, ALUIn1Out)

    # ALU In2 mux
    mux3_ALUIn2 = mux3(ID_EX_regData2, memToRegOut, EX_MEM_ALUOut, ALUIn2MuxControl, ALUIn2Out)

    # ALU Src mux
    mux_ALUSrc = mux(ALUIn2Out, ID_EX_immediate, ID_EX_ALUSrc, ALUSrcOut)

    # ALU
    comb_ALU = alu(clk, ID_EX_ALUOp, ALUIn1Out, ALUSrcOut, ALUOut, zero)

    # Branch adder
    adder_branch = adder(ID_EX_pcIncremented, ID_EX_immediate, PCBranchAddOut)

    ############################################ EX/MEM ############################################
    pipeline_EX_MEM = EX_MEM(clk,   Signal(0),  ID_EX_instruction,  PCBranchAddOut,                 zero,           ALUOut,         ALUIn2Out,          RegDstOut,          ID_EX_RegWrite,     ID_EX_Branch,   ID_EX_MemRead,  ID_EX_MemWrite,     ID_EX_MemToReg,  ID_EX_JUMP,     ID_EX_address, ID_EX_stall,
                                                EX_MEM_instruction, EX_MEM_pcIncrementedImmediate,  EX_MEM_zero,    EX_MEM_ALUOut,  EX_MEM_regData2,    EX_MEM_RegDstOut,   EX_MEM_RegWrite,    EX_MEM_Branch,  EX_MEM_MemRead, EX_MEM_MemWrite,    EX_MEM_MemToReg, EX_MEM_JUMP,   EX_MEM_address, EX_MEM_stall)
    ############################################ EX/MEM ############################################

    # Data memory
    seq_dataMemory = dataMemory(clk, EX_MEM_ALUOut, EX_MEM_regData2, memReadData, EX_MEM_MemRead, EX_MEM_MemWrite)

    # And for PC
    and_branch = andGate(EX_MEM_Branch, EX_MEM_zero, andBranchOut)

    ############################################ MEM/WB ############################################
    pipeline_MEM_WB = MEM_WB(clk,   Signal(0),  EX_MEM_instruction, memReadData,                EX_MEM_ALUOut,  EX_MEM_RegDstOut,   EX_MEM_RegWrite,    EX_MEM_MemToReg,    ID_EX_stall,
                                                MEM_WB_instruction, MEM_WB_dataMemoryReadData,  MEM_WB_ALUOut,  MEM_WB_RegDstOut,   MEM_WB_RegWrite,    MEM_WB_MemToReg,    EX_MEM_stall, stall)
    ############################################ MEM/WB ############################################

    # Mux out of Data Memory
    mux_memToReg = mux(MEM_WB_ALUOut, MEM_WB_dataMemoryReadData, MEM_WB_MemToReg, memToRegOut)

    ############################################ PROCESSOR ############################################

    # Clock
    inst_clk = ClkDriver(clk)

    return instances()

if __name__ == '__main__':
    [ os.remove (f) for f in os.listdir(".") if f.endswith(".vcd") ]
    tb_fsm = traceSignals(testbench)
    sim = Simulation(tb_fsm)

    clocks = 0
    neededClocks = 168*2

    printRegisters()
    printDataMemory()

    while True:
        print
        print "Enter a number to run that many clock cycles."
        print "Enter 'a' to run all instructions of the program."
        print "Enter 't' to run one clock cycle at a time."
        print "Enter 'l' to run one loop at a time."
        print "Enter 'q' to quit."
        userInput = raw_input("Input: ")

        if userInput == "a":
            sim.run(neededClocks)
            break
        elif userInput == "t":
            print "Press enter to run one clock cycle and 'q' to quit"
            while userInput != "q" and clocks < neededClocks:
                userInput = raw_input()
                sim.run(2)
                clocks += 2
                printRegisters()
                printDataMemory()
                print "Enter 'q' to quit"
            break
        elif userInput == "q":
            break
        elif userInput == "l":
            loopCount = 1
            sim.run(16*2)
            printRegisters()
            printDataMemory()
            while loopCount <= 5:
                print "Hit enter to run loop " + str(loopCount)
                userInput = raw_input()
                if loopCount <= 2:
                    sim.run(24*2)
                else:
                    sim.run(20*2)
                sim.run(7*2)

                loopCount += 1
                printRegisters()
                printDataMemory()
            sim.run(9*2)
            break

        else:
            if userInput == "0":
                print "Cannot run 0 clock cycles"
            else:
                try:
                    sim.run(int(userInput)*2)
                    printRegisters()
                    printDataMemory()
                except ValueError:
                    print "Invalid choice"

    print
    checkRegisters()
    checkDataMemory()
