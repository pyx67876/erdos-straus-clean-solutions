# Supplementary Materials for "A Constructive Approach to the Erdős–Straus Conjecture"

## File Descriptions
- `verify_weak_condition.py`: Full Python code for verifying the weak condition in the r=1 parametrization.  
   For all primes p ≡ 1 (mod 12) belonging to the 34 hardest residue classes (mod 9240) identified by Bradford & Ionascu, it searches for s ≤ 1000 and D ≡ 3 (mod 4) satisfying the condition.  
   Outputs primes with s > 200 (consistent with Table 2 in the paper).

- `table2_large_s_primes.txt`: The 43 prime data (p, s, D, y) from Table 2 of the paper.

## Requirements
- Python 3.8+
- Installation: `pip install primesieve tqdm`
- Runtime: approximately 25 minutes (multi-core CPU, range up to 10¹⁰)

## Usage
Can be directly used to reproduce the computational results in Section 6 of the paper, or as a basis for future larger-scale verification.

Author: Yixuan Peng (2026)
