import sys
from src import asm, opcodes
from src.utils import getch
from typing import List
from collections import namedtuple

MEMORY_SIZE = 65536

ConditionCodes = namedtuple('ConditionCodes', ['n', 'z', 'p'])

class Register:
    def __init__(self, value) -> None:
        self.value = value

    def __str__(self) -> str:
        return f"register value {self.value}"

class lc3:
    class HaltException(Exception):
        ...
    
    opcodes = {
        0b0001: opcodes.ADD, # ADD
        0b0101: opcodes.AND, # AND
        0b0000: opcodes.BR, # BR
        0b1100: opcodes.JMP, # JMP
        0b0100: opcodes.JSR, # JSR/JSRR
        0b0010: opcodes.LD, # LD
        0b1010: opcodes.LDI, # LDI
        0b0110: opcodes.LDR, # LDR
        0b1110: opcodes.LEA, # LEA
        0b1001: opcodes.NOT, # NOT
        0b1000: lambda: ..., # RTI unused since trap vectors are handled on host side
        0b0011: opcodes.ST, # ST
        0b1011: opcodes.STI, # STI
        0b0111: opcodes.STR, # STR
        0b1111: opcodes.TRAP, # TRAP
    }

    def __init__(self) -> None:
        self.memory = [0] * MEMORY_SIZE
        self.registers: List[Register] = []
        for _ in range(8):
            self.registers.append(Register(0))
        self.trap_table = {
            0x23: self._read_char,
            0x21: self._print_char,
            0x25: self._halt
        }
        self.condition_codes = ConditionCodes(False, False, False)
        self.pc = 0x3000

    def run(self, program: List[int]):
        while True:
            op = (program[self.pc] << 8) | program[self.pc + 1]
            self.pc += 2
            try:
                lc3.opcodes[(op >> 12)](self, op)
            except lc3.HaltException:
                print("halting lc3-vm")
                exit(0)

    def set_register(self, id: int, value: int):
        self.registers[id] = value
        self.condition_codes = (
            True if value <  0 else False,
            True if value == 0 else False,
            True if value >  0 else False,
        )

    def execute_trap_vector(self, vector: int):
        self.trap_table[vector]()
    
    def _read_char(self):
        c = getch()
        self.registers[0].value = ord(c)
    
    def _print_char(self):
        print(chr(self.registers[0].value), end='', flush=True)

    def _halt(self):
        raise lc3.HaltException



def main(filename = None):
    vm = lc3()
    if filename:
        with open(filename) as f:
            program = list(bytearray(f.read()))
    else:
        program = [0] * 0x3000
        program.append([
            *asm.TRAP(0x23),
            *asm.TRAP(0x21),
        ])
    
    vm.run(program)

    print(program)
    
    print("Registers:")
    for i, r in enumerate(vm.registers):
        print(f"[{i}] ", r)
    
    print("Memory:")
    for i in range(15):
        print(f"mem [{i}] ", vm.memory[i])

if __name__ == "__main__":
    if len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        main()
