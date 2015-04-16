from myhdl import *
from programCounter import *
from instructionMemory import *
from registers import *
from control import *
from combinatorialComponents import *
from alu import *
from dataMemory import *
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
        print("")

    return spaceOutputLogic

def testbench():
    func_Array = []
    clk = Signal(bool(0))

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
    staller = Signal(0)

    # Register file signals
    regData1 = Signal(intbv(init_instruction)[16:])
    regData2 = Signal(intbv(init_instruction)[16:])

    # Memory out line
    memReadData = Signal(intbv(init_instruction)[16:])

    # ALU Signals
    ALUOut = Signal(intbv(init_instruction)[16:])
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
    opcode = Signal(intbv(init_instruction)[4:])
    rs = Signal(intbv(init_instruction)[3:])
    rt = Signal(intbv(init_instruction)[3:])
    rd = Signal(intbv(init_instruction)[3:])
    func = Signal(intbv(init_instruction)[3:])
    immediate = Signal(intbv(init_instruction)[6:])
    address = Signal(intbv(init_instruction)[12:])

    # Creates an instruction signal 16 bits wide, init to 0xFFFF
    instruction = Signal(intbv(init_instruction)[16:])

    # Instruction memory
    seq_instructionMemory = instructionMemory(clk, pc, instruction, programMemory)
    func_Array.append(seq_instructionMemory)

    # Instruction decoder
    comb_instructionDecode = instructionDecode(instruction, opcode, rs, rt, rd, func, immediate, address)
    func_Array.append(comb_instructionDecode)

    # Mux in to write register
    mux_regDest = mux(rt, rd, RegDst, RegDstOut)
    func_Array.append(mux_regDest)

    # Register file
    seq_registerFile = registers(clk, rs, rt, RegDstOut, memToRegOut, RegWrite, regData1, regData2)
    func_Array.append(seq_registerFile)

    # Mux in to ALU
    mux_ALUSrc = mux(regData2, signExtendOut, ALUSrc, ALUSrcOut)
    func_Array.append(mux_ALUSrc)

    # ALU
    comb_ALU = alu(clk, ALUOp, func, regData1, ALUSrcOut, ALUOut, zero)
    func_Array.append(comb_ALU)

    # Data memory
    seq_dataMemory = dataMemory(clk, ALUOut, regData2, memReadData, MemRead, MemWrite)
    func_Array.append(seq_dataMemory)

    # Mux out of Data Memory
    mux_memToReg = mux(ALUOut, memReadData, MemToReg, memToRegOut)
    func_Array.append(mux_memToReg)

    # Program counter
    seq_programCounter = programCounter(clk, pc_write, pcJumpOut, pc, staller)
    func_Array.append(seq_programCounter)

    # Sign extend
    signExtend_branch = signExtend(immediate, signExtendOut)
    func_Array.append(signExtend_branch)

    # Branch adder
    adder_branch = adder(PCAddOut, signExtendOut, PCBranchAddOut)
    func_Array.append(adder_branch)

    # And for PC
    and_branch = andGate(Branch, zero, andBranchOut)
    func_Array.append(and_branch)

    # PC incrementer
    adder_PCIncrementer = adder(pc, Signal(intbv(2)), PCAddOut)
    func_Array.append(adder_PCIncrementer)

    # Mux for branch PC
    mux_branch = mux(PCAddOut, PCBranchAddOut, andBranchOut, pcMuxOut)
    func_Array.append(mux_branch)

    # Mux for jump PC
    mux_jump = mux(pcMuxOut, address, Jump, pcJumpOut)
    func_Array.append(mux_jump)

    # Control module
    comb_control = control(instruction, RegDst, Jump, Branch, MemRead, MemToReg, ALUOp, MemWrite, ALUSrc, RegWrite)
    func_Array.append(comb_control)

    # Clock
    inst_clk = ClkDriver(clk)
    func_Array.append(inst_clk)

    # Output
    inst_spaceOutput = spaceOutput(clk)
    func_Array.append(inst_spaceOutput)

    return func_Array

if __name__ == '__main__':
    [ os.remove (f) for f in os.listdir(".") if f.endswith(".vcd") ]
    tb_fsm = traceSignals(testbench)
    sim = Simulation(tb_fsm)
    # sim.run(2 * clockCycles + 1)
    sim.run(124*2*5)
