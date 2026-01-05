MODES = {
    0x0: (('reg', 'A'),     ('reg', 'B')),
    0x1: (('reg', 'B'),     ('reg', 'A')),
    0x2: (('reg', 'A'),     ('reg', 'I')),
    0x3: (('reg', 'I'),     ('reg', 'A')),
    0x4: (('reg', 'A'),     ('ind_i', None)),
    0x5: (('ind_i', None),  ('reg', 'A')),
    0x6: (('reg', 'A'),     ('const', 'extra')),
    0x7: (('reg', 'B'),     ('const', 'extra')),
    0x8: (('reg', 'I'),     ('const', 'extra')),
    0x9: (('ind_i', None),  ('const', 'extra')),
    0xA: (('reg', 'A'),     ('dir', 'extra')),
    0xB: (('reg', 'B'),     ('dir', 'extra')),
    0xC: (('dir', 'extra'), ('reg', 'A')),
    0xD: (('dir', 'extra'), ('reg', 'B')),
}

UNARY_MODES = {
    0x0: (('reg', 'A'), None),
    0x1: (('reg', 'B'), None),
    0x2: (('reg', 'I'), None),
    0x4: (('ind_i', None), None),
}

OPCODES = {
    'add': 0x0,
    'sub': 0x1,
    'cmp': 0x2,
    'inc': 0x3,
    'dec': 0x4,
    'and': 0x5,
    'or' : 0x6,
    'not': 0x7,
    'shr': 0x8,
    'shl': 0x9,
    'mov': 0xB,
}

JUMP_CODES = {
    'jmp': 0xA0,
    'jz' : 0xA1,
    'js' : 0xA2,
    'jc' : 0xA3,
    'jo' : 0xA4,
    'jp' : 0xA5,
}

BINARY_MNEMONS = ['add', 'sub', 'cmp', 'and', 'or', 'mov']
UNARY_MNEMONS = ['inc', 'dec', 'not', 'shr', 'shl']