import math
import time
import multiprocessing as mp
import primesieve
from tqdm import tqdm

BRADFORD_RESIDUES = {
    1, 169, 289, 361, 529, 841, 961, 1369, 1681, 1849, 2041, 2209,
    2521, 2641, 2689, 2809, 3361, 3481, 3529, 3721, 4321, 4489, 5041,
    5161, 5329, 5569, 6169, 6241, 6889, 7561, 7681, 7921, 8089, 8761
}
MOD = 9240

def is_target(p):
    return (p % MOD) in BRADFORD_RESIDUES

def weak_solution(p, s_max=1000):
    if p % 12 != 1:
        return None
    k = (p - 1) // 12
    for s in range(1, s_max + 1):
        M = p + s
        limit = int(math.isqrt(M))
        for d in range(3, limit + 1, 4):
            if M % d == 0:
                D = d
                c = (D + 1) // 4
                y = 3 * k + c
                if (p * p * y) % s == 0 and math.gcd(s * y, D) == 1:
                    return s, D, y
                D2 = M // d
                if D2 != d and D2 % 4 == 3:
                    c2 = (D2 + 1) // 4
                    y2 = 3 * k + c2
                    if (p * p * y2) % s == 0 and math.gcd(s * y2, D2) == 1:
                        return s, D2, y2
    return None

def test_prime(p):
    res = weak_solution(p)
    if res:
        s, D, y = res
        if s > 200:
            return (p, s, D, y)
    return None

def main():
    limit = 10**10
    print("Generating target prime list...")
    it = primesieve.Iterator()
    it.skipto(2)
    target_primes = []
    p = it.next_prime()
    count = 0
    start_collect = time.time()
    while p < limit:
        if p % 12 == 1 and is_target(p):
            target_primes.append(p)
            count += 1
            if count % 100000 == 0:
                elapsed = time.time() - start_collect
                print(f"Collected {count} target primes, current p = {p}, elapsed {elapsed:.1f} sec")
        p = it.next_prime()
    print(f"Collection complete, {len(target_primes)} target primes, total time {time.time()-start_collect:.1f} sec")

    print("Starting parallel test of weak condition...")
    start_test = time.time()
    with mp.Pool(processes=mp.cpu_count()) as pool:
        results = list(tqdm(pool.imap_unordered(test_prime, target_primes), total=len(target_primes), desc="Test progress"))
    large_s = [r for r in results if r is not None]
    print(f"Test complete, elapsed {time.time()-start_test:.1f} sec")
    print(f"Total tested {len(target_primes)} primes, among them {len(large_s)} require s > 200:")
    for p, s, D, y in large_s:
        print(f"p = {p}, s = {s}, D = {D}, y = {y}")

if __name__ == "__main__":
    main()
