import sys
import re

def extract_strings(filename, min_length=4):
    with open(filename, "rb") as f:
        data = f.read()

    # ASCII and Latin-1ish strings
    ascii_pattern = re.compile(b'[ -~]{%d,}' % min_length)
    for match in ascii_pattern.finditer(data):
        yield match.group(0).decode('ascii', errors='ignore')

    # UTF-16LE strings
    # We look for printable ascii chars separated by null bytes
    # e.g. b'C\x00T\x00O\x00'
    utf16_pattern = re.compile(b'(?:[ -~]\x00){%d,}' % min_length)
    for match in utf16_pattern.finditer(data):
        yield match.group(0).decode('utf-16le', errors='ignore')

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: strings.py <file>")
        sys.exit(1)
        
    found = set()
    for s in extract_strings(sys.argv[1]):
        s = s.strip()
        if len(s) >= 4:
            found.add(s)
            
    for s in sorted(list(found)):
        print(s)
