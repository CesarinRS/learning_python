def delete_double_zero(*args):
    for i in range(len(args) - 1):
        if args[i] == 0 and args[i + 1] == 0:
            return True
    return False

print(delete_double_zero(12,0,5,10,15,8,0,9,8,5,6,0))