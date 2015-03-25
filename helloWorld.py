from myhdl import Signal, delay, always, now, Simulation


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

def inc(count, enable, clock):
	""" Incrementer with enable.

    count -- output
    enable -- control input, increment when 1
    clock -- clock input

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
			count.next = (count + 1)
			print(count)

	return incLogic


if __name__ == '__main__':
	# This will run the simulation for 50 timesteps, so we can expect 25 rising edges
	clk = Signal(0)
	count = Signal(0)
	enable = 1	
	inc_inst = inc(count, enable, clk)
	clkdriver_inst = ClkDriver(clk)
	# hello_inst = HelloWorld(clk)
	high_inst = high(clk)
	low_inst = low(clk)
	# tock_inst = tock(clk)
	sim = Simulation(clkdriver_inst, inc_inst)
	sim.run(50)