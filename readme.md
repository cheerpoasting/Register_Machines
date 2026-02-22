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

## What's Next
- A "bytecode" version of a simple assembler. 
- Implementing a stack.
- Function calls.
- Basic logical operators.
- Native multiplication and division.