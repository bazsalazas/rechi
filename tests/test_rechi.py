import sys
sys.path.append('..')

import rechi
import re

mat = "Apple banana cherry date egg fig grape honey kiwi lemon mango nectar orange pear raisin strawberry"
p = r"\s*(\w+)"

# Test string matching
r = rechi.compile(p).match(mat) 
c = re.compile(p).match(mat)
assert r is not None
assert c is not None
assert r[0].re == c.re
assert r[0].groups() == c.groups()

r = rechi.compile(p).chain(p).match(mat) 
assert r is not None
c2 = re.compile(p).match(mat, pos=c.end())
assert c2 is not None
assert r[0].re == c.re
assert r[0].groups() == c.groups()
assert r[1].re == c2.re
assert r[1].groups() == c2.groups()

o = rechi.compile(p)
o.chain([o, None])
r = o.match(mat)
assert r is not None
assert len(r) == 16
assert r[0].re == c.re
assert r[0].groups() == c.groups()
assert r[1].re == c2.re
assert r[1].groups() == c2.groups()

o = rechi.compile(p, max=4)
o.chain([o, None])
r = o.match(mat)
assert r is not None
assert len(r) == 4
assert r[0].re == c.re
assert r[0].groups() == c.groups()
assert r[1].re == c2.re
assert r[1].groups() == c2.groups()

