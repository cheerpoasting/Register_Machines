#####
#
#       A basic version of a bytecode compiler. It reads from an instruction file.
#       The program should:
#           - Accept an arbitrary number of registers.
#           - Support labels and comments.
#           - Support the following commands: add, subtract, multiply, divide, move,  jump_if, halt.
#           - Support the following logical operator: not, greater than, less than.
#       The program should end by saving a bytestream in the format ".bytestream".
#
#####

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import utils.open_file as open_file

##### Important Dictionaries and Lists

OPCODES = {
    "ADD": 1, # 6
    "SUB": 2,
    "MULT": 3,
    "DIV": 4,
    "MOV": 5,
    "JUMP_IF": 6, # 7
    "HALT": 7 # 1
}

# ADD ex. add 4 r1 r2 [ADD IMM 4 REG r1_idx r2_indx]



OPTYPE = {
    "IMM": 0,
    "REG": 1
}

FLAG = {
    "IS": 0,
    "NOT": 1
}

CONDITIONS = {
    "EQ": 0,
    "GT": 1,
    "LT": 2
}
labels = {}

def seperate_lines(contents):
    lines = []
    for line in contents.splitlines():
        if line:
            lines.append(line)
    return lines

def assign_registers(lines):

    registers = []
    
    for line in lines:
        if line.startswith("register"):
            register_list = line.split()
            for item in register_list:
                if item == "register":
                    pass
                else:
                    registers.append(item)

    if not registers:
        print("No register found")
        exit(404) # not found

    return registers

def assign_label_indexes(lines):

    labels = {}
    index = 0

    for line in lines:
        if line.startswith("add"):
            index += 6
        elif line.startswith("subtract"):
            index += 6
        elif line.startswith("multiply"):
            index += 6
        elif line.startswith("divide"):
            index += 6
        elif line.startswith("move"):
            index += 6
        elif line.startswith("jump_if"):
            index += 7
        elif line.startswith("register"):
            pass
        elif line.startswith("halt"):
            index += 1
        elif line.startswith("_"):
            labels[line] = index
        else:
            print(f"UNKNOWN COMMAND {line}")
            exit(403)

    return labels

def emit_basic_math(bytecode, registers, instruction_list, opcode, name):
    for item in instruction_list:
        if item == name:
            bytecode.append(opcode)
        elif item.isdigit():
            if item == instruction_list[-1]:
                print(f"{instruction_list}: final argument must be register")
                exit(403)
            else:
                bytecode.append(OPTYPE["IMM"])
                bytecode.append(int(item))
        elif item in registers:
            if len(instruction_list) == 4 and item == instruction_list[-1]:
                bytecode.append(registers.index(item))
            elif len(instruction_list) == 3 and item == instruction_list[-1]:
                bytecode.append(OPTYPE["REG"])
                bytecode.append(registers.index(item))
                bytecode.append(registers.index(item))
            else:
                bytecode.append(OPTYPE["REG"])
                bytecode.append(registers.index(item))
        else:
            print(f"INVALID {name.upper()}: {instruction_list}")
def emit_bytecode(lines, labels, registers):
    bytecode = []

    for line in lines:
        if line.startswith("add"):
            emit_basic_math(bytecode, registers, line.split(), OPCODES["ADD"], "add")
        elif line.startswith("subtract"):
            emit_basic_math(bytecode, registers, line.split(), OPCODES["SUB"], "subtract")
        elif line.startswith("multiply"):
            emit_basic_math(bytecode, registers, line.split(), OPCODES["MULT"], "multiply")
        elif line.startswith("divide"):
            emit_basic_math(bytecode, registers, line.split(), OPCODES["DIV"], "divide")
        elif line.startswith("move"):
            emit_basic_math(bytecode, registers, line.split(), OPCODES["MOV"], "move")
        elif line.startswith("jump_if"):
            jump_list = line.split()
            bytecode.append(OPCODES["JUMP_IF"])
            if not jump_list[1].isdigit():
                bytecode.append(registers.index(jump_list[1]))
            else:
                print(f"{line}: First argument of jump cannot be a number")
                exit(403)
            if len(jump_list) == 4:
                bytecode.append(FLAG["IS"])
                bytecode.append(CONDITIONS["EQ"])
                if not jump_list[2].isdigit():
                    bytecode.append(OPTYPE["REG"])
                    bytecode.append(registers.index(jump_list[2]))
                else:
                    bytecode.append(OPTYPE["IMM"])
                    bytecode.append(int(jump_list[2]))
                bytecode.append(labels[jump_list[3]])
            if len(jump_list) == 5:
                if jump_list[2] == "not":
                    bytecode.append(FLAG["NOT"])
                    bytecode.append(CONDITIONS["EQ"])
                elif jump_list[2] == "gt":
                    bytecode.append(FLAG["IS"])
                    bytecode.append(CONDITIONS["GT"])
                elif jump_list[2] == "lt":
                    bytecode.append(FLAG["IS"])
                    bytecode.append(CONDITIONS["LT"])
                else:
                    print(f"{line}: Invalid length")
                if not jump_list[3].isdigit():
                    bytecode.append(OPTYPE["REG"])
                    bytecode.append(registers.index(jump_list[3]))
                else:
                    bytecode.append(OPTYPE["IMM"])
                    bytecode.append(int(jump_list[3]))
                bytecode.append(labels[jump_list[4]])
            if len(jump_list) == 6:
                bytecode.append(FLAG["NOT"])
                if jump_list[3] == "gt":
                     bytecode.append(CONDITIONS["GT"])
                elif jump_list[3] == "lt":
                    bytecode.append(CONDITIONS["LT"])
                if not jump_list[4].isdigit():
                    bytecode.append(OPTYPE["REG"])
                    bytecode.append(registers.index(jump_list[4]))
                else:
                    bytecode.append(OPTYPE["IMM"])
                    bytecode.append(int(jump_list[4]))
                bytecode.append(labels[jump_list[5]])
        elif line.startswith("register"):
            pass
        elif line.startswith("halt"):
            bytecode.append(OPCODES["HALT"])
        elif line.startswith("_"):
            pass
        elif line.startswith("#"):
            pass
        else:
            print(f"UNKNOWN COMMAND {line}")
            exit(403)

    return bytecode

def give_bytecode(file_name):
    target_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), file_name)
    contents = open_file.openfile(target_file)
    lines = seperate_lines(contents)
    registers = assign_registers(lines)
    labels = assign_label_indexes(lines)
    bytecode = emit_bytecode(lines, labels, registers)
    return (bytecode, registers)

if __name__ == "__main__":
    target_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "testing.txt")
    contents = open_file.openfile(target_file)
    lines = seperate_lines(contents)
    registers = assign_registers(lines)
    labels = assign_label_indexes(lines)
    bytecode = emit_bytecode(lines, labels, registers)
    print(bytecode)