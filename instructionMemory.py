from myhdl import *
from memoryDictionaries import *


def instructionMemory(pc, clk, instruction, rd, rt, rs, programMemory):
    """ Stores all instructions and outputs appropriate signals after decoding them
    pc -- input instruction memory address
    instruction -- output
    clk -- clock input
    rd -- output (read reg2)
    rt -- output (read reg1)
    rs -- output (write reg)
    programMemory -- instruction memory loaded in at startup
    """

    # This basically means this function will run every time there is a
    # rising clock edge from the clk signal   
    @always(clk.posedge)
    def instrctionLogic():
        try:
            ins_line = programMemory[int(pc)]
            instruction.next = int(ins_line, 2)
        except KeyError:
            pass
        print("Instruction: %s " % (bin(instruction, 16)))
        opcode = instruction[:12]
        print("Opcode: %s" % (bin(opcode, 4)))
        if opcode == r_type:
            func = bin(instruction[3:0], 3)
            rd = bin(instruction[6:3], 3)
            rt = bin(instruction[9:6], 3)
            rs = bin(instruction[12:9], 3)
            print("%s %s %s %s" % (func_dict[func], registers_dict[rs], registers_dict[rt], registers_dict[rd]))

        elif opcode == jump:
            address = bin(instruction[12:], 12)
            print("%s %s" % (opcode_dict[bin(opcode, 4)], address))

        else:
            imm = bin(instruction[6:], 6)
            rt = bin(instruction[9:6], 3)
            rs = bin(instruction[12:9], 3)
            try:
                print("%s %s %s %s" % (opcode_dict[bin(opcode, 4)], registers_dict[rs], registers_dict[rt], imm))
            except KeyError:
                print("No instruction for opcode %s" % bin(opcode, 4))

        print("")

    return instrctionLogic

# def IF_ID_pipeline(instruction, clk):
#     """ Stores all instructions and outputs appropriate signals after decoding them

#     instruction -- input
#     clk -- clock input

#     """

#     # This basically means this function will run every time there is a
#     # rising clock edge from the clk signal   
#     @always(clk.posedge)
#     def instrctionLogic():