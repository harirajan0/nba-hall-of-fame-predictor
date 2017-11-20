alpha = "abcdefghijklmnopqrstuvwxyz"

def is_numeric(s):
    if len(s.strip()) == 0:
        return False
    for ch in alpha:
        if s.strip().lower().contains(ch):
            return False
    return True