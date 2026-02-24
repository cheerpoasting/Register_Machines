# Small Programming Languages
A collection of small experiments in building programming languages.

## Overview
I want to learn how to create a fully functional programming language, so I'm starting small with a minimal register machine and building up complexity with each project by adding abstractions like labels, higher-level instructions, and eventually functions and bytecode.

## Projects

### Simple_Register
This project creates a simple register machine that accepts an arbitrary number of registers, and recognizes 4 functions: increment, decrement, jump_if_not_zero, and halt. It also supports comments. 
I created this project to help me understand how complex behavior can emerge even using primitive loops.

#### Usage & Instructions
- Make sure that the python file correctly targets the .txt file that contains your instruction set
- Declare your registers using the keyword "register", followed by the names of your registers separated by spaces. ex. "register a b c" -- you can create an arbitrary number of registers, whose names can contain any characters. You can only use one register declaration line.
- Increment and decrement target registers. Use the keyword followed by the target register in the format "increment b".
- Jump_if_not_zero: jump to a specific line if the current register is not zero. If the register is 0, it will continue to the next instruction. Use the keyword followed by the register, then the target line. ex. "jump_if_not_zero a 22"
- Halt: use the command halt to end the program. The keyword is placed on its own line. ex. "halt"
- Comment lines begin with #. They can also follow commands if there is a space between the end of the command and the #. 

There are two sample programs for you to view: new_register.txt and factorial_simplified.txt

### Simple_Assembler
Because editing a program while referencing line numbers and incrementing a register repeatedly is pretty annoying, I decided to create a slightly more complex language where I can jump to labels, increment by more than one, and "move" numbers. 

#### Usage & Instructions
- Make sure that the python file correctly targets the .txt file that contains your instruction set
- Declare your registers using the keyword "register", followed by the names of your registers separated by spaces. ex. "register a b c" -- you can create an arbitrary number of registers, whose names can contain any characters. You can only use one register declaration line.
- Increment and decrement target registers. Use the keyword followed by the amount and then the target register. The "amount" can either be a positive integer (increment 5 a) OR the value of another register (increment b a) meaning that we take the value of register b and add it to a *non-destructively* (the value in register b remains the same).
- Move a value from one register to another. Use the keyword followed by the amount and then the target register. The "amount" can either be a positive integer (move 5 a) OR the value of another register (move b a). This is *destructive* -- if we move 5 to a, then a will equal 5; if we move b to a, then a = b, but b = 0.
- Labels. Create an entrypoint for a specific set of instructions by creating a label for it in the format "_labelname". The label *must* begin with an underscore. Labels must be on their own lines.
- Jump_if_not_zero: jump to a specific label if the current register is not zero. If the register is 0, it will continue to the next instruction. Use the keyword followed by the register, then the target label. ex. "jump_if_not_zero a _mutiplication_loop"
- Halt: use the command halt to end the program. The keyword is placed on its own line. ex. "halt"
- Comment lines begin with #. They can also follow commands if there is a space between the end of the command and the #. 

There are three sample programs for you to view: addition.txt, multiplication.txt, factorial.txt. 

### S_Assembler_Bytecode
In order to do more powerful things, I implemented basic logical operators (not, greater than, less than) as well as native multiplication and division. Additionally, I replaced increment and decrement with the more common "add" and "subtract". In addition to this, I tried to emulate the basic process of a virtual machine. Meaning, in `s_assembler_bytecode.py` I convert instruction set into bytecode, and in `s_assembler_interpreter.py` I created a program that will then read and run that bytecode. 

#### Usage & Instructions
- If you wish to view the bytecode, please run `s_assembler_bytecode.py`, and make sure it correctly targets the .txt file that contains your instruction set. If you wish to run the program, run only `s_assembler_interpreter.py` with the correct .txt instruction set targeted. 
- Declare your registers using the keyword "register", followed by the names of your registers separated by spaces. ex. "register a b c" -- you can create an arbitrary number of registers, whose names can contain any characters. You can only use one register declaration line.
- Add and subtract. Use the keyword followed by the amount and then the target register. The "amount" can either be a positive integer (add 5 a) OR the value of another register (subtract b a) meaning that we take the value of register b and subtract it from a *non-destructively* (the value in register b remains the same). 
- Add and Subtract (Long Form). Use the keyword followed by the first amount and second amount, then the target register. For example short form "add a b" is "b = a + b" and the same as long form add a b b. However, "add a b c" will be "c = a + b"

SUBTRACTION NOTE: 
- "subtract a b c" is equivalent to c = b - a
- Registers can only be non-negative integers (ie, if your subtraction would create a negative number, it becomes zero instead)

- Multiply and Divide. Use the keyword followed by the amount and then the target register. The "amount" can either be a positive integer OR the value of another register. *non-destructive* NOTE: "divide a b" is the same as "b = a/b"
- Multiply and Divide (Long Form). Use the keyword followed by the first amount and second amount, then the target register. For example short form "divide a b" is "b = a / b" and the same as long form divide a b b. However, "divide a b c" will be "c = a / b"

- Move. Use the keyword followed by the amount and then the target register. The "amount" can either be a positive integer (move 5 a) OR the value of another register (move b a). This is *destructive* -- if we move 5 to a, then a will equal 5; if we move b to a, then a = b, but b = 0.
- Jump_if: Use the keyword followed by the register to test, the conditions, then the value to test against, followed by the loop label. The value can either be a positive integer OR the value of another register. If the statement is true, it will jump to the indicated label, otherwise, it will continue to the next instruction. 

CONDITIONS:
- Defaults to "is equal to".
- Supports: not (!), lt (<), gt (>)
- "not" must always go before comparisons. 

JUMP LOGIC: 
- "not" can stand alone. ex. "a not b" is "a != b"
- "not" can negate gt or lt. ex."a not gt b" is "a <= b"

VALID EXAMPLES:
- jump_if a 6 _label_1 (if a == 6, goto label_1)
- jump_if a not b _label_2 (if a !=b, goto label_2)
- jump_if a gt 19 _label_3 (if a > 19, goto label_3)
- jump_if a not lt c _label_4 (if a >= c, goto label 4)

- Labels. Create an entrypoint for a specific set of instructions by creating a label for it in the format "_labelname". The label *must* begin with an underscore. Labels must be on their own lines.
- Halt: use the command halt to end the program. The keyword is placed on its own line. ex. "halt"
- Comment lines begin with #. They can also follow commands if there is a space between the end of the command and the #.

There are five sample programs for you to view: addition.txt, subtraction.txt multiplication.txt, division.txt, factorial.txt. 

## What's Next
- Implementing a stack.
- Function calls.
- Print statements.
- If/else.