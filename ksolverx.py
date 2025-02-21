# original code : https://github.com/pianist-coder/KSOLVER-X
# pip install xxhash cursor
import sys, time, xxhash, os
import secp256k1 as btc
import random
from multiprocessing import Event, Process, Queue, Value, cpu_count, active_children
from math import log2
import cursor

cursor.hide()

pub = '02b560fa090d174209b122923c5e9968153066cd84707cbecf22dbfd11e15f0ec3'
a = btc.pub2upub(pub)
bits = 46
blname = f'{bits}.bf'
basefile = f'{bits}.txt'
n = 20000000
c = 4
l = n

_bits, _hashes, _bf, _fp, _elem = btc.read_bloom_file(blname)

st = time.time()
start = 2 ** (bits - 1)
end = 2 ** bits - 1

def pr():
    print(f'[+] Pubkey:      {btc.point_to_cpub(a).upper()}')
    print(f'[+] Bloom items: {n}')
    print(f'[+] Key range:   {bits - 1} bits')
    print(f'[+] Cores:       {c}')
    print(f'[+] Search in progress...\n')

def find(word, file):
    with open(file, "r") as f:
        for line in f:
            if word in line:
                return int(line.split(";")[0], 16)
    return None

def chunks(s):
    for start in range(0, 65*n, 65):
        yield s[start : start + 65]

def key_solver(cores="all"):
    available_cores = cpu_count()
    if cores == "all": cores = available_cores
    elif 0 < int(cores) <= available_cores: cores = int(cores)
    else: cores = 1
    match = Event()
    queue = Queue()
    workers = []
    
    for r in range(cores):
        p = Process(target=solve_keys, args=(match, queue, r))
        workers.append(p)
        p.start()

    private_key = queue.get()
    print(f'\n[+] Private Key: {hex(private_key)}\n[+] Address:     {btc.privatekey_to_address(0, True, private_key)}\n[+] WIF:         {btc.btc_pvk_to_wif(private_key)}\n')
    print(f'[+] Time taken {time.time() - st:.2f} sec')
    active = active_children()
    for child in active:
        child.kill()
    os._exit(0)

def solve_keys(match, queue, r):
    while not match.is_set():
        step = random.randint(2**(bits-5), 2**(bits-4))
     #   step = random.randint(2**(rng-6), 2**(rng-5)) ### do not go beyond the range
        a_ = btc.point_subtraction(a, btc.scalar_multiplication(step))
     #   with open('possible.txt', 'a') as found: ### you may save result xpoints for future
     #       found.write(f'{a_.hex()[2:66]} # + {step:x}\n')
        for i1, item in enumerate(chunks(btc.point_sequential_increment(n, a_))):
            if btc.check_in_bloom(item, _bits, _hashes, _bf):
                process_collision(item, i1 + 1, match, queue, r, basefile, "addition", step)
                if match.is_set(): return
        for i2, item in enumerate(chunks(btc.point_sequential_decrement(n, a_))):
            if btc.check_in_bloom(item, _bits, _hashes, _bf):
                process_collision(item, i2 + 1, match, queue, r, basefile, "subtraction", step)
                if match.is_set(): return

def process_collision(item, i, match, queue, r, basefile, sign, step):
    print(f'[+] BloomFilter Collision...')
    p1 = find(xxhash.xxh64(item).hexdigest(), basefile)
    if p1:
        offset = p1 - i + step if sign == "addition" else p1 + i + step
        with open('FOUND.txt', 'a') as found:
            found.write(f'{a.hex()};{offset:x}\n')
        print(f'[+] Core#{r} solved key by {sign} with step {step:x}')
        match.set()
        queue.put_nowait(offset)
    else:
        print(f'[+] False Positive')

if __name__ == '__main__':
    pr()
    key_solver(cores=c)
