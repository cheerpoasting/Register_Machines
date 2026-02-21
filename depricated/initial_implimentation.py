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

# So, basically, this current version cannot work correctly because I need to be able to interpret line by line, and my current tokenization strategy doenst work correctly to do that.

import os

##### INSTRUCTION TOKEN CLASS

class Instruction_Token:
    def __init__(self, line, column, text):
        self.line = line
        self.column = column
        self.text = text
    
    def __repr__(self):
        return f"{self.text} L{self.line}C{self.column}"
    
class Categorized_Token(Instruction_Token):
    def __init__ (self, line, column, text, category):
        super().__init__(line, column, text)
        self.category = category

    def __repr__(self):
        return f"{self.category}  \"{self.text}\" L{self.line}C{self.column}"
##### OPEN FILE
def openfile(file_name, allowed_extensions=(".txt",)): 

    if os.path.isdir(file_name):
        print(f"Error: '{os.path.basename(file_name)}' is a directory, not a file.")
        exit(400)  # 400 = Bad Request

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
        if character in (" ", "\n"): # If you hit a space or newline, colon
            if instruction_text: # This will be "false" if the instruction text is empty
                token = Instruction_Token(instruction_line, instruction_column - len(instruction_text), instruction_text)
                token_list.append(token)
                instruction_text = "" # Resets instruction text contents
            if character == '\n': #endline token for later!
                token = Instruction_Token(instruction_line, instruction_column, "END_LINE")
                token_list.append(token)
                instruction_text = "" # Resets instruction text contents
                instruction_line += 1
                instruction_column = 1
            else: # Basically, if space
                instruction_column += 1
        else: 
            instruction_text += character.upper()
            instruction_column += 1

    if instruction_text: # if last token
        token_list.append(Instruction_Token(instruction_line, instruction_column - len(instruction_text), instruction_text))

    return token_list

def categorize_tokens(token_list):
    categorized_token_list = []

    for token in token_list:
        if token.text in ("REGISTER", "INCREMENT", "DECREMENT", "JUMP", "HALT"):
            categorized_token_list.append(Categorized_Token(token.line, token.column, token.text, "KEYWORD"))
        elif token.text in ("END_LINE"):
            categorized_token_list.append(Categorized_Token(token.line, token.column, token.text, "PUNCTUATION"))
        else:
            categorized_token_list.append(Categorized_Token(token.line, token.column, token.text, "REGISTER"))
    
    return categorized_token_list

def build_nodes(categorized_token_list):

    python_code = ""
    result_code = ""

    i = 0

    while i < len(categorized_token_list):
        token = categorized_token_list[i]
        if token.text == "REGISTER":
            python_code += "class Register:\n\tdef __init__(self, name):\n\t\tself.name = name\n\t\tself.value=0\n\n\tdef increment(self):\n\t\tself.value += 1\n\tdef decrement(self):\n\t\tself.value -= 1\n\t\tif self.value < 1:\n\t\t\tself.value = 0\n\n"
            i += 1
            while categorized_token_list[i].text != "END_LINE":
                python_code += f"{categorized_token_list[i].text} = Register(\"{categorized_token_list[i].text}\")\n"
                result_code +=  f"print({categorized_token_list[i].text}.value)\n"
                i += 1
            python_code += "\n"
            i += 1  # skip endline
        elif token.text == "INCREMENT":
            i += 1
            python_code += f"{categorized_token_list[i].text}.increment()\n"
            i += 1
            assert categorized_token_list[i].text == "END_LINE", f"Expected END_LINE at L{categorized_token_list[i].line}C{categorized_token_list[i].column}, got {categorized_token_list[i].text}"
            i += 1
        elif token.text == "DECREMENT":
            i += 1
            python_code += f"{categorized_token_list[i].text}.decrement()\n"
            i += 1
            assert categorized_token_list[i].text == "END_LINE", f"Expected END_LINE at L{categorized_token_list[i].line}C{categorized_token_list[i].column}, got {categorized_token_list[i].text}"
            i += 1
        else:
            i += 1

    python_code += f"\n{result_code}"
    return python_code

def main():
    instruction_set = openfile("register_program.txt")
    token_list = create_instructiontokens(instruction_set)
    categorized_token_list = categorize_tokens(token_list)
    python_code = build_nodes(categorized_token_list)
    with open("python_output.py", "w") as file:
        file.write(python_code)


if __name__ == "__main__":
    main()