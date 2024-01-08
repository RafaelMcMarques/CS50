from cs50 import get_int

while (True) :
    size = get_int("height: ")
    if (size < 9 and size > 0):
        break

for i in range(0, size):
    for k in range(1, size - i):
        print(" ",end="")

    for k in range(0, i+1):
        print("#",end="")

    print("  ", end="")

    for k in range(0, i+1):
        print("#",end="")
    print()



