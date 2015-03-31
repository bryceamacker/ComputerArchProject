from myhdl import always

def programCounter(instruction, pc, clk, programMemory):
    """ Incrementer with enable.

    count -- output
    PC -- counter to increment address
    clk -- clock input

    """

    # This basically means this function will run everytime there is a 
    # rising clock edge from the clk signal   
    @always(clk.posedge)
    def incLogic():
        try:
            ins_line = programMemory[int(pc)]
            pc.next = pc + 2
            instruction.next = int(ins_line.replace(" ", ""), 2)
        except KeyError:
            print("")

    return incLogic
