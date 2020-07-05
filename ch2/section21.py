from enum import IntEnum
from typing import Tuple, List

Nucleotide: IntEnum = IntEnum("Nucleotide", ('A','C','G','T'))

Codon = Tuple[Nucleotide, Nucleotide, Nucleotide]
Gene = List[Codon]

gene_str: str = "ACGTGGCTCTCTAACGTACGTACGTACGGGGTTTATATATACCCTAGGACTCCCTTT"

def string_to_gene(s: str) -> Gene:
    gene: Gene = []
    for i in range(0, len(s), 3):
        if (i+2) >= len(s):
            return gene
        codon: Codon = (
            Nucleotide[s[i]],
            Nucleotide[s[i+1]],
            Nucleotide[s[i+2]],
        )
        gene.append(codon)
    return gene

def linear_contains(gene: Gene, key_codon: Codon) -> bool:
    for codon in gene:
        if key_codon == codon:
            return True
    return False

def binary_contains(gene: Gene, key_codon: Codon) -> bool:
    low: int = 0
    high: int = len(gene)-1
    while low <= high:
        mid: int = (low + high) // 2
        if key_codon == gene[mid]:
            return True
        if key_codon > gene[mid]:
            low = mid+1
        if key_codon < gene[mid]:
            high = mid-1    
    return False

def test_binary_contains():
    acg: Codon = (Nucleotide.A, Nucleotide.C, Nucleotide.G)
    gat: Codon = (Nucleotide.G, Nucleotide.A, Nucleotide.T)
    assert binary_contains(my_sorted_gene, acg), f"Did not find acg"  
    assert not binary_contains(my_sorted_gene, gat), f"found gat by accident"

def test_linear_contains():
    acg: Codon = (Nucleotide.A, Nucleotide.C, Nucleotide.G)
    gat: Codon = (Nucleotide.G, Nucleotide.A, Nucleotide.T)
    assert linear_contains(my_sorted_gene, acg), f"Did not find acg"  
    assert not linear_contains(my_sorted_gene, gat), f"found gat by accident"

def test_string_to_gene():
    test_gene_str = "ACGTGG"
    test_gene: Gene = [
        (Nucleotide.A, Nucleotide.C, Nucleotide.G),
        (Nucleotide.T, Nucleotide.G, Nucleotide.G),
    ]
    gene_from_func = string_to_gene(test_gene_str)
    for _, each in enumerate(test_gene):
        assert each == gene_from_func[_], f"Failed codon {_}"


if __name__ == "__main__":
    my_gene: Gene = string_to_gene(gene_str)
    my_sorted_gene: Gene = sorted(my_gene)
    
    test_string_to_gene()
    test_linear_contains()
    test_binary_contains()

    