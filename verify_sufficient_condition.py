import primesieve
import re
import sys
import os
import time

# ================= User Configuration =================
INITIAL_FILE = "pairs_filtered.txt"   # Chain library (initial + appended new chains)
CHECKPOINT_FILE = "checkpoint.txt"     # Checkpoint file (new)
SCAN_START = 100_000_000_000          # Starting position (100 billion)
MAX_P = 10**12                        # Termination position (1 trillion)

LIMIT_S = 1000
LIMIT_B = 10000
MAX_S_LIMIT = 100000
MAX_B_LIMIT = 1000000

SHOW_EVERY = 100000
# ======================================================

def parse_pairs(filename):
    pairs = []
    if not os.path.exists(filename):
        print(f"⚠️  {filename} does not exist, will create a new file")
        return pairs, set()
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            m = re.search(r's\s*=\s*(\d+)\s*[,;]?\s*B\s*=\s*(\d+)', line, re.I)
            if m:
                s, B = int(m.group(1)), int(m.group(2))
                pairs.append((s, B))
                continue
            nums = re.findall(r'\d+', line)
            if len(nums) >= 2:
                s, B = int(nums[0]), int(nums[1])
                pairs.append((s, B))
    return pairs, set(pairs)

def is_covered(p, pairs):
    for s, B in pairs:
        d = s * B - 1
        if d <= 0:
            continue
        if (p + s) % d == 0:
            A = (p + s) // d
            if A % 4 == 3:
                return True
    return False

def search_new_pair(p, limit_s, limit_B):
    for s in range(1, limit_s + 1):
        for B in range(3, limit_B + 1, 4):
            d = s * B - 1
            if d <= 0:
                continue
            if (p + s) % d == 0:
                A = (p + s) // d
                if A % 4 == 3:
                    return (s, B)
    return None

def get_last_checkpoint():
    """Read the last scanned maximum p from checkpoint.txt"""
    if os.path.exists(CHECKPOINT_FILE):
        with open(CHECKPOINT_FILE, 'r') as f:
            try:
                return int(f.read().strip())
            except:
                return SCAN_START
    return SCAN_START

def save_checkpoint(p):
    """Write the current scanned p to checkpoint.txt"""
    with open(CHECKPOINT_FILE, 'w') as f:
        f.write(str(p))

def append_new_pair_to_file(s, B, filename):
    with open(filename, 'a') as f:
        f.write(f"s={s}, B={B}\n")

def main():
    print("🔭 Loading initial chain library...")
    pairs, pairs_set = parse_pairs(INITIAL_FILE)
    print(f"✅ Loaded {len(pairs)} chains from {INITIAL_FILE}")

    start_p = get_last_checkpoint()
    if start_p < SCAN_START:
        start_p = SCAN_START
    print(f"🔭 Will resume scanning from p = {start_p:,} to {MAX_P:,}")
    print(f"📝 Checkpoint file: {CHECKPOINT_FILE}")
    print(f"📝 New chains will be appended to: {INITIAL_FILE}")

    it = primesieve.Iterator()
    it.skipto(start_p)
    p = it.next_prime()
    count = 0
    new_pairs_added = 0
    last_checkpoint = start_p
    start_time = time.time()

    while p < MAX_P:
        if p % 24 == 1:
            count += 1
            if not is_covered(p, pairs):
                print(f"\n💥 Found uncovered prime: {p}")
                print("   🔍 Searching for new (s, B)...")

                s_lim, b_lim = LIMIT_S, LIMIT_B
                new = None
                while s_lim <= MAX_S_LIMIT and b_lim <= MAX_B_LIMIT:
                    new = search_new_pair(p, s_lim, b_lim)
                    if new:
                        break
                    s_lim *= 2
                    b_lim *= 2
                    print(f"   Not found within s≤{s_lim//2}, B≤{b_lim//2}, expanding to s≤{s_lim}, B≤{b_lim}")

                if new:
                    s, B = new
                    if (s, B) not in pairs_set:
                        print(f"   ✅ Found new chain: s={s}, B={B}, appended to {INITIAL_FILE}")
                        pairs.append((s, B))
                        pairs_set.add((s, B))
                        append_new_pair_to_file(s, B, INITIAL_FILE)
                        new_pairs_added += 1
                    else:
                        print(f"   ⚠️  Chain (s={s}, B={B}) already exists, skipping write")
                else:
                    print(f"   ❌ Search failed! Need larger s/B limits, program will exit.")
                    sys.exit(1)

            if count % SHOW_EVERY == 0:
                elapsed = time.time() - start_time
                rate = count / elapsed if elapsed > 0 else 0
                print(f"   📈 Checked {count} candidates, rate {rate:.1f}/s, current p={p:,}")

        # Save checkpoint every 50 billion
        if p - last_checkpoint >= 50_000_000_000:
            save_checkpoint(p)
            last_checkpoint = p
            print(f"   💾 Checkpoint saved to {CHECKPOINT_FILE}: p={p:,}")

        p = it.next_prime()

    save_checkpoint(p)
    print(f"\n💾 Final checkpoint saved to {CHECKPOINT_FILE}: p={p:,}")

    print("\n" + "="*60)
    print("🎉 Scan completed!")
    print(f"   🔢 Total candidates checked: {count} (p≡1 mod 24)")
    print(f"   🆕 New chains discovered this run: {new_pairs_added}")
    print(f"   📂 Current {INITIAL_FILE} contains {len(pairs)} chains")
    print("="*60)

if __name__ == "__main__":
    main()
