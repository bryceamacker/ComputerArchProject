from myhdl import *
from memoryDictionaries import *
from mipsCompiler import *

# Compile our program
pa = compile('ProcessorAssembly')
programMemory = {}
i = 0
for line in pa:
    programMemory[int(i)] = line
    i += 2

def instructionMemory(clk, pc, instruction):
    """ Stores all instructions and outputs appropriate signals after decoding them
    clk             -- input, clock line
    pc              -- input, instruction memory address
    instruction     -- output, next instruction
    """

    @always_comb
    def instructionLogic():
        try:
            ins_line = programMemory[int(pc)]
            instruction.next = int(ins_line, 2)
        except KeyError:
            pass

    return instructionLogic

def instructionDecode(instruction, opcode, rs, rt, rd, func, immediate, address, stall):
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
        opcodeTmp = instruction[16:12]

        opcode.next = instruction[16:12]
        rs.next = instruction[12:9]
        rt.next = instruction[9:6]
        rd.next = instruction[6:3]
        func.next = instruction[3:0]
        immediate.next = instruction[6:0]
        address.next = instruction[12:0]

    return instructionDecodeLogic
