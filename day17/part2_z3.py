from utils import parse_input
from z3 import *

with open("input.txt") as f:
    _, instrs = parse_input(f.read())


bv = BitVec("a", 8 * 16)
opt = Optimize()

a = bv

# Translated and optimized from the specific input.
# NOTE: We could also have reused the VM from part1, with a as a bit vector.
for x in instrs:
    b = a % 8
    b ^= 1
    c = a >> b
    b ^= 5
    b ^= c
    a = a >> 3
    opt.add((b % 8) == x)

opt.add(a == 0)

opt.minimize(bv)
assert opt.check() == sat

print(opt.model()[bv])
