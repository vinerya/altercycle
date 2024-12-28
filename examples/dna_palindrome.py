"""
DNA Palindrome Detection Example

This example demonstrates how AlterCycle's binary state alternation
naturally maps to DNA strand complementarity, making it particularly efficient
for detecting palindromic sequences in DNA.

DNA palindromes are sequences that read the same on both strands in opposite
directions, considering base pair complementarity (A-T, C-G).
Example: GAATTC
        CTTAAG

The binary state alternation maps perfectly to this problem:
- State 0: Forward strand
- State 1: Complementary strand
"""

from altercycle_core import AlterCycle
from typing import Dict, List, Tuple
import time

# DNA base pair complementarity
COMPLEMENT = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C'}

class DNAAnalyzer:
    def __init__(self):
        self.sequence = AlterCycle[str]()
        
    def load_sequence(self, sequence: str) -> None:
        """Load a DNA sequence into AlterCycle."""
        # Clear existing sequence
        self.sequence = AlterCycle[str]()
        
        # Add each base with its metadata
        for i, base in enumerate(sequence):
            self.sequence.append(base, {
                'position': i,
                'complement': COMPLEMENT[base]
            })
            
    def find_palindromes(self, min_length: int = 4) -> List[Tuple[str, int]]:
        """
        Find palindromic sequences using state alternation.
        Returns list of (palindrome, start_position) tuples.
        """
        palindromes = []
        
        # Use the structure's pattern detection with state awareness
        patterns = self.sequence.find_patterns(min_length)
        
        for pattern, frequency in patterns:
            # Extract just the bases from the pattern (ignoring state)
            bases = [p[0] for p in pattern]
            
            # Check if it's a valid palindrome considering complementarity
            is_palindrome = True
            for i in range(len(bases) // 2):
                if COMPLEMENT[bases[i]] != bases[-(i+1)]:
                    is_palindrome = False
                    break
                    
            if is_palindrome:
                palindromes.append((''.join(bases), pattern[0][2]['position']))
                
        return palindromes

def compare_performance():
    """Compare performance with traditional approach."""
    sequence = "GAATTCAAGCTTGAATTC" * 100  # Create a longer sequence for testing
    
    # AlterCycle approach
    start = time.time()
    analyzer = DNAAnalyzer()
    analyzer.load_sequence(sequence)
    altercycle_palindromes = analyzer.find_palindromes()
    altercycle_time = time.time() - start
    
    # Traditional approach
    def find_palindromes_traditional(sequence: str, min_length: int = 4) -> List[Tuple[str, int]]:
        palindromes = []
        for i in range(len(sequence) - min_length + 1):
            for j in range(i + min_length, len(sequence) + 1):
                substr = sequence[i:j]
                # Create complement strand
                complement = ''.join(COMPLEMENT[base] for base in reversed(substr))
                if substr == complement:
                    palindromes.append((substr, i))
        return palindromes
    
    start = time.time()
    traditional_palindromes = find_palindromes_traditional(sequence)
    traditional_time = time.time() - start
    
    print(f"\nPerformance Comparison (sequence length: {len(sequence)})")
    print(f"AlterCycle approach:     {altercycle_time:.6f}s")
    print(f"Traditional approach:    {traditional_time:.6f}s")
    print(f"Speedup factor:         {traditional_time/altercycle_time:.2f}x")
    
    # Verify results match
    altercycle_set = set((p[0], p[1]) for p in altercycle_palindromes)
    trad_set = set((p[0], p[1]) for p in traditional_palindromes)
    assert altercycle_set == trad_set, "Results don't match!"

if __name__ == "__main__":
    # Example usage
    analyzer = DNAAnalyzer()
    
    # Load a sequence with known palindromes
    sequence = "GAATTCAAGCTTGAATTC"
    print(f"\nAnalyzing sequence: {sequence}")
    
    analyzer.load_sequence(sequence)
    palindromes = analyzer.find_palindromes()
    
    print("\nFound palindromes:")
    for seq, pos in palindromes:
        print(f"Sequence: {seq}")
        print(f"Position: {pos}")
        print(f"Complement: {''.join(COMPLEMENT[b] for b in reversed(seq))}\n")
    
    # Compare performance
    compare_performance()
