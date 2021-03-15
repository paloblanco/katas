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

def cluster_bits(bits: str) -> str:
    # find clusters, and replace bit sequences with fixed values, then feed to original function
    bits = bits.strip("0")
    press_lengths1 = []
    press_lengths0 = []
    last_bit = "1"
    current_count = 0
    for bit in bits:
        if bit == last_bit:
            current_count += 1
        else:
            if last_bit == "1":
                press_lengths1.append(current_count)
            elif last_bit == "0":
                press_lengths0.append(current_count)
            last_bit = bit
            current_count = 1
    press_lengths1.sort()
    press_lengths0.sort()
    press_lengths_all = press_lengths0+press_lengths1
    press_lengths_all.sort()
    gaps = {}
    for i,step in enumerate(press_lengths_all[:-1]):
        new_gap = press_lengths_all[i+1] - step
        gaps[step] = max(gaps.get(step,0),new_gap)
    splits = {}
    for k,v in gaps.items():
        radius = v/2.0
        splits[k+radius] = radius
    return splits


def decodeBitsAdvanced(bits: str) -> str:
    bits = cluster_bits(bits)
    return decode_bits(bits)

def decode_bits(bits: str) -> str:
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
    ## MISC TESTING
    bad_bits = '0000000011011010011100000110000001111110100111110011111100000000000111011111111011111011111000000101100011111100000111110011101100000100000'
    print(f"Original: {bad_bits}")
    print(f"Fixed?  : {cluster_bits(bad_bits)}")

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

    # tests_advanced = [
    #     ('HEY JUDE', '0000000011011010011100000110000001111110100111110011111100000000000111011111111011111011111000000101100011111100000111110011101100000100000')
    # ]
    # for expected, got in tests_advanced:
    #     bit_string = decodeBitsAdvanced(got)
    #     print(f"New bits: {bit_string}")
    #     print(f"Expected: {expected}   got: {decodeMorse(bit_string)}")

