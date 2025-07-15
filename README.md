# rechi
Regular Expression with CHain Iteration

## Installation
Install via pip:
```bash
pip install rechi
```

## Usage
### Using like re
Import rechi as re and use it like built-in re:

```python
>>> import rechi as re
```

``compile()`` a pattern and use ``match()`` to find matches similar to re:
    Note: currently only ``compile()`` and ``match()`` are supported.

``match()`` returns a list of ``re.Match`` objects.

```python
>>> p = re.compile("a(b|B)c")
>>> m = p.match("abcde")
>>> print(m)
[<re.Match object; span=(0, 3), match='abc'>]
>>> m[0].groups()
('b')
```

### Chaining
In addition, you can chain patterns together. A chain maches if all patterns in the chain match in that given order until the last pattern in the chain.

```python
>>> p = re.compile("a(b|B)c").chain("(d)").chain("(e)")
>>> m = p.match("abcde")
>>> print(m)
[<re.Match object; span=(0, 3), match='abc'>, <re.Match object; span=(3, 4), match='d'>, <re.Match object; span=(4, 5), match='e'>]
>>> m[0].groups()
('b',)
>>> m[1].groups()
('d',)
>>> m[2].groups()
('e',)
```

### Using options
You can define multiple options in the chain by using a list:

```python
>>> p = re.compile("a(b|B)c").chain(["(d)", "(D)"])
>>> m = p.match("abcde")
>>> print(m)
[<re.Match object; span=(0, 3), match='abc'>, <re.Match object; span=(3, 4)]
>>> m[0].groups()
('b',)
>>> m[1].groups()
('d',)
>>> m = p.match("abcDe")
>>> print(m)
[<re.Match object; span=(0, 3), match='abc'>, <re.Match object; span=(3, 4)]
>>> m[0].groups()
('b',)
>>> m[1].groups()
('D',)
```

To define an optional pattern, use ``None`` as the pattern:

```python
>>> p = re.compile("a(b|B)c").chain(["(d)", None])
>>> m = p.match("abcde")
>>> print(m)
[<re.Match object; span=(0, 3), match='abc'>, <re.Match object; span=(3, 4)]
>>> m[0].groups()
('b',)
>>> m[1].groups()
('d',)
>>> m = p.match("abce")
>>> print(m)
[<re.Match object; span=(0, 3), match='abc'>]
>>> m[0].groups()
('b',)
```

Note: be careful with using ``None`` as the last pattern in the chain as it will always match and the other options will not be checked:

```python
>>> p = re.compile("a(b|B)c").chain([None, "(d)"])
>>> m = p.match("abcde")
>>> print(m)
[<re.Match object; span=(0, 3), match='abc'>]
>>> m[0].groups()
('b',)
```

### Chaining with recursion
You can also chain patterns with recursion.
Since a chain matches if all its elemenets matched, having recursion cannot match any string. To resolve this problem, you need to close the chain with a ``None`` pattern.

```python
>>> p = re.compile("a(b|B)c")
>>> p = p.chain([p, None])  # Will match any number of p pattern. Don't forget to add None as an option to allow match
>>> m = p.match("abcde")
>>> print(m)
[<re.Match object; span=(0, 3), match='abc'>]
>>> m = p.match("abcaBcde")
>>> print(m)
[<re.Match object; span=(0, 3), match='abc'>, <re.Match object; span=(3, 6), match='aBc'>]
>>> m = p.match("abcaBcabcaBcde")
>>> print(m)
[<re.Match object; span=(0, 3), match='abc'>, <re.Match object; span=(3, 6), match='aBc'>, <re.Match object; span=(6, 9), match='abc'>, <re.Match object; span=(9, 12), match='aBc'>]
```

Note that without adding the ``None`` pattern, the chain will not be able to terminate thus will never match.

### Limiting the number of matches
You can also limit the maximum number of match allowed in a pattern object:

```python
>>> p = re.compile("a(b|B)c", max=3)
>>> p = p.chain([p, None])  # Adding None as optional pattern to be able to terminate the chain
>>> m = p.match("abcde")
>>> print(m)
[<re.Match object; span=(0, 3), match='abc'>]
>>> m = p.match("abcaBcde")
>>> print(m)
[<re.Match object; span=(0, 3), match='abc'>, <re.Match object; span=(3, 6), match='aBc'>]
>>> m = p.match("abcaBcabcaBcde")
>>> print(m)
[<re.Match object; span=(0, 3), match='abc'>, <re.Match object; span=(3, 6), match='aBc'>, <re.Match object; span=(6, 9), match='abc'>]
```

### Nesting
You can also nest patterns to create complex options and chains:

```python
>>> p = re.compile("a(b|B)c").chain([re.compile("d(e|E)f").chain("(g)"), "(D)"])
>>> m = p.match("abcdefg")
>>> print(m)
[<re.Match object; span=(0, 3), match='abc'>, <re.Match object; span=(3, 6), match='def'>, <re.Match object; span=(6, 7), match='g'>]
>>> m[0].groups()
('b',)
>>> m[1].groups()
('e',)
>>> m[2].groups()
('g',)
>>> m = p.match("abcDefg")
>>> print(m)
[<re.Match object; span=(0, 3), match='abc'>, <re.Match object; span=(3, 4), match='d'>]
>>> m[0].groups()
('b',)
>>> m[1].groups()
('D',)
```

## Functions
### compile
```python
def compile(pattern, flags=0, max=None)
```
Compile a pattern and return a pattern object.

- ``pattern``: string, Pattern, None, or list of the above.
- ``flags``: re flags to use to compile patterns, default 0.
- ``max``: maximum number of matches allowed, default None.

Returns: ``Pattern`` object.

### Pattern class
```python
class Pattern
    def __init__(self, pattern, flags=0, max=None)
    def chain(self, patterns)
    def match(self, string, pos=0, endpos=None)

    @property
    def flags(self)
    @property
    def pattern(self)
    @property
    def next(self)
    @property
    def max(self)
```

#### Pattern.chain
```python
def chain(self, patterns)
```
Chain patterns to the end of the chain.

``pattern``: string, Pattern, None, or list of the above.

Returns: ``Pattern`` object. Note: the head of the chain is returned.

#### Pattern.match
```python
def match(self, string, pos=0, endpos=None)
```
Match a string against the pattern.

- ``string``: string to match.
- ``pos``: start position, default 0.
- ``endpos``: end position, default None.

Returns: list of ``re.Match`` objects or None if no match.

#### Pattern.flags
```python
@property
def flags(self)
```
Get the flags used to compile the pattern.

#### Pattern.pattern
```python
@property
def pattern(self)
```
Get the list of patterns within the pattern object.

#### Pattern.next
```python
@property
def next(self)
```
Get the next pattern in the chain.

#### Pattern.max
```python
@property
def max(self)
```
Get the maximum number of matches allowed.

## License
GPL-3.0
