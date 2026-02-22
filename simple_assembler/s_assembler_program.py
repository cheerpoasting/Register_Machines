#####
#
#       A basic version of an assembler. It reads from an instruction file.
#       The program should:
#           - Accept an arbitrary number of registers.
#           - Support labels and comments.
#           - Support the following commands: increment, decrement, move, jump_if_not_zero, halt.
#       The program should end by returning the final status of all registers created.
#
#####

import re
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import utils.open_file as open_file

def create_instructions(file_contents):
    instruction_dictionary ={}

    for i, line in enumerate(file_contents.splitlines(), start = 1):
        instruction_dictionary[i] = line

    return instruction_dictionary

def initialize_registers(instructions):
    registers = {}

    for line in instructions:
        if re.match(r"register", instructions[line]):
            register_list = instructions[line].split()
            for item in register_list:
                if item == "register":
                    pass
                else:
                    registers[item] = 0

    if not registers:
        print("No register found")
        exit(404) # not found

    return registers

def initalize_labels(instructions):
    labels = {}
    
    for line in instructions:
        if re.match(r"_", instructions[line]):
            labels[instructions[line]] = line
    
    return labels
    
def run_instructions(registers, labels, instructions):
    i = 1
    while i in instructions:
        if re.match(r"register", instructions[i]):
            i += 1
        elif re.match(r"increment", instructions[i]):
            increment_instructions = instructions[i].split()
            amount = increment_instructions [1]
            target_register = increment_instructions[2]
            if amount.isdigit():
                registers[target_register] += int(amount)
                i += 1
            else:
                registers[target_register] += registers[amount]
                i += 1
        elif re.match(r"decrement", instructions[i]):
            decrement_instructions = instructions[i].split()
            target_amount = decrement_instructions[1]
            target_register = decrement_instructions[2]
            if registers[target_register] > 0:
                registers[target_register] -= int(target_amount)
                i += 1
            else:
                registers[target_register] = 0
                i += 1
        elif re.match(r"move", instructions[i]):
            move_instructions = instructions[i].split()
            amount = move_instructions[1]
            target_register = move_instructions [2]
            if amount.isdigit():
                registers[target_register] = int(amount)
            else:
                registers[target_register] =registers[amount]
                registers[amount] = 0
            i +=1
        elif re.match(r"#", instructions[i]):
            i += 1
        elif re.match(r"_", instructions[i]):
            i += 1
        elif not instructions[i].strip():
            i += 1
        elif re.match(r"jump_if_not_zero", instructions[i]):
            jump_instructions = instructions[i].split()
            if registers[jump_instructions[1]] != 0:
                i = int(labels[jump_instructions[2]])
            else:
                i += 1
        elif re.match(r"halt", instructions[i]):
            break
        else: 
            print(f"Unknown command {instructions[i]}")
            exit(403)
    return registers

if __name__ == "__main__":
    target_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "factorial.txt")
    contents = open_file.openfile(target_file)
    instructions = create_instructions(contents)
    registers = initialize_registers(instructions)
    labels = initalize_labels(instructions)
    registers = run_instructions(registers, labels,  instructions)
    print(registers)