# Layout: [opcode, input, outputs, cost (if needed)]
# Most operations on the Adamnite Protocol cost 1 micali (1/10^14 of one NITE)
# unless otherwise specified.
# This goes back to the smart contract fees of deployment. Being the same as a
# regular transaction, a smart contract's fee is ultimately specified in net
# ATE, which is like gas on ETH.


# Layout is inspired by PyEthereum's Serenity Implementation
opcodes = {
    0x00: ['TERM', 0, 0, 0],
    0x01: ['+', 2, 1],
    0x02: ['-', 2, 1],
    0x03: ['*', 2, 1, 2],
    0x04: ['/', 2, 1, 2],
    0x05: ['MOD', 2, 1, 2],
    0x06: ['MOD_ADD', 3, 1, 3],
    0x07: ['MOD_MUL', 3, 1, 3],
    0x08: ['POW', 2, 1, 3],
    0x09: ['SIGNED_DIV', 2, 1, 2],
    0x0a: ['SIGNED_MOD', 2, 1, 2],
    0x0b: ['SIGNED_POW', 2, 1, 3],
    0x10: ['<', 2, 1],
    0x11: ['>', 2, 1],
    0x12: ['<=', 2, 1],
    0x13: ['>=', 2, 1],
    0x14: ['==', 2, 1],
    0x15: ['&&', 2, 1],
    0x16: ['||', 2, 1],
    0x17: ['^', 2, 1],
    0x18: ['!', 1, 1],
    0x19: ['BYTE', 2, 1],
    0x1a: ['LEN', 1, 1],
    0x20: ['SHA256', 2, 1, 12],
    0x31: ['RECEIVER', 2, 1, 1],
}
