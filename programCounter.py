from myhdl import always

def programCounter(clk, pc_write, pcIn, pc, staller, stall):
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
        if pc_write and (staller.val == 0):
            pc.next = pcIn
            staller.next = 3
            stall.next = 0
        else:
            staller.next = staller - 1
            stall.next = 1

    return incLogic
