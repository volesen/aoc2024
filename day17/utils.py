import re


def parse_input(program: str):
    regs, instrs = program.split("\n\n")

    regs = [int(x) for x in re.findall(r"\d+", regs)]
    instrs = [int(x) for x in re.findall(r"\d+", instrs)]

    return regs, instrs
