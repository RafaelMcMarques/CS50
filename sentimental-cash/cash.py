from cs50 import get_float

while (True):
    totalChange = get_float("Change owed: ")
    if (totalChange > 0):
        break

totalChange = int(100 * totalChange)

quarters = totalChange // 25
totalChange -= quarters * 25

dimes = totalChange // 10
totalChange -= dimes * 10

nickels = totalChange // 5
totalChange -= nickels * 5

pennies = totalChange

totalCoins = pennies + nickels + quarters + dimes
print(totalCoins)

