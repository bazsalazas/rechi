from typing import List, AnyStr, overload
import re

class Pattern:
    """ Pattern class provides a way to match a string with a list of pattern options and continue to match with chained expression."""

    _patterns: List["re.Pattern | Pattern | None"]
    _flags: int | re.RegexFlag
    _next: "Pattern | None"
    _max: int
    _matched: int

    @overload
    def __init__(self, pattern: AnyStr, flags: int | re.RegexFlag = 0, next: "Pattern | None" = None, max: int = 0): ...
    @overload
    def __init__(self, pattern: "Pattern", flags: int | re.RegexFlag = 0, next: "Pattern | None" = None, max: int = 0): ...
    @overload
    def __init__(self, pattern: None, flags: int | re.RegexFlag = 0, next: "Pattern | None" = None, max: int = 0): ...
    @overload
    def __init__(self, pattern: List["AnyStr | Pattern | None"], flags: int | re.RegexFlag = 0, next: "Pattern | None" = None): ...
    def __init__(self, pattern, flags=0, next=None, max=0):
        """ Initialize Pattern with a list of match options and an optional next chain element.
            Flags can be provided to parse string patterns into regex patterns."""

        self._patterns = []
        self._flags = flags
        self._next = next
        self._max = max

        if isinstance(pattern, List):
            for p in pattern:
                self._add_pattern(p)
        else:
            self._add_pattern(pattern)

    # Add a pattern to the list of patterns
    def _add_pattern(self, pattern: "AnyStr | Pattern | None"):
        if isinstance(pattern, str | bytes):
            self._patterns.append(re.compile(pattern, flags=self._flags))
        elif isinstance(pattern, Pattern):
            self._patterns.append(pattern)
        else:
            assert pattern is None
            self._patterns.append(None)

    @overload
    def chain(self, pattern: AnyStr) -> "Pattern": ...
    @overload
    def chain(self, pattern: "Pattern") -> "Pattern": ...
    @overload
    def chain(self, pattern: List["AnyStr | Pattern | None"]) -> "Pattern": ...
    def chain(self: "Pattern", pattern):
        """ Chain the next Pattern elemenet to the end of the chain.
            Turns chain and list of pattern options into Pattern object."""
        p = self
        while p._next is not None:
            p = p._next
        p._next = Pattern(pattern, self._flags)
        return self

    def match(self, string: AnyStr, pos: int = 0) -> List[re.Match[AnyStr]] | None:
        """ Match string with pattern and return list of matches. """
        # Prep max counters
        p = self
        p._matched = 0
        while p._next is not None:
            p = p._next
            p._matched = 0

        # Match recursively
        return self._match(string, pos)
 
    def _match(self, string: AnyStr, pos: int = 0) -> List[re.Match[AnyStr]] | None:
        # Check for max counter
        if self._max > 0 and self._matched >= self._max:
            return None
 
        # Check each pattern
        for pattern in self._patterns:
            # For null pattern, always match
            if pattern is None:
                return []

            # For regex pattern, try to match
            elif isinstance(pattern, re.Pattern):
                m = pattern.match(string, pos=pos)
 
                # If match, get position and save result to list
                if m is not None:
                    pos = m.end()
                    m = [m]
                    break

            # For Pattren, try to match recursively
            else:
                assert isinstance(pattern, Pattern)
                m = pattern._match(string, pos=pos)

                # If match, get position
                if m is not None:
                    pos = m[-1].end()
                    break

        # If no match, return None
        else:
            return None

        # match found, increment counter
        self._matched += 1
 
        # If a pattern matched, and there is next
        if self._next is not None:
            # Get match of next elelemnt recursively
            n = self._next._match(string, pos=pos)
            if n is not None:
                # Return concatenated matches
                return m + n

            # If next does not match, no complete match
            else:
                return None

        # If no next, return matches of pattern
        return m

def compile(pattern: AnyStr | List[AnyStr | Pattern | None], flags: int | re.RegexFlag = 0, max: int = 0) -> Pattern:
    return Pattern(pattern, flags, max=max)
