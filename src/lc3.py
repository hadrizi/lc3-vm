from src import asm, opcodes
from typing import List

MEMORY_SIZE = 65536

class Register:
    def __init__(self, value) -> None:
        self.value = value

    def __str__(self) -> str:
        return f"register value {self.value}"

class lc3:
    opcodes = {
        0b0001: opcodes.ADD, # ADD
        0b0101: opcodes.AND, # AND
        0b0000: ..., # BR
        0b1100: ..., # JMP
        0b0100: ..., # JSR/JSRR
        0b0010: opcodes.LD, # LD
        0b1010: opcodes.LDI, # LDI
        0b0110: opcodes.LDR, # LDR
        0b1110: ..., # LEA
        0b1001: opcodes.NOT, # NOT
        0b1100: ..., # RET
        0b1000: ..., # RTI
        0b0011: opcodes.ST, # ST
        0b1011: opcodes.STI, # STI
        0b0111: opcodes.STR, # STR
        0b1111: ..., # TRAP
    }

    def __init__(self) -> None:
        self.memory = [0] * MEMORY_SIZE
        self.registers: List[Register] = []
        for _ in range(8):
            self.registers.append(Register(0))
        self.pc = 0
        self.cycles = 0

    def run(self, program: List[int]):
        for op in program:
            self.opcodes[(op >> 12) & 15](self, op)


def main():
    vm = lc3()
    vm.registers[1].value = 15
    vm.registers[3].value = 16
    vm.registers[5].value = 6
    vm.registers[6].value = 17
    vm.registers[7].value = 7
    vm.memory[1] = 100
    vm.memory[3] = 4
    vm.memory[4] = 101
    vm.memory[5] = 6
    vm.memory[8] = 102
    program = [
        asm.LD(0, 1),
        asm.ST(1, 2),
        asm.LD(2, 3, True),
        asm.ST(3, 5, True),
        asm.LDR(4, 5, 2),
        asm.STR(6, 7, 3),
    ]
    vm.run(program)

    print(program)
    
    print("Registers:")
    for i, r in enumerate(vm.registers):
        print(f"[{i}] ", r)
    
    print("Memory:")
    for i in range(15):
        print(f"mem [{i}] ", vm.memory[i])

if __name__ == "__main__":
    main()
