from myhdl import always

def programCounter(clk, pc_write, pcIn, pc):
    """ Incrementer with enable.
    clk         -- input, clock line
    pc_write    -- input, whether or not to take the input
    pcIn        -- input, new address value
    pc          -- output, instruction address
    """

    # This basically means this function will run everytime there is a
    # rising clock edge from the clk signal
    @always(clk.posedge)
    def incLogic():
        try:
            if pc_write:
                pc.next = pcIn
        except KeyError:
            print("PC Increment Error")

    return incLogic
