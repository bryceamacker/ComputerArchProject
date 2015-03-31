#!/usr/local/bin/python

from myhdl import *
from memoryDictionaries import *
import os

# Read in file as a dictionary
# 0 : 010011...
# 2 : 010110...
programMemory = {}
i = 0
with open("ProcessorMachineCode") as f:
    for line in f:
       programMemory[int(i)] = line.replace(" ", "")
       i = i + 2
clockCycles = len(programMemory)

def ClkDriver(clk):

    halfPeriod = delay(1)

    @always(halfPeriod)
    def driveClk():
        clk.next = not clk

    return driveClk


def HelloWorld(clk):

    @always(clk.posedge)
    def sayHello():
        print "%s Hello World!" % now()

    return sayHello

def high(clk):
	i = 0
	@always(clk.posedge)
	def sayHigh():
		print("High")

	return sayHigh

def low(clk):
	@always(clk.negedge)
	def sayLow():
		print("Low")

	return sayLow

def inc(count, enable, clk):
    """ Incrementer with enable.

    count -- output
    enable -- control input, increment when 1
    clk -- clock input

    """

    # This basically means this function will run everytime there is a
    # rising clock edge from the clk signal
    @always(clk.posedge)
    def incLogic():
        # The enable signal is currently tied high, so this will always count
        if enable:
            # count is not a regular variable, it is a Signal. A regular
            # python variable would only exist in this functions scope each
            # clock cycle, and then be reset.
            next_op = (count[:12] + 1)
            func = (count[4:] + 1)
            if func <= 5:
                count.next[4:] = func
            elif next_op <= 15:
                count.next[:12] = next_op

    return incLogic

def programCounter(instruction, PC, clk):
    """ Incrementer with enable.

    count -- output
    enable -- control input, increment when 1
    clk -- clock input

    """

    # This basically means this function will run everytime there is a
    # rising clock edge from the clk signal
    @always(clk.posedge)
    def incLogic():
            # lines = fo.readline()
            # no_line = lines.replace(" ", "")
            # print("Lines: " + lines)
            # print("No Lines: " + no_line)
            try:
                line = programMemory[int(PC)]
                PC.next = PC + 2
                instruction.next = int(line.replace(" ", ""), 2)
            except KeyError:
                print("")
    return incLogic

def instructionMemory(instruction, clk):
    """ Incrementer with enable.

    count -- output
    clk -- clock input

    """

    # This basically means this function will run everytime there is a
    # rising clock edge from the clk signal
    @always(clk.posedge)
    def instrctionLogic():
            print("Instruction: %s " % (bin(instruction, 16)))
            opcode = instruction[:12]
            print("Opcode: %s" % (bin(opcode, 4)))
            if opcode == r_type:
                # print("Func: %s" % (bin(func, 3)))

                func = bin(instruction[3:0], 3)
                rd = bin(instruction[6:3], 3)
                rt = bin(instruction[9:6], 3)
                rs = bin(instruction[12:9], 3)
                print("%s %s %s %s" % (func_dict[func], registers_dict[rs], registers_dict[rt], registers_dict[rd]))

            elif opcode == jump:
                address = bin(instruction[12:], 12)
                print("%s %s" % (opcode_dict[bin(opcode, 4)], address))

            else:
                imm = instruction[6:]
                rt = instruction[9:6]
                rs = instruction[12:9]

                imm = bin(instruction[6:], 6)
                rt = bin(instruction[9:6], 3)
                rs = bin(instruction[12:9], 3)
                try:
                    print("%s %s %s %s" % (opcode_dict[bin(opcode, 4)], registers_dict[rs], registers_dict[rt], imm))
                except KeyError:
                    print("No instruction for opcode %s" % bin(opcode, 4))

            print("")

    return instrctionLogic

def testbench():
    func_Array = []
    clk = Signal(bool(0))
    count = Signal(0)
    PC = Signal(0)
    # Creates an instruction signal 4 bits wide, init to 0000b
    instruction = Signal(intbv(65535)[16:])
    enable = 1
    # Instantiate all modules and store them in func_Array
    # inc_inst = inc(instruction, enable, clk)
    PC_inst = programCounter(instruction, PC, clk)
    instMem_inst = instructionMemory(instruction, clk)
    clkdriver_inst = ClkDriver(clk)
    func_Array.append(PC_inst)
    func_Array.append(instMem_inst)
    # func_Array.append(inc_inst)
    func_Array.append(clkdriver_inst)

    return func_Array

if __name__ == '__main__':
    [ os.remove (f) for f in os.listdir(".") if f.endswith(".vcd") ]

    tb_fsm = traceSignals(testbench)
	# This will run the simulation for 50 timesteps, so we can expect 25 rising edges
    sim = Simulation(tb_fsm)
    sim.run(2 * clockCycles + 1)
