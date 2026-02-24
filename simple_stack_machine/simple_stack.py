#####
#
#       A simple program to model a stack machine. It reads from an instruction file.
#       The program read reverse polish notation. It should accept the following commands: implicit push (any positive integer), add, subtract.
#
#####

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import utils.open_file as open_file

stack = []

def stack_push(item):
    stack.append(item)

def stack_pop():
    return stack.pop()

def stack_add():
    argument_a = int(stack_pop())
    argument_b = int(stack_pop())
    result = argument_a + argument_b
    if result < 1:
        result = 0
    stack_push(result)

def stack_subtract():
    argument_a = int(stack_pop())
    argument_b = int(stack_pop())
    result = argument_b - argument_a
    stack_push(result)

def parse_contents(contents):
    instruction_list = contents.split()
    for instruction in instruction_list:
        if instruction.isdigit():
            stack_push(instruction)
        elif instruction == "+":
            stack_add()
        elif instruction == "-":
            stack_subtract()
        else:
            raise ValueError(f"UNKNOWN COMMAND {instruction}")
    
if __name__ == "__main__":
    target_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "subtraction.txt")
    contents = open_file.openfile(target_file)
    parse_contents(contents)
    print(f"Final Stack: {stack}")