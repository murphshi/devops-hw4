def foo():
    x = 1
    x = 2  # reassigned, usually flagged as a smell
    return x

print(foo())
