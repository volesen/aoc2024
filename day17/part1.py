from enum import Enum
from utils import parse_input


class OpCode(Enum):
    ADV = 0
    BXL = 1
    BST = 2
    JNZ = 3
    BXC = 4
    OUT = 5
    BDV = 6
    CDV = 7


class VM:
    def __init__(self, ip, a, b, c, instrs):
        self.ip = ip
        self.a = a
        self.b = b
        self.c = c

        self.instrs = instrs
        self.outputs = []

    def combo_operand(self, operand: int) -> int:
        match operand:
            case 0 | 1 | 2 | 3:
                return operand
            case 4:
                return self.a
            case 5:
                return self.b
            case 6:
                return self.c
            case _:
                raise ValueError(f"Invalid operand {operand}")

    def step(self):
        opcode = self.instrs[self.ip]
        operand = self.instrs[self.ip + 1]

        match OpCode(opcode):
            case OpCode.ADV:
                self.a //= 2 ** self.combo_operand(operand)
                self.ip += 2
            case OpCode.BXL:
                self.b ^= operand
                self.ip += 2
            case OpCode.BST:
                self.b = self.combo_operand(operand) % 8
                self.ip += 2
            case OpCode.JNZ:
                self.ip = operand if self.a != 0 else self.ip + 2
            case OpCode.BXC:
                self.b ^= self.c
                self.ip += 2
            case OpCode.OUT:
                output = self.combo_operand(operand) % 8
                self.outputs.append(output)
                self.ip += 2
            case OpCode.BDV:
                self.a = self.a // 2 ** self.combo_operand(operand)
                self.ip += 2
            case OpCode.CDV:
                self.c = self.a // 2 ** self.combo_operand(operand)
                self.ip += 2

    def run(self):
        while self.ip < len(self.instrs):
            self.step()

        return self.outputs


if __name__ == "__main__":
    with open("input.txt") as f:
        regs, instrs = parse_input(f.read())

    vm = VM(0, *regs, instrs)

    print(vm.run())
