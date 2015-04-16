from myhdl import *
from memoryDictionaries import *


def instructionMemory(clk, pc, instruction, programMemory):
    """ Stores all instructions and outputs appropriate signals after decoding them
    clk             -- input, clock line
    pc              -- input, instruction memory address
    instruction     -- output, next instruction
    programMemory   -- input, instruction memory loaded in at startup, PROBABLY SHOULD FIND A BETTER WAY TO DO THIS
    """

    # This basically means this function will run every time there is a
    # rising clock edge from the clk signal
    @always(clk.posedge)
    def instructionLogic():
        opcode = Signal()
        rd = Signal()
        rt = Signal()
        rs = Signal()

        try:
            ins_line = programMemory[int(pc)]
            instruction.next = int(ins_line, 2)
        except KeyError:
            pass
        # print("Instruction: %s " % (bin(instruction, 16)))
        opcode = instruction[:12]
        # print("Opcode: %s" % (bin(opcode, 4)))
        if opcode == r_type:
            func = bin(instruction[3:0], 3)
            rd = bin(instruction[6:3], 3)
            rt = bin(instruction[9:6], 3)
            rs = bin(instruction[12:9], 3)
            print("%s %s %s %s" % (func_dict[func], registers_dict[rd], registers_dict[rs], registers_dict[rt])),

        elif opcode == jump:
            address = bin(instruction[12:], 12)
            print("%s %s" % (opcode_dict[bin(opcode, 4)], address)),

        else:
            imm = bin(instruction[6:], 6)
            rt = bin(instruction[9:6], 3)
            rs = bin(instruction[12:9], 3)
            try:
                print("%s %s %s %s" % (opcode_dict[bin(opcode, 4)], registers_dict[rt], registers_dict[rs], imm)),
            except KeyError:
                print("No instruction for opcode %s" % bin(opcode, 4))

        opcode.next = opcode

    return instructionLogic

def instructionDecode(instruction, opcode, rs, rt, rd, func, immediate, address):
    """ Stores all instructions and outputs appropriate signals after decoding them
    instruction     -- input, next instruction
    opcode          -- output, instruction[15:12]
    rs              -- output, instruction[11:9]
    rt              -- output, instruction[8:6]
    rd              -- output, instruction[5:3]
    func            -- output, instruction[2:0]
    immediate       -- output, instruction[5:0]
    address         -- output, instruction[12:11]
    """

    @always_comb
    def instructionDecodeLogic():
        opcode.next = instruction[16:12]
        rs.next = instruction[12:9]         #- to read_reg_1
        rt.next = instruction[9:6]         #- to read_reg_2 and mux controlled by RegDst
        rd.next = instruction[6:3]         #- to the mux controlled by RegDst
        func.next = instruction[3:0]         #- to ALUCtrl
        immediate.next = instruction[6:0]     #- to Sign Extend
        address.next = instruction[12:0]     #- to Sign Extend

    return instructionDecodeLogic

# def IF_ID_pipeline(instruction, clk):
#     """ Stores all instructions and outputs appropriate signals after decoding them

#     instruction -- input
#     clk -- clock input

#     """

#     # This basically means this function will run every time there is a
#     # rising clock edge from the clk signal
#     @always(clk.posedge)
#     def instrctionLogic():
