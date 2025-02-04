# KSOLVER-X
Find PrivateKey of corresponding Pubkey using random xpoint search<br>
original code : https://github.com/pianist-coder/KSOLVER-X

KSOLVER X is a tool for solving private keys in the Bitcoin secp256k1 curve.

## Features

- Utilizes the secp256k1 elliptic curve python library by iceland2k14 for efficient and fast ec operations
- btc.point_sequential_increment(n, a_)) uses a lot of RAM
- btc.point_sequential_decrement(n, a_)) uses a lot of RAM
- Supports parallel processing using multiple CPU cores for faster computation
- Each CPU Core uses a separate Process with Python Interpreter Instance

## Usage

To use KSOLVER X, you'll need to have the following dependencies installed:

- `cursor`
- `xxhash`

You can install these dependencies using pip:

```
pip install cursor xxhash
```

Once the dependencies are installed, you can run the KSOLVER X script:
<pre>
bloom.py
bits = 46        # range upper bits
count = 20000000 # number of bloom entries
core = 4         # number of CPU cores to use

ksolverx.py
pub = '02b560fa090d174209b122923c5e9968153066cd84707cbecf22dbfd11e15f0ec3' # pubkey to search private key
bits = 46    # range upper bits
n = 20000000 # number of bloom entries
c = 4        # number of CPU cores to use
</pre>
