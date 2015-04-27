# Opcodes
r_type = 0
addi = 1
subi = 2
andi = 3
ori = 4
lw = 6
sw = 7
sll = 8
srl = 9
jump = 10
beq = 11

# Funcs
add = 0
sub = 1
logical_and = 2
logical_or = 3
xor = 4
slt = 5

# Initialize memory with proper values
memory=[i for i in range(26)]
a0 = 16
memory[a0] =     int("0101", 16)
memory[a0 + 2] = int("0110", 16)
memory[a0 + 4] = int("0011", 16)
memory[a0 + 6] = int("00F0", 16)
memory[a0 + 8] = int("00FF", 16)


func_dict = {'000': 'add',
         '001': 'sub',
         '010': 'and',
         '011': 'or',
         '100': 'xor',
         '101': 'slt'}

# Register file
registers_dict = {'000': 'a0',
                 '001': 'a1',
                 '010': 'v0',
                 '011': 'v1',
                 '100': 't0',
                 '101': 't1',
                 '110': 'v2',
                 '111': 'v3'}

registers_mem = { 0: '0000000000000000',
                  1: '0000000000000000',
                  2: '0000000000000000',
                  3: '0000000000000000',
                  4: '0000000000000000',
                  5: '0000000000000000',
                  6: '0000000000000000',
                  7: '0000000000000000'}

# Opcodes
opcode_dict = {'0000': 'r_type',
               '0001': 'addi',
               '0010': 'subi',
               '0011': 'andi',
               '0100': 'ori',
               '0110': 'lw',
               '0111': 'sw',
               '1000': 'sll',
               '1001': 'srl',
               '1010': 'j',
               '1011': 'beq'}
