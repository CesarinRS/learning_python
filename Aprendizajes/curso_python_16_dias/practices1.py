def reorganized(name):
    name = str(name).lower()
    list1 = sorted(set(name))
    return list1

print(reorganized("AbeCedario"))