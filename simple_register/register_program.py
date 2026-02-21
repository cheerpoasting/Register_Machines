#####
#
#       A simple program to model a register machine. It reads from an instruction file.
#       The program should create an arbitrary number of registers and excecute 4 commands (increment, decrement, jump if not 0, halt).
#       The program should end by returning the final status of all registers created.
#
#####

import re
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import utils.open_file as open_file

def create_instruction_dictionary(instruction_content):

    instruction_dictionary = {}

    for i, line in enumerate(instruction_content.splitlines(), start=1):
        # variable.splitlines() is needed because we are going from the contents of a variable instead of directly from the file
        # splitlines() will automatically treat each line (ending in \n) as something to iterate over 
        # start = 1 tells the enumerator to treat the first item as "1" instead of "0
        instruction_dictionary[i] = line # store as dictionary entry

    return instruction_dictionary

def initialize_registers(instructions):
    registers = {}

    for line in instructions:
        if re.match(r"register", instructions[line]):
            # re.match means do a regex match for "register" at the start of the string
            register_list = instructions[line].split()
            # here, we turn the register declaration into a list by splitting on whitespace
            for item in register_list:
                if item == "register":
                    pass # we want to ignore this line
                else:
                    registers[item] = 0
                    # here we are adding each register to the register dictionary and initalizing with a value of 0
            return registers
    
    if not registers:
        print("No register found")
        exit(404) # not found

def simulate_registers(registers, instructions):
    i = 1
    instructions_run = 0
    while i in instructions: # as long as i is a valid key in instructions
        if re.match(r"register", instructions[i]):
            i += 1 # if value starts with "register", go to next pair
        elif not instructions[i]:
            i += 1 # if value is empty, go to next pair
        elif re.match(r"#", instructions[i]):
            i+=1
        elif re.match(r"increment", instructions[i]):
            increment_instruction = instructions[i].split() # turn instruction into list
            argument = increment_instruction[1] # grab argument
            registers[argument] += 1 # use argument to increment dictionary entry
            i += 1
            instructions_run += 1
        elif re.match(r"decrement", instructions[i]):
            decrement_instruction = instructions[i].split()
            argument = decrement_instruction[1]
            if registers[argument] > 0:
                registers[argument] -= 1
            else:
                registers[argument] = 0
            i += 1
            instructions_run += 1

        elif re.match(r"jump_if_not_zero", instructions[i]):
            jump_instruction = instructions[i].split()
            target_register = jump_instruction[1] # register to check
            target_line = jump_instruction[2] # line to jump to if true
            if registers[target_register] != 0:
                i = int(target_line) # if register is not 0, go to target line
            else:
                i += 1 # if register is 0, continue to next instruction
        elif instructions[i] == "halt":
            instructions_run += 1
            print(instructions_run)
            break
        else:
            print(f"UNKNOWN COMMAND {instructions[i]} on line {i}")
            exit(403) # forbidden
    return registers

if __name__ == "__main__":
    target_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "factorial_simplified.txt")
    contents = open_file.openfile(target_file)
    instructions = create_instruction_dictionary(contents)
    registers = initialize_registers(instructions)
    result = simulate_registers(registers, instructions)
    print(result)


