# original code : https://github.com/pianist-coder/KSOLVER-X
# pip install xxhash cursor
import os, sys, xxhash, random, time
import secp256k1
from multiprocessing import Process, cpu_count, Value, Event
import cursor

cursor.hide()

bits = 46
count = 20000000
bloom_filter_name = f'{bits}.bf'
filebase = f'{bits}.txt'
core = 4

_elem = (count * 2)
_fp = 0.000001
_bits, _hashes = secp256k1.bloom_para(_elem, _fp)
_bf = (b'\x00') * (_bits//8)

start = bits - 1
end = bits

st = time.time()

def pr():
    print(f'[+] Creating BloomFilter')
    print(f'[+] Items: {count}')
    print(f'[+] Cores: {core}')
    
def generate_random_bloom(start, end):
    rnd = {}
    for _ in range(10000):
        x = random.randint(2 ** start - (2 ** start - 5), 2 ** end - 1)
        P = secp256k1.scalar_multiplication(x)
        rnd[P] = f'{x:x}'
    return rnd

def scan_str(num):
    suffixes = ["", "K", "M", "B", "T"]
    exponent = 0
    while abs(num) >= 1000 and exponent < 4:
        num /= 1000
        exponent += 1
    return f"{num:.2f} {suffixes[exponent]}"

def display_time(seconds):
    hours, rem = divmod(seconds, 3600)
    minutes, seconds = divmod(rem, 60)
    return f"{int(hours):02d}:{int(minutes):02d}:{seconds:05.2f}"

def speedup(st, counter):
    speed = counter / (time.time() - st)
    print(f'[+] [{scan_str(counter)}] [{scan_str(speed)}keys] [{display_time(time.time() - st)}]      ', end = '\r')
    
def bloom_start(cores='all'):    
    try:
        available_cores = cpu_count()
        if cores == 'all': cores = available_cores
        elif 0 < int(cores) <= available_cores: cores = int(cores)
        else: cores = 1
        counter = Value('L')
        workers = []
        match = Event()
        for r in range(cores):
            p = Process(target=bloom_create, args=(counter, r, match))
            workers.append(p)
            p.start()
        for worker in workers:
            worker.join()
    except(KeyboardInterrupt, SystemExit):
        exit('\nSIGINT or CTRL-C detected. Exiting gracefully. BYE')
    sys.stdout.write('[+] Time taken {0:.2f} sec\n'.format(time.time() - st))

def save_data(data, filename):
    with open(filename, "a") as f:
        for item, value in data.items():
            secp256k1.add_to_bloom(item, _bits, _hashes, _bf)
            f.write(f'{value};{xxhash.xxh64(item).hexdigest()}\n')
            
def bloom_create(counter, r, match):
    st = time.time()
    while not match.is_set():
        if match.is_set(): return
        temp = generate_random_bloom(start, end)
        save_data(temp, filebase)
        with counter.get_lock(): counter.value += 10000
        if counter.value % 100000 == 0:
            speedup(st, counter.value)
        if counter.value == count:
            print(f'\n[+] Writing Bloomfilter to {bloom_filter_name}')
            secp256k1.dump_bloom_file(bloom_filter_name, _bits, _hashes, _bf, _fp, _elem)
            match.set()

if __name__ == '__main__':            
    pr()
    bloom_start(cores=core)
