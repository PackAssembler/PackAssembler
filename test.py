try:
    num1 = int(input("Number 1: "))
    num2 = int(input("Number 2: "))
except ValueError:
    print("DIE!!!")
    exit()
print(num1+num2)
