from threading import RLock


class Sieve:
    def __init__(self, maxsize):
        self.maxsize = maxsize
        self.cache = {}
        self.tail = []
        self.full = None
        self.lock = RLock()
        self.tail[:] = [
            self.tail,  # PREV
            self.tail,  # NEXT
            None,       # KEY
            None,       # RESULT
            None,       # VISITED
        ]
        self.PREV, self.NEXT, self.KEY, self.RESULT, self.VISITED = 0, 1, 2, 3, 4
        self.hand = self.tail

    def _evict(self):
        """Evicts an entry using the Sieve eviction strategy."""
        o = self.hand
        if o[self.KEY] is None:
            o = self.tail[self.PREV]

        while o[self.VISITED]:
            o[self.VISITED] = False
            o = o[self.PREV]
            if o[self.KEY] is None:
                o = self.tail[self.PREV]

        # Remove evicted entry
        self.hand = o[self.PREV]
        oldkey = o[self.KEY]
        self.hand[self.NEXT] = o[self.NEXT]
        o[self.NEXT][self.PREV] = self.hand
        del self.cache[oldkey]
        return oldkey

    def _insert(self, key, result):
        """Inserts a new entry into the cache."""
        head = self.tail[self.NEXT]
        new_entry = [self.tail, head, key, result, True]  # PREV, NEXT, KEY, RESULT, VISITED
        head[self.PREV] = self.tail[self.NEXT] = self.cache[key] = new_entry
        self.full = len(self.cache) >= self.maxsize

    def request(self, oblock):
        """Handles a cache request for a block."""
        key = oblock
        link = self.cache.get(key)

        if link is not None:
            # Cache hit
            link[self.VISITED] = True
            return False, None  # Miss = False, Evicted = None

        # Cache miss
        evicted = None
        with self.lock:
            if self.full:
                evicted = self._evict()
            self._insert(key, None)
        return True, evicted  # Miss = True, Evicted = evicted key
