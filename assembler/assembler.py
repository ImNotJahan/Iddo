from parser import parse

from util import set_bit

# opcodes = {instruction: (machine code, number of arguments, is jump operation)}
opcodes = {
    "ADD": (0, 2), "SUB": (1, 2), "MUL": (2, 2), "NEG": (3, 1), "NOT": (4, 1), 
    "AND": (5, 2), "OR": (6, 2), "XOR": (7, 2), "SHL": (8, 1), "SHR": (9, 1), 
    "MOVE": (10, 1), "DIV": (11, 2), "MOD": (12, 2), 

    "SAVE": (16, -1), "LOAD": (17, -1), "PUSH": (18, 1), "POP": (19, 0), "STK": (20, -1), 

    "EQ": (32, 2, True), "NEQ": (33, 2, True), "LT": (34, 2, True), "LTE": (35, 2, True), "GT": (36, 2, True), 
    "GTE": (37, 2, True), "JUMP": (38, 0, True), "NEVER": (39, 0, True), "CALL": (40, 0, True), "RET": (41, 0, True), 
    }
without_output = ["RET"] # rarely, opcodes will not expect an output to be specified

locations = {
    "R0": 0, "R1": 1, "R2": 2, "R3": 3, "R4": 4, 
    "R5": 5, "R6": 6, "R7": 7,
    "RAM": 8, "ADR": 9, "COUNTER": 10, "INPUT": 11,
    "OUTPUT": 11, "NULL": 12 
    }

def assemble(file) -> list[int]:
    assembly_code = parse(file)
    machine_code = []

    # labels = {"label": [line_number, [places referencing this label]]}
    labels = {}
    # constants = {"constant": value}
    constants = {}

    # returns the current position in the machine code
    def current_pos() -> int:
        return len(machine_code)
    
    def use_label(label):
        if label in labels:
            labels[label][1].append(current_pos())
        else:
            labels[label] = [-1, [current_pos()]]
        machine_code.append(labels[label][0])

    for line in assembly_code:
        if len(line) == 0:
            raise ValueError("Expected line in assembly code to not be empty. This means the parser is doing something wrong.", assembly_code)
        
        if line[0] == "label":
            if len(line) != 2:
                raise Exception("Expected label declaration to have two tokens", line)

            label = line[1]

            if label in labels:
                pos = current_pos()
                labels[label][0] = pos

                for ref in labels[label][1]:
                    machine_code[ref] = pos
        elif line[0] == "const":
            if len(line) != 3:
                raise Exception("Expected constant declaration to have three tokens", line)
            if not line[1][0].isalpha():
                raise Exception("Constant must start with letter")
            if not line[1].islower():
                raise Exception("Constant must be lowercase")

            value = line[2]

            if value in locations:
                constants[line[1]] = value
            elif value.isnumeric():
                constants[line[1]] = int(value)
            else:
                raise ValueError("Expected location or integer literal for constant value")
        # if it's not a label or const, it's an operation
        else:
            opcode = line[0]
            # or at least should be
            if opcode not in opcodes:
                raise ValueError("Line does not start with a valid instruction", opcode)
            
            opcode_pos = current_pos()
            machine_code.append(opcodes[opcode][0])
            arg_count = opcodes[opcode][1]

            if opcode in without_output:
                if len(line) != 1 + arg_count:
                    raise Exception("Expected {} to have {} tokens".format(opcode, 1 + arg_count), line)
            else:
                if len(line) != 2 + arg_count:
                    raise Exception("Expected {} to have {} tokens".format(opcode, 2 + arg_count), line)
            
            for i in range(1, arg_count + 1):
                arg = line[i]

                if arg in locations:
                    machine_code.append(locations[arg])
                elif arg.isnumeric():
                    machine_code.append(int(arg))
                    machine_code[opcode_pos] = set_bit(machine_code[opcode_pos], 8 - i)
                elif arg in constants:
                    const = constants[arg]
                    if type(const) is int:
                        machine_code.append(constants[arg])
                        machine_code[opcode_pos] = set_bit(machine_code[opcode_pos], 8 - i)
                    elif type(const) is str:
                        machine_code.append(locations[const])
                else:
                    raise ValueError("Expected argument to be integer literal, constant name, or location", arg)
            
            if opcode in without_output:
                continue
            
            final_token = line[-1]
            if len(opcodes[opcode]) == 3: # is compare operation
                if final_token in labels or (final_token[0].isalpha() and final_token.islower()):
                    use_label(final_token)
                elif final_token.isnumeric():
                    machine_code.append(int(final_token))
                    
                else:
                    raise ValueError("Expected label or integer literal for comparison to jump to", final_token)
            else:
                if final_token in locations:
                    machine_code.append(locations[final_token])
                elif final_token in constants:
                    machine_code.append(locations[constants[final_token]])
                else:
                    raise ValueError("Expected location to pipe output to", final_token)
    
    return machine_code

if(__name__ == "__main__"):
    machine_code = assemble(open(input("File to assemble: ")))
    print(" ".join(map(str, machine_code)))