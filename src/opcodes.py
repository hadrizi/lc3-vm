from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from lc3 import lc3


def NOT(vm: lc3, opcode: int):
    dst = (opcode >> 9) & 7
    src = (opcode >> 6) & 7
    vm.registers[dst].value = ~vm.registers[src].value


def AND(vm: lc3, opcode: int):
    dst = (opcode >> 9) & 7
    src1 = vm.registers[(opcode >> 6) & 7].value
    if opcode & (1 << 5):
        src2 = opcode & 31
    else:
        src2 = vm.registers[opcode & 7].value
    vm.registers[dst].value = src1 & src2


def ADD(vm: lc3, opcode: int):
    dst = (opcode >> 9) & 7
    src1 = vm.registers[(opcode >> 6) & 7].value
    if opcode & (1 << 5):
        src2 = opcode & 31
    else:
        src2 = vm.registers[opcode & 7].value
    vm.registers[dst].value = src1 + src2


def LD(vm: lc3, opcode: int):
    dst = (opcode >> 9) & 7
    offset = opcode & 511
    vm.registers[dst].value = vm.memory[vm.pc + offset]


def ST(vm: lc3, opcode: int):
    src = (opcode >> 9) & 7
    offset = offset = opcode & 511
    vm.memory[vm.pc + offset] = vm.registers[src].value


def LDI(vm: lc3, opcode: int):
    dst = (opcode >> 9) & 7
    offset = opcode & 511
    src = vm.memory[vm.pc + offset]
    vm.registers[dst].value = vm.memory[src]


def STI(vm: lc3, opcode: int):
    src = (opcode >> 9) & 7
    offset = offset = opcode & 511
    dst = vm.memory[vm.pc + offset]
    vm.memory[dst] = vm.registers[src].value


def LDR(vm: lc3, opcode: int):
    dst = (opcode >> 9) & 7
    base = vm.registers[(opcode >> 6) & 7].value
    offset = opcode & 63
    vm.registers[dst].value = vm.memory[base+offset]


def STR(vm: lc3, opcode: int):
    src = (opcode >> 9) & 7
    base = vm.registers[(opcode >> 6) & 7].value
    offset = offset = opcode & 63
    vm.memory[base + offset] = vm.registers[src].value

