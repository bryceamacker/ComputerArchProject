from myhdl import always

def programCounter(pc_write, clk, pc, pcIn):
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
            pc.next = pcIn
        except KeyError:
            print("PC Increment Error")

    return incLogic
