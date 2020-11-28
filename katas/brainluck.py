def inc(value):
    return (value+1)%256

def dec(value):
    return(value-1)%256

def val_from_char(char):
    return ord(char)

def char_from_val(val):
    return chr(val)

def brain_luck(code, program_input):
    tape = [0 for i in range(10000)]
    ix_pointer = 0
    ix_input = 0
    ix_code = 0
    output=""
    processing = True
    while processing:
        current_operator = code[ix_code]
        if current_operator == ">":
            ix_pointer += 1
            ix_code += 1
        elif current_operator == "<":
            ix_pointer += -1
            ix_code += 1
        elif current_operator == "+":
            tape[ix_pointer] = inc(tape[ix_pointer])
            ix_code += 1
        elif current_operator == "-":
            tape[ix_pointer] = dec(tape[ix_pointer])
            ix_code += 1
        elif current_operator == ".":
            new_char = char_from_val(tape[ix_pointer])
            output += new_char
            ix_code += 1
        elif current_operator == ",":
            new_val = val_from_char(program_input[ix_input])
            tape[ix_pointer] = new_val
            ix_input += 1
            ix_code += 1
        elif current_operator == "[":
            if tape[ix_pointer] == 0:
                open_count = 1
                ix_code_check  = ix_code+1
                while open_count > 0:
                    next_operator = code[ix_code_check]
                    if next_operator == "[": open_count += 1
                    if next_operator == "]": open_count += -1
                    ix_code_check += 1
                ix_code = ix_code_check
            else:
                ix_code += 1
        elif current_operator == "]":
            if tape[ix_pointer] != 0:
                open_count = 1
                ix_code_check  = ix_code-1
                while open_count > 0:
                    next_operator = code[ix_code_check]
                    if next_operator == "[": open_count += -1
                    if next_operator == "]": open_count += 1
                    ix_code_check += -1
                ix_code = ix_code_check+2
            else:
                ix_code += 1
        if ix_code >= len(code):
            processing = False
    return output
    


if __name__ == "__main__":

    assert brain_luck(',.',"Codewars") == "C"

    # Echo until byte(255) encountered
    assert brain_luck(',+[-.,+]', 'Codewars' + chr(255)) == 'Codewars', brain_luck(',+[-.,+]', 'Codewars' + chr(255))

    # Echo until byte(0) encountered
    assert brain_luck(',[.[-],]', 'Codewars' + chr(0)) == 'Codewars'

    # Two numbers multiplier
    assert brain_luck(',>,<[>[->+>+<<]>>[-<<+>>]<<<-]>>.', chr(8) + chr(9)) == chr(72)

    print(brain_luck(',>+>>>>++++++++++++++++++++++++++++++++++++++++++++>++++++++++++++++++++++++++++++++<<<<<<[>[>>>>>>+>+<<<<<<<-]>>>>>>>[<<<<<<<+>>>>>>>-]<[>++++++++++[-<-[>>+>+<<<-]>>>[<<<+>>>-]+<[>[-]<[-]]>[<<[>>>+<<<-]>>[-]]<<]>>>[>>+>+<<<-]>>>[<<<+>>>-]+<[>[-]<[-]]>[<<+>>[-]]<<<<<<<]>>>>>[++++++++++++++++++++++++++++++++++++++++++++++++.[-]]++++++++++<[->-<]>++++++++++++++++++++++++++++++++++++++++++++++++.[-]<<<<<<<<<<<<[>>>+>+<<<<-]>>>>[<<<<+>>>>-]<-[>>.>.<<<[-]]<<[>>+>+<<<-]>>>[<<<+>>>-]<<[<+>-]>[<+>-]<<<-]', chr(10)))
