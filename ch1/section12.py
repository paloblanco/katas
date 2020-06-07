class GetList:
    def __init__(self, startlist: list = []):
        self._list = startlist

    def __getitem__(self, key):
        return self._list[key]

class BitString(int):
    def __new__(cls, value: int = 0) -> None:
        return int.__new__(cls, int(value))
    
    def __getitem__(self, key: int) -> str:
        value_bit_string: str = format(self, "b")
        return value_bit_string[key]

    def __repr__(self) -> str:
        return repr(format(self, "b"))

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


class CompressedGene:
    def __init__(self, gene: str) -> None:
        self._compress(gene)

    def _compress(self, gene: str) -> None:
        self.bit_string: int = 1
        for nucleotide in gene.upper():
            self.bit_string <<= 2
            if nucleotide == "A":
                self.bit_string |= 0b00
            elif nucleotide == "C":
                self.bit_string |= 0b01
            elif nucleotide == "G":
                self.bit_string |= 0b10
            elif nucleotide == "T":
                self.bit_string |= 0b11
            else:
                raise ValueError(f"Invalid Nuecleotide:{nucleotide}")

    def decompress(self) -> str:
        gene: str = ""
        for i in range(0, self.bit_string.bit_length() - 1, 2):
            bits: int = self.bit_string >> i & 0b11
            if bits == 0b00:
                gene += "A"
            elif bits == 0b01:
                gene += "C"
            elif bits == 0b10:
                gene += "G"
            elif bits == 0b11:
                gene += "T"
            else:
                raise ValueError(f"Invalid bits:{bits}"
            )
        return gene[::-1]

    def __str__(self) -> str:
        return self.decompress()



if __name__ == "__main__":
    from sys import getsizeof
    original :str = "TAGGGATTAACCGTTATATATATATAGCCATGGATCGATTATATAGGGATTAACCGTTATATATATATAGCCATGGATCGATTATA" * 100
    print(f"original is {getsizeof(original)} bytes")
    compressed: CompressedGene = CompressedGene(original)
    print(f"compressed is {getsizeof(compressed.bit_string)} bytes")
    print(compressed)
    print(f"original and decompressed are the same {original == compressed.decompress()}")
