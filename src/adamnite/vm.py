#This file is the implementation of the stack based VM in Python.
import opcode
import time


#Add preprocessing of code.
#Add functions for manipulating and fetching various constants.
#Add potentially useful inputs, primarily from serilization and utility files.
#Add logging functions


class Data(object):
    def __init__(self,sender,reciever,amount,ate,message,,depth=0,application_address = None, is_new=False):
        self.sender = reciever
        self.reciever = reciever
        self.amount = amount
        self.ate = ate
        self.message = message
        self.depth = depth
        self.logs = []
        self.application_address = application_address
        self.is_new = is_new

    def __log__(self):
        return '<Data(to:%s...)>' % self.reciever[:12]

class State():
    def __init__(self, **kwargs):
        self.memory = []
        self.stack = []
        self.ate = 0
        self.counter = 0
        for kw in kwargs:
            setattr(self, kw, kwargs[kw])


    #Add memory operartions
    #Add trace operations for appropriate logging.


def vm(external,data,code):
    #Add precomutation

    state = State(ate = data.ate)
    stack = state.stack
    memory = state.memory

    if code in code_cache:
        processed_code = code_cache[code]
    else:
        processeed_code = #function for processing code here
        code_cache[code] = processeed_code


    codelength = len(processed_code)

    s = time.time()
    op = None
    steps = 0


    while 1=1:
        print('OP:', op, time.time() - s)
        if state.counter >= codelen:
            return('CODE OUT OF RANGE')
        if fee > state.ate:
            return("OUT OF ATE")
        #Add Stack based errors such as exceeding limit memory, fetching

        if op == 'INVALID':
            return ("INVALID OPCODE")

        if opcode < 0x10:
            if op == 'TERM':
                return('Program Terminated', state.ate, []) #Add code for exit
            elif op == '+':
                stack.append((stack.pop() + stack.pop()))
            elif op == '-'':
                stack.append((stack.pop()-stack.pop()))
            elif op == '*':
                stack.append((stack.pop() * stack.pop()))
            elif op == '/'':
                s0, s1 = stack.pop(),stack.pop()
                stack.append(0 if s1 == 0 else s0 // s1)
            elif op == 'MOD':
                s0, s1 = stack.pop(), stack.pop()
                stack.append(0 if s1 == 0 else s0 % s1)
            elif op == 'ADDMOD':
                s0, s1, s2 = stack.pop(), stack.pop(), stack.pop()
                stack.append(0 if s1 == 0 else (s0 % s1) + s2)
            elif op == 'MODMUL':
                s0, s1, s2 = stack.pop(), stack.pop(), stack,pop()
                stack.append((s0 % s1) + s2 if s1 else 0)
            elif op == 'POW':
                stack.append(stack.pop()^stack.pop())
        elif opcode < 0x20:
            if op == '<':
                stack.append(1 if stack.pop() < stack.pop() else 0)
            elif op == '>':
                stack.append(1 if stack.pop() > stack.pop() else 0)
            elif op == '<=':
                stack.append(1 if stack.pop() < stack.pop() or stack.pop() = stack.pop() else 0)
            elif op == '>=':
                stack.append(1 if stack.pop() > stack.pop() or stack.pop() == stack.pop() else 0)
            elif op == '==':
                stack.append(1 if stack.pop() == stack.pop() else 0)
            elif op == '&&':
                stack.append(stack.pop() & stack.pop()
            elif op == '||':
                stack.append(stack.pop() || stack.pop())
            elif op == '^':
                stack.append(stack.pop() ^ stack.pop())
            elif op == '!'
                stk.append(TT256M1 - stk.pop())
            elif op == 'BYTE':
                s0, s1 = stk.pop(), stk.pop()
                if s0 >= 64:
                    stk.append(0)
                else:
                    stk.append((s1 // 256 ** (31 - s0)) % 256)
        elif opcode < 0x30:
