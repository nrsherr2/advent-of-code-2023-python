from utils.api import get_input, get_test_input, print_hlight, print_tlight
import time

current_day = 21
input_str = get_input(current_day)
test_str = get_test_input(current_day)


def part1(fullInput, numSteps, startingLocation=None):
    staringLoc, rocLocs = parseInput(fullInput)
    if startingLocation:
        staringLoc = startingLocation
    currentLocs = set()
    currentLocs.add(staringLoc)
    numLines = len(fullInput.splitlines())
    numCols = len(fullInput.splitlines()[0])
    return len(calcLocs(numSteps, numLines, numCols, currentLocs, rocLocs))


def calcLocs(numSteps, numLines, numCols, currentLocs, rocLocs):
    for i in range(numSteps):
        newLocs = set()
        for loc in currentLocs:
            for d in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                nl = (loc[0] + d[0], loc[1] + d[1])
                if nl not in rocLocs and 0 <= nl[0] < numLines and 0 <= nl[1] < numCols:
                    newLocs.add(nl)
        currentLocs = newLocs
    return currentLocs


def part2(fullInput):
    # https://imgur.com/tq8bDre
    # assume grid is square
    lines = fullInput.splitlines()
    grid = [[c for c in row] for row in lines]
    width = len(lines)
    if len(lines) != len(grid[0]):
        raise Exception()
    startingLoc = ((width - 1) // 2, (width - 1) // 2)
    # figure out N
    numSteps = 26501365
    # expected 202300
    N = (numSteps - startingLoc[0]) // width
    print(len(grid))
    E = part1(fullInput, width * 3)
    O = part1(fullInput, width * 3 + 1)
    T = Tcalc(fullInput, startingLoc, width)


def Tcalc(fullInput, startingLocation, width):
    T1 = part1(fullInput, width, (0, startingLocation[0]))
    T2 = part1(fullInput, width, (startingLocation[0], 0))
    T3 = part1(fullInput, width, (width - 1, startingLocation[0]))
    T4 = part1(fullInput, width, (startingLocation[0], width - 1))
    return T1 + T2 + T3 + T4


def parallelUniverseHoriz(numEvenInFull, numOddInFull, hScore, htScore, hbScore, stepsLeft, evenStep):
    s = stepsLeft
    sc = 0
    es = evenStep
    print(s)
    while s > 131:
        if str(s)[-2:] == '00':
            print(s)
        thisScore = numEvenInFull if es else numOddInFull
        uScore = parallelUniverseVert(numEvenInFull, numOddInFull, htScore, s - 131, not es)
        lScore = parallelUniverseVert(numEvenInFull, numOddInFull, hbScore, s - 131, not es)
        sc += (thisScore + uScore + lScore)
        es = not es
        s -= 131
    return sc + hScore


def parallelUniverseVert(numEvenInFull, numOddInFull, nScore, stepsLeft, evenStep):
    s = (stepsLeft - 131) / 131
    numB, leftOver = divmod(s, 2)
    numA = numB + leftOver
    if evenStep:
        scoreA = numA * numEvenInFull
        scoreB = numB * numOddInFull
    else:
        scoreA = numA * numOddInFull
        scoreB = numB * numEvenInFull
    return int(scoreA) + int(scoreB) + nScore


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

# part2Test = part2(test_str)
print_hlight(part2(input_str))

print_tlight("--- %s seconds ---" % (time.time() - startTime))
