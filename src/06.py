from utils.api import get_input, get_test_input
import time
import math

current_day = 6
input_str = get_input(current_day)
test_str = get_test_input(current_day)


def part1(fullInput):
    (times, distances) = list(map(lambda x: x.split(':')[1].split(), fullInput.splitlines()))
    tuples = [(float(times[i]), float(distances[i])) for i in range(0, len(times))]
    iteratore = 1
    for (gTime, goal) in tuples:
        numWins = calcNumWins(gTime, goal)
        iteratore = iteratore * numWins
    return iteratore


def calcNumWins(givenTime, goal):
    (lowerBound, upperBound) = solveQuadratic(givenTime, goal)
    if math.ceil(lowerBound) == lowerBound:
        lowerBound += 1
    if math.floor(upperBound) == upperBound:
        upperBound -= 1
    lowerBound = int(math.ceil(lowerBound))
    upperBound = int(math.floor(upperBound))
    numWins = len(range(lowerBound, upperBound)) + 1
    return numWins


def part2(fullInput):
    (gTime, distance) = list(map(lambda x: x.split(':')[1].replace(' ', ''), fullInput.splitlines()))
    return int(calcNumWins(float(gTime), float(distance)))


def solveQuadratic(b, c):
    plusSq = ((-1 * b) + math.sqrt(math.pow(b, 2) - (4 * c))) / -2
    minusSq = ((-1 * b) - math.sqrt(math.pow(b, 2) - (4 * c))) / -2
    return sorted([plusSq, minusSq])


startTime = time.time()
# WRITE YOUR SOLUTION HERE

part1Test = part1(test_str)
part1TestExpected = 288
if part1Test != part1TestExpected:
    raise Exception(part1Test, part1TestExpected)

print(part1(input_str))

part2Test = part2(test_str)
part2TestExpected = 71503
if part2Test != part2TestExpected:
    raise Exception(part2Test, part2TestExpected)

print(part2(input_str))

print("--- %s seconds ---" % (time.time() - startTime))
