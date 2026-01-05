import re
from arch import *

HEX_RE = re.compile(r'^(-)?[0-9A-Fa-f]+H?$')

def is_hex(arg: str) -> bool:
    return bool(HEX_RE.match(arg))

def parse_hex(s: str) -> int:
    neg = s.startswith('-')
    s = s[1:] if neg else s
    s = s[:-1] if s.upper().endswith('H') else s
    val = int(s, 16)
    if neg:
        val = -val
        val = (256 + val) & 0xFF  # Two's complement
    #print(f'Debbug: ({s}) -> {val & 0xFF}')
    return val & 0xFF

def preprocess(lines):
    processed = []
    for line in lines:
        if '//' in line:
            line = line.split('//', 1)[0]
        line = line.strip()
        if line:
            processed.append(line)
    return processed

def parse_line(line):
    label = None
    instr_part = line
    if ':' in line:
        parts = line.split(':', 1)
        label = parts[0].strip()
        instr_part = parts[1].strip() if len(parts) > 1 else None
    if not instr_part:
        return label, None, [], line
    parts = re.split(r'\s+', instr_part)
    instr = parts[0].lower()
    args_str = ' '.join(parts[1:]) if len(parts) > 1 else ''
    args = [a.strip() for a in args_str.split(',') if a.strip()]
    return label, instr, args, line

def first_pass(lines):
    addr = 0
    labels = {}
    parsed = []
    for line in lines:
        lbl, instr, args, orig = parse_line(line)
        if lbl:
            if lbl in labels:
                raise ValueError(f"Duplicate label: {lbl}")
            labels[lbl] = addr
        if instr:
            parsed.append((instr, args, orig))
            size = get_instr_size(instr, args)
            addr += size
    return parsed, labels

def get_instr_size(instr, args):
    instr = instr.lower()
    if instr in JUMP_CODES:
        return 2
    elif instr == 'nop':
        return 1
    else:
        dst_src = get_dst_src(instr, args)
        _, extra = find_mode(*dst_src)
        return 1 + (1 if extra is not None else 0)

def parse_arg(arg):
    arg = arg.strip()
    if arg in ['A', 'B', 'I']:
        return ('reg', arg)
    elif arg == '[I]':
        return ('ind_i', None)
    elif arg.startswith('[') and arg.endswith(']'):
        inner = arg[1:-1].strip()
        if is_hex(inner):
            return ('dir', parse_hex(inner))
        else:
            raise ValueError(f"Invalid direct mem: {arg}")
    elif is_hex(arg):
        return ('const', parse_hex(arg))
    else:
        raise ValueError(f"Invalid arg: {arg}")

def get_dst_src(mnemon, args):
    is_unary = mnemon in UNARY_MNEMONS
    if is_unary:
        if len(args) != 1:
            raise ValueError(f"{mnemon} expects 1 arg")
        dst = parse_arg(args[0])
        src = None
    else:
        if len(args) != 2:
            raise ValueError(f"{mnemon} expects 2 args")
        dst = parse_arg(args[0])
        src = parse_arg(args[1])
    return dst, src

def find_mode(dst, src=None):
    is_unary = src is None
    if is_unary:
        target_dst = dst
        modes_dict = UNARY_MODES
        for m, (d, _) in modes_dict.items():
            if d[0] == target_dst[0] and d[1] == target_dst[1]:
                return m, None
    else:
        modes_dict = MODES
        for m, (d, s) in modes_dict.items():
            match_d = (d[0] == dst[0]) and (d[1] == dst[1] if d[1] != 'extra' else True)
            match_s = (s[0] == src[0]) and (s[1] == src[1] if s[1] != 'extra' else True)
            if match_d and match_s:
                extra = None
                if d[1] == 'extra':
                    extra = dst[1]
                elif s[1] == 'extra':
                    extra = src[1]
                return m, extra
    raise ValueError(f"No mode found for {dst} {src}")

def second_pass(parsed, labels):
    mem = [0] * 256
    listing = []
    addr = 0
    for instr, args, orig in parsed:
        bytes_list = encode(instr, args, labels, addr)
        for b in bytes_list:
            mem[addr] = b
            addr += 1
        listing.append((addr - len(bytes_list), bytes_list, orig))
    return mem, listing, addr

def encode(instr, args, labels, current_addr):
    instr = instr.lower()
    if instr in JUMP_CODES:
        if len(args) != 1:
            raise ValueError("Jump expects 1 label")
        label = args[0]
        addr = labels.get(label)
        if addr is None:
            raise ValueError(f"Unknown label: {label}")
        return [JUMP_CODES[instr], addr]
    elif instr == 'nop':
        if args:
            raise ValueError("nop no args")
        return [0xFF]
    elif instr in OPCODES:
        op = OPCODES[instr]
        dst, src = get_dst_src(instr, args)
        mode, extra = find_mode(dst, src)
        instr_byte = (op << 4) | mode
        if extra is not None:
            return [instr_byte, extra]
        return [instr_byte]
    else:
        raise ValueError(f"Unknown instr: {instr}")