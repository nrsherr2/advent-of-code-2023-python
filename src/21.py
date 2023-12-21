from utils.api import get_input, get_test_input, print_hlight, print_tlight
import time

current_day = 21
input_str = get_input(current_day)
test_str = get_test_input(current_day)


def part1(fullInput, numSteps):
    staringLoc, rocLocs = parseInput(fullInput)
    # start on 1 for even numbers, 0 for odd
    currentLocs = set()
    currentLocs.add(staringLoc)
    for i in range(numSteps):
        newLocs = set()
        for loc in currentLocs:
            for d in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                nl = (loc[0] + d[0], loc[1] + d[1])
                if nl not in rocLocs:
                    newLocs.add(nl)
        currentLocs = newLocs
    return len(currentLocs)


def part2(fullInput):
    print(fullInput)


def genDiamond(step, startingLoc):
    points = set()
    for i in range(-1 * step, step + 1):
        j = step - abs(i)
        j1 = -1 * j
        points.add((startingLoc[0] + i, startingLoc[1] + j))
        points.add((startingLoc[0] + i, startingLoc[1] + j1))
    return points


def parseInput(fullInput):
    rocLocs = set()
    startingLoc = None
    for rowNum, row in enumerate(fullInput.splitlines()):
        for colNum, c in enumerate(row):
            if c == 'S':
                startingLoc = (rowNum, colNum)
            elif c == '#':
                rocLocs.add((rowNum, colNum))
    return startingLoc, rocLocs


# solutions corner

startTime = time.time()

part1Test = part1(test_str, 6)
part1TestExpected = 16
if part1Test != part1TestExpected:
    raise Exception(part1TestExpected, part1Test)
print_hlight(part1(input_str, 64))

part2Test = part2(test_str)
print_hlight(part2(input_str))

print_tlight("--- %s seconds ---" % (time.time() - startTime))
