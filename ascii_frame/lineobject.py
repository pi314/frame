import re

from unicodedata import east_asian_width
# for more information, see http://unicode.org/reports/tr11/


class LineObject:
    @classmethod
    def uwidth(cls, c):
        return 1 + (east_asian_width(c) in 'WF')

    def __init__(self, text):
        self.text = re.sub(r'\x1b\[[^hm]*[hm]', '', text.rstrip())

    @property
    def width(self):
        return sum(1 + (east_asian_width(c) in 'WF') for c in self.text)

    def wrap(self, width):
        w, ret = 0, ''
        for c in self.text:
            if w + self.uwidth(c) > width and w > 0:
                yield LineObject(ret)
                w, ret = 0, ''

            w, ret = w + self.uwidth(c), ret + c

        yield LineObject(ret)

    def __str__(self):
        return self.text

    def __eq__(self, other):
        if isinstance(other, str):
            return self.text == other

        if isinstance(other, LineObject):
            return self.text == other.text

        return str(self) == str(other)
