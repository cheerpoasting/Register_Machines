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

# ADD ex. add 4 r1 r2 [ADD IMM 4 REG r1_idx r2_indx]
# JUMP_IF ex jump_if r1 not gt 6 _addition [jump_if reg r1_idx not gt imm 6 _addition_idx]

import re
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import utils.open_file as open_file

OPCODES = {
    "ADD": 1,
    "SUB": 2,
    "MULT": 3,
    "DIV": 4,
    "MOV": 5,
    "JUMP_IF": 6,
    "HALT": 7
}

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

registers = {}
labels = {}


if __name__ == "__main__":
    target_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "testing.txt")
    contents = open_file.openfile(target_file)
    print(contents)