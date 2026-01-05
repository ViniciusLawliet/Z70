from arch import *

def handle_mov(cpu, dst_loc, src_loc):
    val = cpu.get_loc_val(*src_loc)
    cpu.set_loc_val(*dst_loc, val)

def handle_add(cpu, dst_loc, src_loc):
    dst_val = cpu.get_loc_val(*dst_loc)
    src_val = cpu.get_loc_val(*src_loc)
    u_res = dst_val + src_val
    res = u_res & 0xFF
    cf = 1 if u_res > 0xFF else 0
    signed_d = dst_val - 256 if dst_val & 0x80 else dst_val
    signed_s = src_val - 256 if src_val & 0x80 else src_val
    signed_r = signed_d + signed_s
    of = 1 if signed_r > 127 or signed_r < -128 else 0
    cpu.set_flags(res, cf, of)
    cpu.set_loc_val(*dst_loc, res)

def handle_sub(cpu, dst_loc, src_loc):
    dst_val = cpu.get_loc_val(*dst_loc)
    src_val = cpu.get_loc_val(*src_loc)
    u_res = dst_val - src_val
    res = u_res & 0xFF
    cf = 1 if dst_val < src_val else 0
    signed_d = dst_val - 256 if dst_val & 0x80 else dst_val
    signed_s = src_val - 256 if src_val & 0x80 else src_val
    signed_r = signed_d - signed_s
    of = 1 if signed_r > 127 or signed_r < -128 else 0
    cpu.set_flags(res, cf, of)
    cpu.set_loc_val(*dst_loc, res)

def handle_cmp(cpu, dst_loc, src_loc):
    dst_val = cpu.get_loc_val(*dst_loc)
    src_val = cpu.get_loc_val(*src_loc)
    u_res = dst_val - src_val
    res = u_res & 0xFF
    cf = 1 if dst_val < src_val else 0
    signed_d = dst_val - 256 if dst_val & 0x80 else dst_val
    signed_s = src_val - 256 if src_val & 0x80 else src_val
    signed_r = signed_d - signed_s
    of = 1 if signed_r > 127 or signed_r < -128 else 0
    cpu.set_flags(res, cf, of)

def handle_and(cpu, dst_loc, src_loc):
    dst_val = cpu.get_loc_val(*dst_loc)
    src_val = cpu.get_loc_val(*src_loc)
    res = dst_val & src_val
    cpu.set_flags(res, logical=True)
    cpu.set_loc_val(*dst_loc, res)

def handle_or(cpu, dst_loc, src_loc):
    dst_val = cpu.get_loc_val(*dst_loc)
    src_val = cpu.get_loc_val(*src_loc)
    res = dst_val | src_val
    cpu.set_flags(res, logical=True)
    cpu.set_loc_val(*dst_loc, res)

def handle_inc(cpu, dst_loc):
    val = cpu.get_loc_val(*dst_loc)
    res = (val + 1) & 0xFF
    cf = 1 if val == 0xFF else 0
    signed = val - 256 if val & 0x80 else val
    signed_r = signed + 1
    of = 1 if signed_r > 127 or signed_r < -128 else 0
    cpu.set_flags(res, cf, of)
    cpu.set_loc_val(*dst_loc, res)

def handle_dec(cpu, dst_loc):
    val = cpu.get_loc_val(*dst_loc)
    res = (val - 1) & 0xFF
    cf = 1 if val == 0 else 0
    signed = val - 256 if val & 0x80 else val
    signed_r = signed - 1
    of = 1 if signed_r > 127 or signed_r < -128 else 0
    cpu.set_flags(res, cf, of)
    cpu.set_loc_val(*dst_loc, res)

def handle_not(cpu, dst_loc):
    val = cpu.get_loc_val(*dst_loc)
    res = (~val) & 0xFF
    cpu.set_flags(res, logical=True)
    cpu.set_loc_val(*dst_loc, res)

def handle_shr(cpu, dst_loc):
    val = cpu.get_loc_val(*dst_loc)
    cf = val & 0x01
    res = (val >> 1) & 0xFF
    of = (val >> 7) & 0x01
    cpu.set_flags(res, cf, of)
    cpu.set_loc_val(*dst_loc, res)

def handle_shl(cpu, dst_loc):
    val = cpu.get_loc_val(*dst_loc)
    cf = (val >> 7) & 0x01
    res = (val << 1) & 0xFF
    of = cf ^ ((res >> 7) & 0x01)
    cpu.set_flags(res, cf, of)
    cpu.set_loc_val(*dst_loc, res)

class CPU:
    def __init__(self, mem, labels):
        self.mem = list(mem)
        self.labels = labels
        self.A = 0
        self.B = 0
        self.I = 0
        self.FLAGS = 0
        self.PC = 0
        self.program_end = 0

    def get_flag(self, flag):
        masks = {'OF': 7, 'CF': 6, 'ZF': 5, 'PF': 4, 'SF': 3}
        return (self.FLAGS >> masks[flag]) & 1

    def set_flag(self, flag, val):
        masks = {'OF': 0x80, 'CF': 0x40, 'ZF': 0x20, 'PF': 0x10, 'SF': 0x08}
        mask = masks[flag]
        if val:
            self.FLAGS |= mask
        else:
            self.FLAGS &= ~mask

    def set_flags(self, res, cf=0, of=0, logical=False):
        self.set_flag('ZF', 1 if res == 0 else 0)
        self.set_flag('SF', 1 if (res & 0x80) != 0 else 0)
        self.set_flag('PF', 1 if bin(res).count('1') % 2 == 0 else 0)
        self.set_flag('CF', cf if not logical else 0)
        self.set_flag('OF', of if not logical else 0)

    def get_loc_val(self, loc_type, loc_val):
        if loc_type == 'reg':
            return getattr(self, loc_val)
        elif loc_type == 'ind_i':
            return self.mem[self.I]
        elif loc_type == 'const':
            return loc_val
        elif loc_type == 'dir':
            return self.mem[loc_val]
        raise ValueError("Invalid loc")

    def set_loc_val(self, loc_type, loc_val, val):
        val &= 0xFF
        if loc_type == 'reg':
            setattr(self, loc_val, val)
        elif loc_type == 'ind_i':
            self.mem[self.I] = val
        elif loc_type == 'dir':
            self.mem[loc_val] = val
        else:
            raise ValueError("Invalid set loc")

    def run(self):
        while self.PC < self.program_end:
            self.step()

    def step(self):
        instr_byte = self.mem[self.PC]
        self.PC += 1
        if instr_byte == 0xFF:
            return  # nop
        if 0xA0 <= instr_byte <= 0xA5:
            addr = self.mem[self.PC]
            self.PC += 1
            cond_code = instr_byte - 0xA0
            take = [True, self.get_flag('ZF'), self.get_flag('SF'), self.get_flag('CF'), self.get_flag('OF'), self.get_flag('PF')][cond_code]
            if take:
                self.PC = addr
            return
        op = instr_byte >> 4
        mode = instr_byte & 0xF
        is_unary = op in [0x3, 0x4, 0x7, 0x8, 0x9]
        if is_unary:
            dst_loc, _ = UNARY_MODES[mode]
            src_loc = None
        else:
            dst_loc, src_loc = MODES[mode]
            has_extra = dst_loc[1] == 'extra' or (src_loc and src_loc[1] == 'extra')
            extra = self.mem[self.PC] if has_extra else None
            if has_extra:
                self.PC += 1
            if dst_loc[1] == 'extra':
                dst_loc = (dst_loc[0], extra)
            if src_loc and src_loc[1] == 'extra':
                src_loc = (src_loc[0], extra)
        if is_unary:
            UNARY_HANDLERS[op](self, dst_loc)
        else:
            BINARY_HANDLERS[op](self, dst_loc, src_loc)

    def regs(self):
        return f"A={self.A:02X}H B={self.B:02X}H I={self.I:02X}H PC={self.PC:02X}H"

    def flags(self):
        return f"OF={self.get_flag('OF')} CF={self.get_flag('CF')} ZF={self.get_flag('ZF')} PF={self.get_flag('PF')} SF={self.get_flag('SF')}"

BINARY_HANDLERS = {
    0x0: handle_add,
    0x1: handle_sub,
    0x2: handle_cmp,
    0x5: handle_and,
    0x6: handle_or,
    0xB: handle_mov,
}

UNARY_HANDLERS = {
    0x3: handle_inc,
    0x4: handle_dec,
    0x7: handle_not,
    0x8: handle_shr,
    0x9: handle_shl,
}