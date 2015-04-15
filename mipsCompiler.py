#!/usr/local/bin/python

#########################################################################################################
#########################################################################################################
#
################ R-Type Format ################
# Instruction Format:
# [opcode]     [rs]    [rt]   [rd]   [func]
#  [15:12]    [11:9]  [8:6]  [5:3]   [2:0]
#
# Assembly Format:
# add $rd, $rs, $rt
# slt $rd, $rs, $rt
#
# Examples:
# add $r1, $r2, $r3: $r1 = $r2 + $r3
# slt $r1, $r2, $r3: $r1 = ($r2 < $r3) ? 1 : 0
#
###############################################
#
################ I-Type Format ################
# Instruction Format:
# [opcode]     [rs]    [rt]   [immediate]
#  [15:12]    [11:9]   [8:6]     [5:0]
#
# Assembly Format:
# addi $rt, $rs, immediate
# lw $rt, immediate($rs)
# beq $rt, $rs, immediate
# sll $rt, $rs, immediate
#
# Examples:
# addi $r1, $r2, 8: $r1 = $r2 + 8
# lw $r1, 4($r2): $r1 = M[$r2 + 4]
# beq $r1, $r2, LABEL: if($r1 == $r2) PC = PC + 4 + LABEL
# sll $r1, $r2, 8: $r1 = $r3 << 8
#
###############################################
#
################ J-Type Format ################
# Instruction Format:
# [opcode] [address]
#  [15:12]  [11:0]
#
# Assembly Format:
# j JumpAddr
#
# Examples:
# j LABEL: PC = LABEL
#
###############################################
#
#########################################################################################################
#########################################################################################################

# Arrays to hold all the types of commands
rTypes = ["add", "sub", "and", "or", "xor", "slt"]
iTypes = ["slti", "addi", "subi", "andi", "ori", "lw", "sw", "sll", "srl", "beq"]
jTypes = ["j"]

# Dictionary for opcodes and their binary values
opcodeDictionary = {
  "add":  "0000",
  "sub":  "0000",
  "and":  "0000",
  "or":   "0000",
  "xor":  "0000",
  "slt":  "0000",
  "slti": "0000",
  "addi": "0001",
  "subi": "0010",
  "andi": "0011",
  "ori":  "0100",
  "lw":   "0110",
  "sw":   "0111",
  "sll":  "1000",
  "srl":  "1001",
  "j":    "1010",
  "beq":  "1011"
}

# Dictionary for operations and their function codes
funcDictionary = {
  "add":  "000",
  "sub":  "001",
  "and":  "010",
  "or":   "011",
  "xor":  "100",
  "slt":  "101",
  "slti": "110",
}

# Register addresses
registerDictionary = {
  "$a0":  "000",
  "$a1":  "001",
  "$v0":  "010",
  "$v1":  "011",
  "$t0":  "100",
  "$t1":  "101",
  "$v2":  "110",
  "$v3":  "111"
}

labels = {}
codeWithoutLabels = []

def compile(fileName):
  global labels, codeWithoutLabels

  machineCode = []
  codeLines = []

  codeLines = stripComments(fileName)
  labels, codeWithoutLabels = getLabels(codeLines)

  for lineNum, line in enumerate(codeWithoutLabels):
    line = parseLine(line, lineNum)
    machineCode.append(line)

  return machineCode

def parseLine(line, lineNum):
  pieces = line.split()

  opcode = pieces[0]

  if opcode in rTypes:
    return parseRTypeLine(line)
  elif opcode in iTypes:
    return parseITypeLine(line, lineNum)
  elif opcode in jTypes:
    return parseJTypeLine(line, lineNum)

def parseRTypeLine(line):
  pieces = line.split()

  opcode = pieces[0]
  rd = pieces[1].replace(',', '')
  rs = pieces[2].replace(',', '')
  rt = pieces[3].replace(',', '')

  binary = opcodeDictionary[opcode] + registerDictionary[rs] + registerDictionary[rt] + registerDictionary[rd] + funcDictionary[opcode]
  return binary

def parseITypeLine(line, lineNum):
  pieces = line.split()

  opcode = pieces[0]
  rt = pieces[1].replace(',', '')
  if opcode == "lw" or opcode == "sw":
    rsImmediate = pieces[2]
    secondaryPieces = rsImmediate.split("(")
    immediate = secondaryPieces[0]
    rs = secondaryPieces[1][0:3].replace(',', '')

  else:
    rs = pieces[2].replace(',', '')
    immediate = pieces[3]

  binary = opcodeDictionary[opcode] + registerDictionary[rs] + registerDictionary[rt] + expandImmediate(immediate, 6, lineNum, 1)
  return binary

def parseJTypeLine(line, lineNum):
  pieces = line.split()

  opcode = pieces[0]
  address = pieces[1]

  binary = opcodeDictionary[opcode] + expandImmediate(address, 12, lineNum, 0)
  return binary

def getLabels(codeLines):
  numOfLabels = 0
  labels = {}
  codeWithoutLabels = []

  for lineNum, line in enumerate(codeLines):
      pieces = line.split()
      if pieces[0].endswith(":"):
        labels[pieces[0].strip(":")] = str((lineNum-numOfLabels)*2)
        numOfLabels += 1
      else:
        codeWithoutLabels.append(line)
  return labels, codeWithoutLabels

def expandImmediate(value, numBits, lineNum, relative):
  if value in labels:
    base = 10
    if relative == 1:
        number = str(int(labels[value]) - int(lineNum*2) - 2)
    else:
        number = labels[value]

  elif value.startswith("0x"):
    number = value[2:]
    base = 16
  else:
    number = value
    base = 10

  binary = bin(int(number, base))[2:].zfill(numBits)

  return binary

def printCode(code):
  for lineNum, line in enumerate(code):
    print line[0:4],
    print ' ',
    print line[4:8],
    print ' ',
    print line[8:12],
    print ' ',
    print line[12:16],
    print ' ',
    print str(lineNum) + ": ",
    print codeWithoutLabels[lineNum].strip(),
    print

def stripComments(fileName):
  codeLines = []

  with open(fileName) as f:
      for lineNum, line in enumerate(f):
          if line != "\n" and not (line.lstrip().startswith("#")):
              codeLines.append(line)
  return codeLines


if __name__ == '__main__':
  machineCode = compile("ProcessorAssembly")
  # printCode(machineCode)
