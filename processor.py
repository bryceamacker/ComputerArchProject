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
    jump = Signal(0)
    branch = Signal(0)
    memRead = Signal(0)
    memToReg = Signal(0)
    ALUOp = Signal(intbv(0)[4:])
    memWrite = Signal(0)
    ALUSrc = Signal(0)
    regWrite = Signal(1)

    # Program counter signals
    pc = Signal(intbv(0)[16:])
    PCAddOut = Signal(intbv(0)[16:])
    pc_write = Signal(1)

    # Register file signals ## GONNA FIND A WAY TO REMOVE THESE
    data1 = Signal(intbv(init_instruction)[16:])
    data2 = Signal(intbv(init_instruction)[16:])
    readData = Signal(intbv(init_instruction)[16:])

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
    instMem_inst = instructionMemory(clk, pc, instruction, programMemory)
    func_Array.append(instMem_inst)

    # Instruction decoder
    instructionDecode_inst = instructionDecode(instruction, opcode, rs, rt, rd, func, immediate, address)
    func_Array.append(instructionDecode_inst)

    # Mux in to write register
    mux_regDest = mux(rt, rd, RegDst, RegDstOut)
    func_Array.append(mux_regDest)

    # Register file
    register_inst = registers(clk, rs, rt, RegDstOut, memToRegOut, regWrite, data1, data2)
    func_Array.append(register_inst)

    # Mux in to ALU
    mux_ALUSrc = mux(data2, signExtendOut, ALUSrc, ALUSrcOut)
    func_Array.append(mux_ALUSrc)

    # ALU
    alu_inst = alu(ALUOp, func, data1, ALUSrcOut, ALUOut, zero)
    func_Array.append(alu_inst)

    # Data memory
    dataMemory_inst = dataMemory(clk, ALUOut, data2, readData, memRead, memWrite)
    func_Array.append(dataMemory_inst)

    # Mux out of Data Memory
    mux_memToReg = mux(ALUOut, readData, memToReg, memToRegOut)
    func_Array.append(mux_memToReg)

    # Program counter
    pc_inst = programCounter(clk, pc_write, pcJumpOut, pc)
    func_Array.append(pc_inst)

    # Sign extend
    signExtend_branch = signExtend(immediate, signExtendOut)
    func_Array.append(signExtend_branch)

    # Branch adder
    adder_branch = adder(PCAddOut, signExtendOut, PCBranchAddOut)
    func_Array.append(adder_branch)

    # And for PC
    and_branch = andGate(branch, zero, andBranchOut)
    func_Array.append(and_branch)

    # PC incrementer
    adder_PCIncrementer = adder(pc, Signal(intbv(2)), PCAddOut)
    func_Array.append(adder_PCIncrementer)

    # Mux for branch PC
    mux_branch = mux(PCAddOut, PCBranchAddOut, andBranchOut, pcMuxOut)
    func_Array.append(mux_branch)

    # Mux for jump PC
    mux_jump = mux(pcMuxOut, address, jump, pcJumpOut)
    func_Array.append(mux_jump)

    # Control module
    control_inst = control(instruction, RegDst, jump, branch, memRead, memToReg, ALUOp, memWrite, ALUSrc, regWrite)
    func_Array.append(control_inst)

    # Clock
    clkdriver_inst = ClkDriver(clk)
    func_Array.append(clkdriver_inst)

    # Output
    spaceOutput_inst = spaceOutput(clk)
    func_Array.append(spaceOutput_inst)

    return func_Array

if __name__ == '__main__':
    [ os.remove (f) for f in os.listdir(".") if f.endswith(".vcd") ]
    tb_fsm = traceSignals(testbench)
    sim = Simulation(tb_fsm)
    # sim.run(2 * clockCycles + 1)
    sim.run(44*2)
    print(registers_mem)
