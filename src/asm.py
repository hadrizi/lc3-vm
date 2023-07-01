from typing import List


def _split(opcode: int) -> List[int]:
    return [opcode >> 8, opcode & 255]


def NOT(dst: int, src: int) -> List[int]:
    return _split(
        int('1001{:03b}{:03b}111111'.format(dst, src), 2))


def ADD(dst: int, **kwargs) -> List[int]:
    if "imm" in kwargs:
        return _split(int('0001{:03b}{:03b}1{:05b}'.format(
            dst, kwargs["src1"], kwargs["imm"]), 2))
    return _split(int('0001{:03b}{:03b}000{:03b}'.format(
        dst, kwargs["src1"], kwargs["src2"]), 2))


def AND(dst: int, **kwargs) -> List[int]:
    if "imm" in kwargs:
        return _split(int('0101{:03b}{:03b}1{:05b}'.format(
            dst, kwargs["src1"], kwargs["imm"]), 2))
    return _split(int('0101{:03b}{:03b}000{:03b}'.format(
        dst, kwargs["src1"], kwargs["src2"]), 2))


def LD(dst: int, offset: int, indirect: bool = False) -> List[int]:
    return _split(int('{}010{:03b}{:09b}'.format(
        1 if indirect else 0, dst, offset), 2))


def ST(src: int, offset: int, indirect: bool = False) -> List[int]:
    return _split(int('{}011{:03b}{:09b}'.format(
        1 if indirect else 0, src, offset), 2))


def LDR(dst: int, base: int, offset:int) -> List[int]:
    return _split(int('0110{:03b}{:03b}{:06b}'.format(dst, base, offset), 2))


def STR(src: int, base: int, offset:int) -> List[int]:
    return _split( int('0111{:03b}{:03b}{:06b}'.format(src, base, offset), 2))


def LEA(dst: int, offset: int) -> List[int]:
    return _split(int('1110{:03b}{:09b}'.format(dst, offset), 2))


def BR(n: bool, z: bool, p: bool, offset: int) -> List[int]:
    return _split(int('0000{:01b}{:01b}{:01b}{:09b}'.format(
            1 if n else 0, 1 if z else 0, 1 if p else 0, 
            offset), 2))


def JMP(base: int) -> List[int]:
    return _split(
        int('1100000{:03b}000000'.format(base), 2))


def JSR(long: bool, **kwargs) -> List[int]:
    if long:
        return _split(int('01001{:011b}'.format(kwargs["offset"]), 2))
    return _split(int('0100000{:03b}000000'.format(kwargs["base"]), 2))


def TRAP(vector: int) -> List[int]:
    return _split(int('11110000{:08b}'.format(vector), 2))

