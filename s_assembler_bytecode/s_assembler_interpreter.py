#####
#
#       A basic version of a bytecode vm. It reads from a bytestream.
#       The program should:
#           - Accept a bytestream and list of registers.
#           - Support the following commands: add, subtract, multiply, divide, move,  jump_if, halt.
#           - Support the following logical operator: not, greater than, less than.
#       The program should end by displaying the final state of the registers.
#
#####

import s_assembler_bytecode as compiler

class Register:
    def __init__(self, name, index):
        self.name = name
        self.index = index
        self.value = 0

    def __repr__(self):
        return f"Register \"{self.name}\" at  index {self.index} = {self.value}"

def init_registers(registers):
    register_list = [Register(name, i) for i, name in enumerate(registers)]
    return register_list

# The dispactch table reads an opcode, then calls the correct function to parse it
# It uses a decorator to fill itself automatically
dispatch = {}

# The decorator that fills the dispatch table
def register_op_code(op_code):
    def add_to_dispatch(handler_function):
        dispatch[op_code] = handler_function
        # that is add an entry to "dispatch" with the key "opcode" and the value "handler_function" 
        return handler_function
    return add_to_dispatch

def common_arithmetic(bytecode, instruction_index, registers):
    if bytecode[instruction_index+1] == 0: # if int
        primary_value = bytecode[instruction_index+2]
    else: # register
        primary_value = registers[bytecode[instruction_index+2]].value
    if bytecode[instruction_index+3] == 0:
        secondary_value = bytecode[instruction_index+4]
    else:
        secondary_value = registers[bytecode[instruction_index+4]].value
    target_register = registers[bytecode[instruction_index+5]]
    return primary_value, secondary_value, target_register 

@register_op_code(1) # this is the decorator adding "op_add" to the dispatch table with the key "1" (the actual opcode)
def op_add(bytecode, instruction_index, registers):
    primary_value, secondary_value, target_register = common_arithmetic(bytecode, instruction_index, registers)
    target_register.value = primary_value + secondary_value
    instruction_index += 6
    return instruction_index

@register_op_code(2) 
def op_sub(bytecode, instruction_index, registers):
    primary_value, secondary_value, target_register = common_arithmetic(bytecode, instruction_index, registers)
    target_register.value = primary_value - secondary_value
    instruction_index += 6
    return instruction_index

@register_op_code(3) 
def op_mult(bytecode, instruction_index, registers):
    primary_value, secondary_value, target_register = common_arithmetic(bytecode, instruction_index, registers)
    target_register.value = primary_value * secondary_value
    instruction_index += 6
    return instruction_index

@register_op_code(4) 
def op_div(bytecode, instruction_index, registers):
    primary_value, secondary_value, target_register = common_arithmetic(bytecode, instruction_index, registers)
    target_register.value = primary_value / secondary_value
    instruction_index += 6
    return instruction_index

@register_op_code(5) 
def op_mov(bytecode, instruction_index, registers):
    primary_value, secondary_value, target_register = common_arithmetic(bytecode, instruction_index, registers)
    if bytecode[instruction_index+1] == 1: # if reg
        registers[bytecode[instruction_index+2]]. value = 0
    target_register.value = primary_value
    instruction_index += 6
    return instruction_index

@register_op_code(6) 
def op_jump_if(bytecode, instruction_index, registers):
    instruction_index += 7
    return instruction_index

@register_op_code(7) 
def op_halt(bytecode, instruction_index, registers):
    print(f"Program ended successfully: \n{registers}") # program ended successfully
    exit(0)

def parse_and_run(bytecode, registers):

    instruction_index = 0 # pc/program counter
    while instruction_index < len(bytecode):
        opcode = bytecode[instruction_index]
        instruction_index = dispatch[opcode](bytecode, instruction_index, registers)

if __name__ == "__main__":
    bytecode, registers = compiler.give_bytecode("testing.txt")
    registers = init_registers(registers)
    #print({k: v.__name__ for k, v in dispatch.items()}) #checks dispatch table created correctly
    parse_and_run(bytecode, registers)

