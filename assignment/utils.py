from functools import reduce


class flist:
    def __init__(self, l): self.list = l
    def __iter__(self): return self.list.__iter__()
    def __next__(self): return self.list.__next__()
    def max(self, *a, **kw): return max(self.list, *a, **kw)
    def min(self, *a, **kw): return min(self.list, *a, **kw)
    def sum(self, *a, **kw): return sum(self.list, *a, **kw)
    def len(self, *a, **kw): return len(list(self.list), *a, **kw)
    def reduce(self, *a, **kw): return reduce(self.list, *a, **kw)

    def filter(self, f, *a, **kw):
        self.list = filter(f, self.list, *a, **kw)
        return self

    def map(self, f, *a, **kw):
        self.list = map(f, self.list, *a, **kw)
        return self

    def for_each(self, f):
        for item in self.list:
            f(item)

    def sort(self, *a, **kw):
        self.list = list(self.list)
        self.list.sort(*a, **kw)
        return self


# Better see usage
def bd_map(entries, k, v):
    ret = dict()
    for ent in entries:
        if not ent[k] in ret:
            ret[ent[k]] = set()
        ret[ent[k]].add(ent[v])
    return ret
