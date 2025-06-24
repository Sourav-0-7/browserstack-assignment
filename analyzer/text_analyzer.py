from collections import Counter
import re

def analyze(headers):
    words = []
    for h in headers:
        words += re.findall(r'\w+', h.lower())
    ctr = Counter(words)
    return {w: c for w, c in ctr.items() if c > 2}
