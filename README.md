# Clean Solutions for the Erdős–Straus Conjecture

This repository contains all code and data necessary to reproduce the computational verification results reported in:

> **"Clean Solutions to the Erd˝os–Straus Conjecture: A Unified Parametrization and Nonexistence of Clean Solutions for Perfect Squares \(n=m^2>4\)"**  
> (submitted to *Journal of Experimental Mathematics*)
 
## Overview

We verify the sufficient condition from Theorem 4.1:

For primes \( p \equiv 1 \pmod{12} \), if there exist integers \( A \equiv 3 \pmod{4} \) and \( B \equiv 3 \pmod{4} \) such that \( AB-1 \mid p+A \), then a solution to \( 4/p = 1/x + 1/y + 1/z \) exists.

We search for such \( (A,B) \) pairs for:
- All \( p \equiv 1 \pmod{12} \) up to \( 10^{10} \), focusing on the 34 hardest residue classes modulo 9240.
- All \( p \equiv 1 \pmod{24} \) up to \( 10^{12} \), as the most demanding subclass.

## Repository Structure

| Path | Description |
| :--- | :--- |
| `algorithm/` | Core search engine and parallel workers |
| `data/raw/` | Complete `(s, B)` pairs for each verified prime |
| `data/processed/` | Summary statistics used to generate Tables 1–2 |
| `data/exceptional/` | Primes requiring unusually large `s` (> 2000) |
| `scripts/` | Scripts to regenerate tables and figures |
| `notebooks/` | Jupyter notebooks for exploratory analysis |
| `tests/` | Unit tests for the search logic |

## Requirements

See `requirements.txt`. Key dependencies:
- Python 3.9+
- `primesieve` (fast prime generation)
- `sympy` (divisor enumeration)
- `numpy`, `pandas` (data handling)
- `matplotlib` (figure generation)

## How to Reproduce

### 1. Install environment

 "python_version": "3.10.20",
 "os": "Windows 10",
 "cpu_cores": 32,
 "libraries": 
 "primesieve": "2.3.0",
 "sympy": "1.14.0",
 "numpy": "1.26.4",
 "pandas": "2.3.3",
 "matplotlib": "3.10.8",
 "tqdm": "4.67.3"
 

