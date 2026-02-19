#####
#
#       A simple program to model a register machine.
#       The program should read an instruction file, use 2 registers, use an instruction pointer, recognize 4 commands (increment, decrement, jump if 0, and halt), and return results.
#
#####

##### PROGRAM OVERVIEW

# Create class for instruction tokens
# Open Instruction File
# Create Instruction Tokens
# Initalize the 2 registers named in the instruction file
# Execute the 4 valid commands as found in the instruction file
# Return final state of the two registers

import os

##### INSTRUCTION TOKEN CLASS

class Instruction_Token:
    def __init__(self, line, column, text):
        self.line = line
        self.column = column
        self.text = text
    
    def __repr__(self):
        return f"{self.text} L{self.line}C{self.column}"

##### OPEN FILE
def openfile(file_name): 

    if os.path.isdir(file_name):
        print(f"Error: '{os.path.basename(file_name)}' is a directory, not a file.")
        exit(400)  # 400 = Bad Request

    allowed_extensions = (".txt",)
    if not file_name.endswith(allowed_extensions):
        print(f"Error: '{os.path.basename(file_name)}' is not a supported file type, such as {allowed_extensions}.")
        exit(415) # invalid media type

    try: 
        if os.path.getsize(file_name) == 0:
            print(f"Error: '{os.path.basename(file_name)}' is empty.")
            exit(204) # 204 == No Content

        with open(file_name, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        print(f"Error: '{os.path.basename(file_name)}' not found.")
        exit(404) # 404 = File Not Found
    except UnicodeDecodeError:
        print(f"Error: '{os.path.basename(file_name)}' is not valid UTF-8.")
        exit(415) # 415 = Unsupported Media Type
    except PermissionError:
        print(f"Error: '{os.path.basename(file_name)}' cannot be read (permission denied).")
        exit(403)  # 403 = Forbidden

##### GENERATE INSTRUCTION TOKENS
def create_instructiontokens(instruction_set):

    token_list = []
    instruction_line = 1
    instruction_column = 1
    instruction_text = ""

    for character in instruction_set:
        if character in (" ", "\n"): # If you hit a space or newline
            if instruction_text: # This will be "false" if the instruction text is empty
                token = Instruction_Token(instruction_line, instruction_column - len(instruction_text), instruction_text)
                token_list.append(token)
                instruction_text = "" # Resets instruction text contents
            if character == '\n':
                instruction_line += 1
                instruction_column = 1
            else: # Basically, if space
                instruction_column += 1
        else: 
            instruction_text += character
            instruction_column += 1

    if instruction_text: # if last token
        token_list.append(Instruction_Token(instruction_line, instruction_column - len(instruction_text), instruction_text))

    return token_list
def main():
    instruction_set = openfile("register_program.txt")
    token_list = create_instructiontokens(instruction_set)
    print(token_list)

if __name__ == "__main__":
    main()