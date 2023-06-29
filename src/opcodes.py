from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from lc3 import lc3


def NOT(vm: lc3, opcode: int):
    dst = (opcode >> 9) & 7
    src = (opcode >> 6) & 7
    vm.set_register(dst, ~vm.registers[src].value)


def AND(vm: lc3, opcode: int):
    dst = (opcode >> 9) & 7
    src1 = vm.registers[(opcode >> 6) & 7].value
    if opcode & (1 << 5):
        src2 = opcode & 31
    else:
        src2 = vm.registers[opcode & 7].value
    vm.set_register(dst, src1 & src2)


def ADD(vm: lc3, opcode: int):
    dst = (opcode >> 9) & 7
    src1 = vm.registers[(opcode >> 6) & 7].value
    if opcode & (1 << 5):
        src2 = opcode & 31
    else:
        src2 = vm.registers[opcode & 7].value
    vm.set_register(dst, src1 + src2)


def LD(vm: lc3, opcode: int):
    dst = (opcode >> 9) & 7
    offset = opcode & 511
    vm.set_register(dst, vm.memory[vm.pc + offset])


def ST(vm: lc3, opcode: int):
    src = (opcode >> 9) & 7
    offset = offset = opcode & 511
    vm.memory[vm.pc + offset] = vm.registers[src].value


def LDI(vm: lc3, opcode: int):
    dst = (opcode >> 9) & 7
    offset = opcode & 511
    src = vm.memory[vm.pc + offset]
    vm.set_register(dst, vm.memory[src])


def STI(vm: lc3, opcode: int):
    src = (opcode >> 9) & 7
    offset = offset = opcode & 511
    dst = vm.memory[vm.pc + offset]
    vm.memory[dst] = vm.registers[src].value


def LDR(vm: lc3, opcode: int):
    dst = (opcode >> 9) & 7
    base = vm.registers[(opcode >> 6) & 7].value
    offset = opcode & 63
    vm.set_register(dst, vm.memory[base+offset])


def STR(vm: lc3, opcode: int):
    src = (opcode >> 9) & 7
    base = vm.registers[(opcode >> 6) & 7].value
    offset = offset = opcode & 63
    vm.memory[base + offset] = vm.registers[src].value


def LEA(vm: lc3, opcode: int):
    dst = (opcode >> 9) & 7
    offset = opcode & 511
    vm.registers[dst].value = vm.pc + offset


def BR(vm: lc3, opcode: int):
    n = bool((opcode >> 11) & 1)
    z = bool((opcode >> 10) & 1)
    p = bool((opcode >>  9) & 1)
    offset = opcode & 511

    if (
        (n and vm.condition_codes.n) or 
        (z and vm.condition_codes.z) or 
        (p and vm.condition_codes.p)
    ):
        vm.pc += offset


def JMP(vm: lc3, opcode: int):
    base = (opcode >> 6) & 7
    vm.pc = vm.registers[base].value


def JSR(vm: lc3, opcode: int):
    is_long = bool((opcode >> 11) & 1)
    vm.registers[7].value = vm.pc
    if is_long:
        offset = opcode & 2047
        vm.pc += offset
    else:
        src = (opcode >> 6) & 7
        vm.pc = vm.registers[src].value


def TRAP(vm: lc3, opcode: int):
    vector = opcode & 255
    vm.execute_trap_vector(vector)