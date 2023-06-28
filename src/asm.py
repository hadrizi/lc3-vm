def NOT(dst: int, src: int) -> int:
    return int('1001{:03b}{:03b}111111'.format(dst, src), 2)


def ADD(dst: int, **kwargs) -> int:
    if "imm" in kwargs:
        return int('0001{:03b}{:03b}1{:05b}'.format(
            dst, kwargs["src1"], kwargs["imm"]), 2)
    else:
        return int('0001{:03b}{:03b}000{:03b}'.format(
            dst, kwargs["src1"], kwargs["src2"]), 2)


def AND(dst: int, **kwargs) -> int:
    if "imm" in kwargs:
        return int('0101{:03b}{:03b}1{:05b}'.format(
            dst, kwargs["src1"], kwargs["imm"]), 2)
    else:
        return int('0101{:03b}{:03b}000{:03b}'.format(
            dst, kwargs["src1"], kwargs["src2"]), 2)


def LD(dst: int, offset: int, indirect: bool = False):
    return int('{}010{:03b}{:09b}'.format(
        1 if indirect else 0, dst, offset), 2)


def ST(src: int, offset: int, indirect: bool = False):
    return int('{}011{:03b}{:09b}'.format(
        1 if indirect else 0, src, offset), 2)


def LDR(dst: int, base: int, offset:int):
    return int('0110{:03b}{:03b}{:06b}'.format(dst, base, offset), 2)


def STR(src: int, base: int, offset:int):
    return int('0111{:03b}{:03b}{:06b}'.format(src, base, offset), 2)
