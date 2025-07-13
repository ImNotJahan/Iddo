def set_bit(value: int, bit: int) -> int:
    return value | (1 << bit)

def clear_bit(value: int, bit: int) -> int:
    return value & ~(1 << bit)