from utils.api import get_input, get_test_input
import time

current_day = 4
input_str = get_input(current_day)
test_str = get_test_input(current_day)


def part1(fullText):
    runningTotal = 0
    for line in fullText.splitlines():
        currTotal = 0
        (winningSon, mySon) = line.split(":")[1].split("|")
        winningNums = winningSon.split()
        for num in mySon.split():
            if num in winningNums:
                if currTotal == 0:
                    currTotal = 1
                else:
                    currTotal = currTotal * 2
        runningTotal += currTotal
    return runningTotal


def part2(fullText):
    buckets = list(map(lambda x: (x, 1), fullText.splitlines()))
    print(buckets)
    for i in range(0, len(buckets)):
        buck = buckets[i]
        line = buck[0]
        count = 0
        (winningSon, mySon) = line.split(":")[1].split("|")
        winningNums = winningSon.split()
        for num in mySon.split():
            if num in winningNums:
                count += 1
        if count > 0:
            for j in range(i + 1, i + 1 + count):
                buckets[j] = (buckets[j][0], buckets[j][1] + buck[1])
    return sum(list(map(lambda x: x[1], buckets)))


part1TestExpected = 13
part1Test = part1(test_str)
if part1Test != part1TestExpected:
    raise Exception("TEST FAILED! Expected {exp}, Got {rel}".format(exp=part1TestExpected, rel=part1Test))

part2TestExpected = 30
part2Test = part2(test_str)
if part2Test != part2TestExpected:
    raise Exception("TEST FAILED! Expected {exp}, Got {rel}".format(exp=part2TestExpected, rel=part2Test))

startTime = time.time()
# WRITE YOUR SOLUTION HERE

part1Real = part1(input_str)
part2Real = part2(input_str)

print(part1Real)
print(part2Real)

print("--- %s seconds ---" % (time.time() - startTime))
