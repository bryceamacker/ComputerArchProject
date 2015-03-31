from myhdl import *
from programCounter import *
from instructionMemory import *
from registers import *
import os

# Read in file as a dictionary
# 0 : 010011...
# 2 : 010110...
programMemory = {}
i = 0
with open("ProcessorMachineCode") as f:
    for line in f:
        if line != "\n":
            programMemory[int(i)] = line.replace(" ", "")
        else:
            programMemory[int(i)] = "1111111111111111\n"
        i += 2
    programMemory[int(i)] =  "1111111111111111\n"
clockCycles = len(programMemory)
init_instruction = programMemory[0]
init_instruction = int(init_instruction.replace(" ", ""), 2)

def ClkDriver(clk):
    halfPeriod = delay(1)

    @always(halfPeriod)
    def driveClk():
        clk.next = not clk

    return driveClk

def testbench():
    func_Array = []
    clk = Signal(bool(0))
    count = Signal(0)
    pc = Signal(0)
    pc_write = 1
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
    instMem_inst = instructionMemory(pc, clk, instruction, rd, rt, rs, programMemory)
    register_inst = registers(rd, rt, rs, wd, regWrite, clk, data1, data2)
    clkdriver_inst = ClkDriver(clk)
    func_Array.append(pc_inst)
    func_Array.append(instMem_inst)
    func_Array.append(register_inst)
    func_Array.append(clkdriver_inst)
    return func_Array

if __name__ == '__main__':
    [ os.remove (f) for f in os.listdir(".") if f.endswith(".vcd") ]
    tb_fsm = traceSignals(testbench)
    sim = Simulation(tb_fsm)
    sim.run(2 * clockCycles + 1)
    print(registers_mem)