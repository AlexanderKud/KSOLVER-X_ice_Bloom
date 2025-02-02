# KSOLVER-X
Find PrivateKey of corresponding Pubkey using random xpoint search
original code : https://github.com/pianist-coder/KSOLVER-X

KSOLVER X is a tool for solving private keys in the Bitcoin ecosystem. It is designed to efficiently search for private keys that correspond to a given public key.

## Features

- Utilizes the secp256k1 elliptic curve python library by iceland2k14 for efficient and fast ec operations
- Supports parallel processing using multiple CPU cores for faster computation
- Provides detailed progress information, including estimated probability of finding the key

## Usage

To use KSOLVER X, you'll need to have the following dependencies installed:

- `cursor`
- `xxhash`

You can install these dependencies using pip:

```
pip install cursor xxhash
```

Once the dependencies are installed, you can run the KSOLVER X script:
bloom.py
bits = 46        # range upper bits
count = 20000000 # number of bloom entries
core = 4         # number of CPU cores to use

ksolverx.py
pub = '02b560fa090d174209b122923c5e9968153066cd84707cbecf22dbfd11e15f0ec3' # pubkey to search private key
bits = 46    # range upper bits
n = 20000000 # number of bloom entries
c = 4        # number of CPU cores to use


## How it Works

KSOLVER X uses a combination of techniques to efficiently search for private keys:

1. **Bloom Filter**: The script uses a Bloom filter to quickly check if a potential private key matches the given public key. This allows the script to avoid performing expensive cryptographic operations for keys that are unlikely to match.
2. **Parallel Processing**: The script utilizes multiple CPU cores to search for private keys in parallel, significantly speeding up the computation.
3. **Incremental and Decremental Search**: The script performs both incremental and decremental searches around the base private key, increasing the chances of finding the correct key.
4. **Progress Reporting**: The script provides detailed progress information, including the estimated probability of finding the key, the current search speed, and the elapsed time.

