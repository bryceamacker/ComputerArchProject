from myhdl import *


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
            if next_op <= 15:
                count.next[:12] = next_op

    return incLogic

def instructionMemory(instruction, clk):
    """ Incrementer with enable.

    count -- output
    clk -- clock input

    """
    r_type = 0
    addi = 1
    subi = 2
    andi = 3
    ori = 4
    lw = 6
    sw = 7
    sll = 8
    srl = 9
    jump = 10
    beq = 11
    # This basically means this function will run everytime there is a 
    # rising clock edge from the clk signal   
    @always(clk.posedge)
    def instrctionLogic():
            print("Instruction: %s " % (bin(instruction, 16)))
            opcode = instruction[:12]
            print("Opcode: %s" % (bin(opcode, 4)))
            if opcode == r_type:
                print("r_type")

            if opcode == addi:
                print("addi")

            if opcode == subi:
                print("subi")

            if opcode == andi:
                print("andi")

            if opcode == ori:
                print("ori")

            if opcode == lw:
                print("lw")

            if opcode == sw:
                print("sw")

            if opcode == sll:
                print("sll")

            if opcode == srl:
                print("srl")

            if opcode == jump:
                print("jump")

            if opcode == beq:
                print("beq")

    return instrctionLogic

def testbench():
    func_Array = []
    clk = Signal(bool(0))
    count = Signal(0)
    # Creates an instruction signal 4 bits wide, init to 0000b
    instruction = Signal(intbv(0)[16:])
    enable = 1  
    # Instantiate all modules and store them in func_Array
    inc_inst = inc(instruction, enable, clk)
    instMem_inst = instructionMemory(instruction, clk)
    clkdriver_inst = ClkDriver(clk)
    func_Array.append(instMem_inst)
    func_Array.append(inc_inst)
    func_Array.append(clkdriver_inst)

    return func_Array

if __name__ == '__main__':
    tb_fsm = traceSignals(testbench)
	# This will run the simulation for 50 timesteps, so we can expect 25 rising edges
    sim = Simulation(tb_fsm)
    sim.run(50)