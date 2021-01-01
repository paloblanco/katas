"""
3 part kata.
Part 1: https://www.codewars.com/kata/54b724efac3d5402db00065e

"""

MORSE_CODE_DICT = { 'A':'.-', 'B':'-...', 
                    'C':'-.-.', 'D':'-..', 'E':'.', 
                    'F':'..-.', 'G':'--.', 'H':'....', 
                    'I':'..', 'J':'.---', 'K':'-.-', 
                    'L':'.-..', 'M':'--', 'N':'-.', 
                    'O':'---', 'P':'.--.', 'Q':'--.-', 
                    'R':'.-.', 'S':'...', 'T':'-', 
                    'U':'..-', 'V':'...-', 'W':'.--', 
                    'X':'-..-', 'Y':'-.--', 'Z':'--..', 
                    '1':'.----', '2':'..---', '3':'...--', 
                    '4':'....-', '5':'.....', '6':'-....', 
                    '7':'--...', '8':'---..', '9':'----.', 
                    '0':'-----', ', ':'--..--', '.':'.-.-.-', 
                    '?':'..--..', '/':'-..-.', '-':'-....-', 
                    '(':'-.--.', ')':'-.--.-'} 

MORSE_CODE = {v:k for k, v in MORSE_CODE_DICT.items()}

def decode_bits(bits: str):
    # if i assume there is at least one dot, i expect a short string of 1s
    # count the shortest 1 string, then take that as my denominator
    bits=bits.strip("0")
    count1=0
    count0=0
    min1=100
    for bit in bits:
        if bit == "1":
            count1 += 1
            if count0 > 0:
                min1 = min(min1,count0)
            count0 = 0
        else:
            count0 += 1
            if count1 > 0:
                min1 = min(min1,count1)
            count1 = 0
    print(min1)
    bits = bits[::min1]
    return bits.replace('0000000','   ').replace('111', '-').replace('000', ' ').replace('1', '.').replace('0', '')


def decodeMorse(morse_code):
    morse_code = morse_code.strip()
    morse_code = morse_code.replace("   "," space ")
    morse_code_tokens = morse_code.split(" ")
    translation = ""
    for token in morse_code_tokens:
        letter = MORSE_CODE.get(token,token)
        translation += letter
    translation = translation.replace("space"," ")
    return translation


if __name__ == "__main__":
    tests_decode = [
        ('HEY JUDE', '.... . -.--   .--- ..- -.. .')
    ]
    failed = 0
    for expected, got in tests_decode:
        print(f"Expected: {expected}   got: {decodeMorse(got)}")

    tests_bit = [
        ('HEY JUDE','1100110011001100000011000000111111001100111111001111110000000000000011001111110011111100111111000000110011001111110000001111110011001100000011')
    ]
    for expected, got in tests_bit:
        bit_string = decode_bits(got)
        print(f"New bits: {bit_string}")
        print(f"Expected: {expected}   got: {decodeMorse(bit_string)}")