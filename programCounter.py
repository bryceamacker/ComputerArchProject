from myhdl import always

def programCounter(clk, pcIn, pc, pcWrite, stall, reset):
    """ Incrementer with enable.
    clk         -- input, clock line
    pc_write    -- input, whether or not to take the input
    pcIn        -- input, new address value
    pc          -- output, instruction address
    staller     -- input, staller signal
    """

    # This basically means this function will run everytime there is a
    # rising clock edge from the clk signal
    @always(clk.posedge)
    def incLogic():
        if (stall.val == 0) and (pcWrite == 1):
            pc.next = pcIn
            reset.next = 0

    return incLogic
