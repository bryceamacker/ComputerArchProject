from myhdl import *
from programCounter import *
from instructionMemory import *

# Read in file as a dictionary
# 0 : 010011...
# 2 : 010110...
programMemory = {}
i = 0
with open("ProcessorMachineCode") as f:
    for line in f:
        programMemory[int(i)] = line.replace(" ", "")
        i += 2
clockCycles = len(programMemory)


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
    PC = Signal(0)
    # Creates an instruction signal 16 bits wide, init to 0xFFFF
    instruction = Signal(intbv(65535)[16:])
    # Instantiate all modules and store them in func_Array
    pc_inst = programCounter(instruction, PC, clk, programMemory)
    instMem_inst = instructionMemory(instruction, clk)
    clkdriver_inst = ClkDriver(clk)
    func_Array.append(pc_inst)
    func_Array.append(instMem_inst)
    func_Array.append(clkdriver_inst)
    return func_Array

if __name__ == '__main__':
    tb_fsm = traceSignals(testbench)
    sim = Simulation(tb_fsm)
    sim.run(2 * clockCycles + 1)
