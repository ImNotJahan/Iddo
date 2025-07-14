import numpy # I refuse to initialize such a large list for memory
from time import sleep

MEMORY_SIZE = 1000
OPCODE_BITMASK = 63

OPCODE_ARG_COUNT = {0: 3, 1: 3, 2: 3, 3: 2, 4: 2, 5: 3, 6: 3, 7: 3, 8: 2, 9: 2, 10: 2, 11: 3, 12: 3,
                    18: 2, 19: 1, 32: 3, 33: 3, 34: 3, 35: 3, 36: 3, 37: 3, 38: 1, 39: 1, 40: 1, 41: 0}

'''A virtual machine emulating an Iddo computer'''
class VM:
    ram = numpy.empty(MEMORY_SIZE, dtype=numpy.int16)
    counter = 0 # current position in the program
    registers = [0, 0, 0, 0, 0, 0, 0, 0]
    output = 0
    input = [] # queue
    ram_address = 0
    stack = []
    fn_stack = []

    def set_program(self, code: list[int]):
        self.program = code
    
    '''Run the currently loaded program. Waits delay amount of time between each cycle'''
    def run(self, delay=0.0):
        if self.program == None:
            return
        
        while self.cycle():
            sleep(delay)
    
    def cycle(self) -> bool:
        if self.counter >= len(self.program):
            return False
        
        instruction = self.program[self.counter]
        opcode = instruction & OPCODE_BITMASK
        firstArgIsLit = instruction >> 7 & 1
        secondArgIsLit = instruction >> 6 & 1
        argCount = OPCODE_ARG_COUNT.get(opcode, 0)

        if self.counter + argCount >= len(self.program):
            return False
        
        args = []

        if argCount >= 2:
            if firstArgIsLit:
                args.append(self.program[self.counter + 1])
            else:
                args.append(self.get_location_value(self.program[self.counter + 1]))
        if argCount >= 3:
            if secondArgIsLit:
                args.append(self.program[self.counter + 2])
            else:
                args.append(self.get_location_value(self.program[self.counter + 2]))
        if argCount >= 1:
            args.append(self.program[self.counter + argCount])
        
        self.counter += argCount + 1
        self.handle_operation(opcode, args)

        return True
    
    def get_location_value(self, location: int) -> int:
        if 0 <= location < 8:
            return self.registers[location]
        if location == 8:
            return self.ram[self.ram_address]
        if location == 9:
            return self.ram_address
        if location == 10:
            return self.counter
        if location == 11:
            return self.input.pop(0) if len(self.input) > 0 else 0
        return 0
    
    def set_location_value(self, location: int, value: int):
        if 0 <= location < 8:
            self.registers[location] = value
        elif location == 8:
            self.ram[self.ram_address] = value
        elif location == 9:
            self.ram_address = value
        elif location == 10:
            self.counter = value
        elif location == 11:
            self.output = value
            print(value)
    
    def jump_if(self, position: int, condition: bool):
        if condition:
            self.counter = position
    
    def handle_operation(self, opcode: int, args: list[int]):
        assert len(args) == OPCODE_ARG_COUNT.get(opcode, 0)

        match opcode:
            case 0:
                self.set_location_value(args[2], args[0] + args[1])
            case 1:
                self.set_location_value(args[2], args[0] - args[1])
            case 2:
                self.set_location_value(args[2], args[0] * args[1])
            case 3:
                self.set_location_value(args[1], -args[0])
            case 4:
                self.set_location_value(args[1], ~args[0])
            case 5:
                self.set_location_value(args[2], args[0] & args[1])
            case 6:
                self.set_location_value(args[2], args[0] | args[1])
            case 7:
                self.set_location_value(args[2], args[0] ^ args[1])
            case 8:
                self.set_location_value(args[2], args[0] << args[1])
            case 9:
                self.set_location_value(args[2], args[0] >> args[1])
            case 10:
                self.set_location_value(args[1], args[0])
            case 11:
                self.set_location_value(args[2], args[0] // args[1])
            case 12:
                self.set_location_value(args[2], args[0] % args[1])
            
            case 18:
                self.stack.append(args[0])
            case 19:
                self.set_location_value(args[0], self.stack.pop())
            
            case 32:
                self.jump_if(args[2], args[0] == args[1])
            case 33:
                self.jump_if(args[2], args[0] != args[1])
            case 34:
                self.jump_if(args[2], args[0] < args[1])
            case 35:
                self.jump_if(args[2], args[0] <= args[1])
            case 36:
                self.jump_if(args[2], args[0] > args[1])
            case 37:
                self.jump_if(args[2], args[0] >= args[1])
            case 38:
                self.counter = args[0]
            
            case 40:
                self.fn_stack.append(self.counter + 2)
                self.counter = args[0]
            case 41:
                self.counter = self.fn_stack.pop()

