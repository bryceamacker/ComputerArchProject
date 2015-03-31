from myhdl import always

def programCounter(pc_write, clk, pc):
    """ Incrementer with enable.
    pc_write -- input (enable pc += 2)
    pc -- output instruction address
    clk -- clock input

    """

    # This basically means this function will run everytime there is a 
    # rising clock edge from the clk signal   
    @always(clk.posedge)
    def incLogic():
        try:
            if pc_write:
                pc.next = pc + 2
        except KeyError:
            print("")

    return incLogic
