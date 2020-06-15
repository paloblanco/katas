from typing import Union

class BitString:
    def __init__(self, value: Union[int,str] = 0) -> None:
        if type(value) == int:
            self._value: int = value
        elif type(value) == str:
            try:
                int_val = int(value,2)
                self._value = int_val
            except ValueError:
                print("String must be sequence of 0 and 1, eg '0101'")
     
    def append_bit_string(self, value: str) -> str:   
        try:
            int_new_value: int = int(value,2)
            length_bits = len(value) # need length from string, in case there are leading 0s
            self._value <<= length_bits
            self._value |= int_new_value
            return format(self._value, "b")
        except ValueError:
            print("String must be sequence of 0 and 1, ie '0101'")
    
    def get_length(self) -> int:
        return len(format(self._value,"b"))

    def __getitem__(self, key: int) -> str:
        value_bit_string: str = format(self._value, "b")
        return value_bit_string[key]

    def __repr__(self) -> str:
        return format(self._value, "b")


def test_BitString_get_length():
    test_int = 107
    test_string_old = '1101011'
    test_len = len(test_string_old)
    bit = BitString(107)
    assert bit.get_length() == test_len

def test_BitString_append_val():
    test_int = 107
    test_string_old = '1101011'
    test_val = "01"
    new_val = 429
    bit = BitString(test_int)
    assert bit.append_bit_string(test_val) == test_string_old+test_val

def test_BitString_get_5():
    test_int = 127
    test_ix = 5
    expected_value = "1"
    bit = BitString(test_int)
    assert bit[test_ix] == "1"
    
def test_BitString_get_slice():
    test_int = 107
    slice_start = 1
    slice_end = 4
    expected_value = "101"
    bit = BitString(test_int)
    assert bit[slice_start:slice_end] == expected_value

def run_tests():
    test_BitString_append_val()
    test_BitString_get_5()
    test_BitString_get_length()
    test_BitString_get_slice()

class CompressedGene:
    def __init__(self, gene: str) -> None:
        self._compress(gene)

    def _compress(self, gene: str) -> None:
        for nucleotide in gene.upper():
            if nucleotide == "A":
                bit_to_set = ("00")
            elif nucleotide == "C":
                bit_to_set = ("01")
            elif nucleotide == "G":
                bit_to_set = ("10")
            elif nucleotide == "T":
                bit_to_set = ("11")
            else:
                raise ValueError(f"Invalid Nuecleotide:{nucleotide}")
            try:
                self.bit_string.append_bit_string(bit_to_set)
            except:
                self.bit_string: BitString = BitString(bit_to_set)

    def decompress(self) -> str:
        gene: str = ""
        for i in range(0, self.bit_string.get_length(), 2):
            bits: str = self.bit_string[i:i+2]
            if bits == "00":
                gene += "A"
            elif bits == "01":
                gene += "C"
            elif bits == "10":
                gene += "G"
            elif bits == "11":
                gene += "T"
            else:
                raise ValueError(f"Invalid bits:{bits}")
        return gene

    def __str__(self) -> str:
        return self.decompress()



if __name__ == "__main__":
    run_tests()
    from sys import getsizeof
    original :str = "TAGGGATTAACCGTTATATATATATAGCCATGGATCGATTATATAGGGATTAACCGTTATATATATATAGCCATGGATCGATTATA" * 100
    print(f"original is {getsizeof(original)} bytes")
    compressed: CompressedGene = CompressedGene(original)
    print(f"compressed is {getsizeof(compressed.bit_string)} bytes")
    print(compressed)
    print(f"original and decompressed are the same {original == compressed.decompress()}")
