from .lru import LRU
from .lfu import LFU
from .lecar import LeCaR
from .sieve import Sieve

def get_algorithm(alg_name):
    alg_name = alg_name.lower()

    if alg_name == 'lru':
        return LRU
    if alg_name == 'lfu':
        return LFU
    if alg_name == 'lecar':
        return LeCaR
    if alg_name == 'sieve':
        return Sieve
    return None
