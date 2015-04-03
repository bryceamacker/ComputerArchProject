from myhdl import *
from programCounter import *
from instructionMemory import *
from registers import *
from control import *
import os
from mipsCompiler import *

pa = compile('ProcessorAssembly')
print(pa)

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
    ALUOp = Signal(intbv(0)[3:])
    memWrite = Signal(0)
    ALUSrc = Signal(0)
    ALUCommand = Signal(0)
    opcode = Signal(intbv(init_instruction)[3:])


    count = Signal(0)
    pc = Signal(0)
    pc_write = 1

    # Register lines 
    rd = Signal(intbv(init_instruction)[3:])
    rt = Signal(intbv(init_instruction)[3:])
    rs = Signal(intbv(init_instruction)[3:])
    wd = Signal(intbv(init_instruction)[3:])
    regWrite = Signal(1)
    data1 = Signal(intbv(init_instruction)[16:])
    data2 = Signal(intbv(init_instruction)[16:])

    # Creates an instruction signal 16 bits wide, init to 0xFFFF
    instruction = Signal(intbv(init_instruction)[16:])

    # Instantiate all modules and store them in func_Array
    pc_inst = programCounter(pc_write, clk, pc)
    instMem_inst = instructionMemory(pc, clk, instruction, rd, rt, rs, programMemory, opcode)
    register_inst = registers(rd, rt, rs, wd, regWrite, clk, data1, data2)
    control_inst = control(instruction, clk, RegDst, jump, branch, memRead, memToReg, ALUOp, memWrite, ALUSrc, regWrite)
    aluControl_inst = aluControl(instruction, ALUOp, ALUCommand)
    clkdriver_inst = ClkDriver(clk)
    spaceOutput_inst = spaceOutput(clk)
    func_Array.append(pc_inst)
    func_Array.append(instMem_inst)
    func_Array.append(register_inst)
    func_Array.append(control_inst)
    func_Array.append(aluControl_inst)
    func_Array.append(clkdriver_inst)
    func_Array.append(spaceOutput_inst)
    return func_Array

if __name__ == '__main__':
    [ os.remove (f) for f in os.listdir(".") if f.endswith(".vcd") ]
    tb_fsm = traceSignals(testbench)
    sim = Simulation(tb_fsm)
    sim.run(2 * clockCycles + 1)
    print(registers_mem)