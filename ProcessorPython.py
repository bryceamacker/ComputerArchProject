v0 = v1 = v2 = v3 = t0 = t1 = a0 = a1 = 0
Mem = [None] * 1024

v0 = int("0040", 16)
v1 = int("1010", 16)
v2 = int("000F", 16)
v3 = int("00F0", 16)
t0 = int("0000", 16)
a0 = int("0010", 16)
a1 = int("0005", 16)

Mem[a0] =     int("0101", 16)
Mem[a0 + 2] = int("0110", 16)
Mem[a0 + 4] = int("0011", 16)
Mem[a0 + 6] = int("00F0", 16)
Mem[a0 + 8] = int("00FF", 16)

print
print
print ("***NORMAL ASSEMBLY***")
print ("INITIAL VALUES")
print ("v0: " + hex(v0))
print ("v1: " + hex(v1))
print ("v2: " + hex(v2))
print ("v3: " + hex(v3))
print ("t0: " + hex(t0))
print ("a0: " + hex(a0))
print ("a1: " + hex(a1))

print ("Mem[a0]: " + hex(Mem[a0]))
print ("Mem[a0 + 2]: " + hex(Mem[a0 + 2]))
print ("Mem[a0 + 4]: " + hex(Mem[a0 + 4]))
print ("Mem[a0 + 6]: " + hex(Mem[a0 + 6]))
print ("Mem[a0 + 8]: " + hex(Mem[a0 + 8]))
print

while (a1 > 0):
  a1 = a1 - 1
  t0 = Mem[a0]
  if (t0 > int("0100", 16)):
    v0 = v0/8
    v1 = v1 | v0
    Mem[a0] = int("FF00", 16)
  else:
    v2 = v2 * 4
    v3 = v3 ^ v2
    Mem[a0] = int("00FF", 16)

  a0 = a0 + 2

  # Zero out t0, because...reasons
  t0 = 0

print ("FINAL VALUES")
print ("v0: " + hex(v0))
print ("v1: " + hex(v1))
print ("v2: " + hex(v2))
print ("v3: " + hex(v3))
print ("t0: " + hex(t0))
print ("a0: " + hex(a0))
print ("a1: " + hex(a1))

a0 = int("0010", 16)
print ("Mem[a0]: " + hex(Mem[a0]))
print ("Mem[a0 + 2]: " + hex(Mem[a0 + 2]))
print ("Mem[a0 + 4]: " + hex(Mem[a0 + 4]))
print ("Mem[a0 + 6]: " + hex(Mem[a0 + 6]))
print ("Mem[a0 + 8]: " + hex(Mem[a0 + 8]))

executedCode = []

print
print
print ("***EXPANDED ASSEMBLY***")
# $t1 = 0
t1 = t1 & int("0", 16)
executedCode.append("andi $t1, $t1, 0x0")

# $v0 = 0x0040
v0 = t1 + int("4", 16)
executedCode.append("addi $v0, $t1, 0x4")
v0 = v0 << 4
executedCode.append("sll $v0, $v0, 4")

# $v1 = 0x1010
v1 = t1 + int("1", 16)
executedCode.append("addi $v1, $t1, 0x1")
v1 = v1 << 8
executedCode.append("sll $v1, $v1, 8")
v1 = v1 + int("1", 16)
executedCode.append("addi $v1, $v1, 0x1")
v1 = v1 << 4
executedCode.append("sll $v1, $v1, 4")

# $v2 = 0x000F
v2 = t1 + int("F", 16)
executedCode.append("addi $v2, $t1, 0xF")

# $v3 = 0x00F0
v3 = t1 + int("F", 16)
executedCode.append("addi $v3, $t1, 0xF")
v3 = v3 << 4
executedCode.append("sll $v3, $v3, 4")

# $t0 = 0x0000
t0 = t0 & 0
executedCode.append("andi $t0, $t0, 0x0")

# $a0 = 0x0010
a0 = t1 + int("1", 16)
executedCode.append("addi $a0, $t1, 0x1")
a0 = a0 << 4
executedCode.append("sll $a0, $a0, 4")

# $a1 = 0x0005
a1 = t1 + int("5", 16)
executedCode.append("addi $a1, $t1, 0x5")

Mem[a0] =     int("0101", 16)
Mem[a0 + 2] = int("0110", 16)
Mem[a0 + 4] = int("0011", 16)
Mem[a0 + 6] = int("00F0", 16)
Mem[a0 + 8] = int("00FF", 16)

print ("INITIAL VALUES")
print ("v0: " + hex(v0))
print ("v1: " + hex(v1))
print ("v2: " + hex(v2))
print ("v3: " + hex(v3))
print ("t0: " + hex(t0))
print ("a0: " + hex(a0))
print ("a1: " + hex(a1))

print ("Mem[a0]: " + hex(Mem[a0]))
print ("Mem[a0 + 2]: " + hex(Mem[a0 + 2]))
print ("Mem[a0 + 4]: " + hex(Mem[a0 + 4]))
print ("Mem[a0 + 6]: " + hex(Mem[a0 + 6]))
print ("Mem[a0 + 8]: " + hex(Mem[a0 + 8]))
print

while (1):
  # while ($a1 > 0)
  t0 = t0 & 0
  executedCode.append("andi $t0, $t0, 0x0")
  if t0 < a1:
    t1 = 1
  else:
    t1 = 0

  executedCode.append("slt $t1, $t0, $a1")
  executedCode.append("beq $t0, $t1, CONTINUE_LOOP")

  if t0 == t1:
    executedCode.append("j ENDLOOP")
    break

  #$a1 = $a1 - 1
  a1 = a1 - 1
  executedCode.append("subi $a1, $a1, 1")

  #$t0 = Mem[$a0]
  t0 = Mem[a0]
  executedCode.append("lw $t0, 0($a0)")

  # $t1 = 0x0100
  t1 = t1 & 0
  executedCode.append("andi $t1, $t1, 0")
  t1 = t1 + 1
  executedCode.append("addi $t1, $t1, 1")
  t1 = t1 << 8
  executedCode.append("sll $t1, $t1, 8")

  # if ($t0 > 0x0100)
  if t0 < t1:
    t1 = 1
  else:
    t1 = 0
  executedCode.append("slt $t1, $t0, $t1")
  executedCode.append("andi $t0, $t0, 0")

  if (t1 == 0):
    executedCode.append("beq $t1, $t0, IF")
    # $v0 = $v0 / 8
    v0 = v0 >> 3
    executedCode.append("srl $v0, $v0, 3")

    # $v1 = $v1 | $v0
    v1 = v1 | v0
    executedCode.append("or $v1, $v1, $v0")

    # $t1 = 0xFF00
    t1 = t1 & 0
    executedCode.append("andi $t1, $t1, 0x0")
    t1 = t1 + int("F", 16)
    executedCode.append("addi $t1, $t1, 0xF")
    t1 = t1 << 4
    executedCode.append("sll $t1, $t1, 4")
    t1 = t1 + int("F", 16)
    executedCode.append("addi $t1, $t1, 0xF")
    t1 = t1 << 8
    executedCode.append("sll $t1, $t1, 8")

    # Mem[$a0] = 0xFF00
    Mem[a0] = t1
    executedCode.append("sw $t1, 0($a0)")
    executedCode.append("j END")

  else:
    executedCode.append("j ELSE")
    # $v2 = $v2 x 2
    v2 = v2 << 2
    executedCode.append("sll $v2, $v2, 2")

    # $v3 = $v3 (x) $v2
    v3 = v3 ^ v2
    executedCode.append("xor $v3, $v3, $v2")

    # $t1 = 0x00FF
    t1 = t1 & 0
    executedCode.append("andi $t1, $t1, 0x0")
    t1 = t1 + int("F", 16)
    executedCode.append("addi $t1, $t1, 0xF")
    t1 = t1 << 4
    executedCode.append("sll $t1, $t1, 4")
    t1 = t1 + int("F", 16)
    executedCode.append("addi $t1, $t1, 0xF")

    # Mem[$a0] = 0x00FF
    Mem[a0] = t1
    executedCode.append("sw $t1, 0($a0)")
    executedCode.append("j END")

  # $a0 = $a0 + 2
  a0 = a0 + 2
  executedCode.append("addi $a0, $a0, 2")
  executedCode.append("j WHILE")


print ("FINAL VALUES")
print ("v0: " + hex(v0))
print ("v1: " + hex(v1))
print ("v2: " + hex(v2))
print ("v3: " + hex(v3))
print ("t0: " + hex(t0))
print ("t1: " + hex(t1))
print ("a0: " + hex(a0))
print ("a1: " + hex(a1))

a0 = int("0010", 16)
print ("Mem[a0]: " + hex(Mem[a0]))
print ("Mem[a0 + 2]: " + hex(Mem[a0 + 2]))
print ("Mem[a0 + 4]: " + hex(Mem[a0 + 4]))
print ("Mem[a0 + 6]: " + hex(Mem[a0 + 6]))
print ("Mem[a0 + 8]: " + hex(Mem[a0 + 8]))

print
print ("Executed lines:")
for instructionNum, instruction in enumerate(executedCode):
    print str(instructionNum) + ": " + instruction
