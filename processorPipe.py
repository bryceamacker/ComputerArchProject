from myhdl import *
from programCounter import *
from instructionMemory import *
from registers import *
from control import *
from combinatorialComponents import *
from alu import *
from dataMemory import *
from pipeline import *
import os
from mipsCompiler import *

pa = compile('ProcessorAssembly')

programMemory = {}
i = 0
for line in pa:
    programMemory[int(i)] = line
    i += 2

clockCycles = len(programMemory)
init_instruction = programMemory[0]

def ClkDriver(clk):
    halfPeriod = delay(1)

    @always(halfPeriod)
    def driveClk():
        clk.next = not clk

    return driveClk

def spaceOutput(clk):

    @always(clk.negedge)
    def spaceOutputLogic():
        # print("")
        pass
    return spaceOutputLogic

def testbench():
    clk = Signal(bool(0))

    # Pipline signals
    # IF_ID
    IF_ID_pcIncremented = Signal(intbv(0)[16:])
    IF_ID_instruction = Signal(intbv(0)[16:])
    IF_ID_stall = Signal(0)
    # ID_EX
    ID_EX_pcIncremented = Signal(intbv(0)[16:])
    ID_EX_regData1 = Signal(intbv(0)[16:])
    ID_EX_regData2 = Signal(intbv(0)[16:])
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
    # EX_MEM
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
    # MEM_WB
    MEM_WB_dataMemoryReadData = Signal(intbv(0)[16:])
    MEM_WB_ALUOut = Signal(intbv(0)[16:])
    MEM_WB_RegDstOut = Signal(intbv(0)[3:])
    MEM_WB_RegWrite = Signal(0)
    MEM_WB_MemToReg = Signal(0)

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
    pc_write = Signal(1)
    staller = Signal(3)
    stall = Signal(0)

    # Register file signals
    regData1 = Signal(intbv(0)[16:])
    regData2 = Signal(intbv(0)[16:])

    # Memory out line
    memReadData = Signal(intbv(0)[16:])

    # ALU Signals
    ALUOut = Signal(intbv(0)[16:])
    zero = Signal(0)

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


    ############################################ PROCESSOR ############################################

    # Mux for branch PC
    mux_branch = mux(PCAddOut, EX_MEM_pcIncrementedImmediate, andBranchOut, pcMuxOut)

    # Mux for jump PC
    mux_jump = mux(pcMuxOut, EX_MEM_address, EX_MEM_JUMP, pcJumpOut)

    # Program counter
    seq_programCounter = programCounter(clk, pc_write, pcJumpOut, pc, staller, stall)

    # PC incrementer
    adder_PCIncrementer = adder(pc, Signal(intbv(2)), PCAddOut)

    # Instruction memory
    seq_instructionMemory = instructionMemory(clk, pc, instruction, programMemory, staller)

    ############################################ IF/ID ############################################
    pipeline_IF_ID = IF_ID(clk, PCAddOut,               instruction,        stall,
                                IF_ID_pcIncremented,    IF_ID_instruction,  IF_ID_stall)
    ############################################ IF/ID ############################################

    # Instruction decoder
    comb_instructionDecode = instructionDecode(IF_ID_instruction, opcode, rs, rt, rd, func, immediate, address)

    # Control module
    comb_control = control(IF_ID_instruction, RegDst, Jump, Branch, MemRead, MemToReg, ALUOp, MemWrite, ALUSrc, RegWrite, IF_ID_stall)

    # Register file
    seq_registerFile = registers(clk, rs, rt, MEM_WB_RegDstOut, memToRegOut, MEM_WB_RegWrite, regData1, regData2)

    # Sign extend
    # signExtend_branch = signExtend(immediate, signExtendOut)

    ############################################ ID/EX ############################################
    pipeline_ID_EX = ID_EX(clk, IF_ID_pcIncremented, regData1,          regData2,       rt,         rd,         immediate,          RegWrite,       Branch,         RegDst,         ALUOp,          ALUSrc,         MemToReg,       MemRead,        MemWrite,       Jump,       address,
                                ID_EX_pcIncremented, ID_EX_regData1,    ID_EX_regData2, ID_EX_rt,   ID_EX_rd,   ID_EX_immediate,    ID_EX_RegWrite, ID_EX_Branch,   ID_EX_RegDst,   ID_EX_ALUOp,    ID_EX_ALUSrc,   ID_EX_MemToReg, ID_EX_MemRead,  ID_EX_MemWrite, ID_EX_JUMP, ID_EX_address)
    ############################################ ID/EX ############################################

    # Mux in to write register
    mux_regDest = mux(ID_EX_rt, ID_EX_rd, ID_EX_RegDst, RegDstOut)

    # ALU Src mux
    mux_ALUSrc = mux(ID_EX_regData2, ID_EX_immediate, ID_EX_ALUSrc, ALUSrcOut)

    # ALU
    comb_ALU = alu(clk, ID_EX_ALUOp, ID_EX_regData1, ALUSrcOut, ALUOut, zero)

    # Branch adder
    adder_branch = adder(ID_EX_pcIncremented, ID_EX_immediate, PCBranchAddOut)

    ############################################ EX/MEM ############################################
    pipeline_EX_MEM = EX_MEM(clk,   PCBranchAddOut,                 zero,           ALUOut,         ID_EX_regData2,     RegDstOut,          ID_EX_RegWrite,     ID_EX_Branch,   ID_EX_MemRead,  ID_EX_MemWrite,     ID_EX_MemToReg,  ID_EX_JUMP,     ID_EX_address,
                                    EX_MEM_pcIncrementedImmediate,  EX_MEM_zero,    EX_MEM_ALUOut,  EX_MEM_regData2,    EX_MEM_RegDstOut,   EX_MEM_RegWrite,    EX_MEM_Branch,  EX_MEM_MemRead, EX_MEM_MemWrite,    EX_MEM_MemToReg, EX_MEM_JUMP,   EX_MEM_address)
    ############################################ EX/MEM ############################################

    # Data memory
    seq_dataMemory = dataMemory(clk, EX_MEM_ALUOut, EX_MEM_regData2, memReadData, EX_MEM_MemRead, EX_MEM_MemWrite)

    # And for PC
    and_branch = andGate(EX_MEM_Branch, EX_MEM_zero, andBranchOut)

    ############################################ MEM/WB ############################################
    pipeline_MEM_WB = MEM_WB(clk,   memReadData,                EX_MEM_ALUOut,  EX_MEM_RegDstOut,   EX_MEM_RegWrite,    EX_MEM_MemToReg,
                                    MEM_WB_dataMemoryReadData,  MEM_WB_ALUOut,  MEM_WB_RegDstOut,   MEM_WB_RegWrite,    MEM_WB_MemToReg)
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
    # sim.run(2 * clockCycles + 1)
    sim.run((124*2*5*2) + 10)
    printRegisters()
    printDataMemory()
