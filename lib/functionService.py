import re



def findall(pattern, string):
    result = []
    pos = 0
    while True:
        m = re.search(pattern, string[pos:])
        if not m:
            break
        result.append(m.groups())
        pos += m.end()
    return result