import sys
from assembler import *
from CPU import *

import re
DUMP_RE = re.compile(r'^[0-9A-Fa-f]{1,3}H?-[0-9A-Fa-f]{1,3}H?$')

def is_dump_range(arg: str) -> bool:
    return bool(DUMP_RE.match(arg))

def parse_dump_arg(s):
    a, b = s.split('-', 1)
    a = int(a[:-1] if a.upper().endswith('H') else a, 16)
    b = int(b[:-1] if b.upper().endswith('H') else b, 16)
    return (a & 0xFF, b & 0xFF)

def main():
    if len(sys.argv) < 2:
        print("Use: python z70.py src.z70 [dump-range (hex)] [outfile]")
        print("Example [dump-range]: 80H-83H (memory [00H-FFH])")
        sys.exit(1)

    src = sys.argv[1]
    dump = None
    outfile = None

    if len(sys.argv) >= 3:
        maybe = sys.argv[2]
        if is_dump_range(maybe):
            dump = parse_dump_arg(maybe)
            if len(sys.argv) >= 4:
                outfile = sys.argv[3]
        else:
            outfile = maybe

    lines = open(src, encoding='utf-8').read().splitlines()
    pp = preprocess(lines)
    parsed, labels = first_pass(pp)
    mem, listing, code_end = second_pass(parsed, labels)

    cpu = CPU(mem, labels)
    cpu.program_end = code_end
    cpu.run()

    print(f'REGS:  {cpu.regs()}')
    print(f'FLAGS: {cpu.flags()}')

    if dump:
        a, b = dump
        rng = range(a, b + 1) if a <= b else list(range(a, 256)) + list(range(0, b + 1))
        hx = ' '.join(f"{i:02X}H:{cpu.mem[i]:02X}H" for i in rng)
        s = ''.join(chr(cpu.mem[i]) if 32 <= cpu.mem[i] <= 126 else '.' for i in rng)
        print("DUMP:", hx)
        print("ASCII:", s)

    if outfile:
        with open(outfile, 'w', encoding='utf-8') as fo:
            for start_addr, bs, src in listing:
                cod = f"{start_addr:02X}H " + ' '.join(f"{b:02X}H" for b in bs)
                fo.write(f"{cod:<18}{src}\n")
        print("Wrote", outfile)

if __name__ == '__main__':
    main()