from utils.api import get_input, get_test_input, print_hlight, print_tlight
import time

current_day = 21
input_str = get_input(current_day)
test_str = get_test_input(current_day)


def part1(fullInput, numSteps):
    staringLoc, rocLocs = parseInput(fullInput)
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
    # calculate the number of spaces if we can freely move an even number of steps
    numEvenInFull = part1(fullInput, 130)
    # calculate the number of spaces if we can free move an odd number of steps
    numOddInFull = part1(fullInput, 131)
    numLines = len(fullInput.splitlines())
    numCols = len(fullInput.splitlines()[0])
    _, rocLocs = parseInput(fullInput)
    lPoints = calcLocs(131, numLines, numCols, {(65, 0)}, rocLocs)
    lScore = len(lPoints)

    rPoints = calcLocs(131, numLines, numCols, {(65, 130)}, rocLocs)
    rScore = len(rPoints)

    bPoints = calcLocs(131, numLines, numCols, {(130, 65)}, rocLocs)
    bScore = len(bPoints)

    tPoints = calcLocs(131, numLines, numCols, {(0, 65)}, rocLocs)
    tScore = len(tPoints)

    lbPoints = lPoints.union(bPoints)
    lbScore = len(lbPoints)

    ltPoints = lPoints.union(tPoints)
    ltScore = len(ltPoints)

    rtPoints = rPoints.union(tPoints)
    rtScore = len(rtPoints)

    rbPoints = rPoints.union(bPoints)
    rbScore = len(rbPoints)

    numStepsLeft = 26501365
    totalCurrentPoints = numOddInFull
    totalCurrentPoints += parallelUniverseVert(numEvenInFull, numOddInFull, tScore, numStepsLeft - 65, True)
    totalCurrentPoints += parallelUniverseVert(numEvenInFull, numOddInFull, bScore, numStepsLeft - 65, True)
    totalCurrentPoints += parallelUniverseHoriz(numEvenInFull, numOddInFull, rScore, rtScore, rbScore,
                                                numStepsLeft - 65, True)
    totalCurrentPoints += parallelUniverseHoriz(numEvenInFull, numOddInFull, lScore, ltScore, lbScore,
                                                numStepsLeft - 65, True)
    # totalCurrentPoints = (numOddInFull
    #                       + parallelUniverseVert(numEvenInFull, numOddInFull, tScore, numStepsLeft - 65, True)
    #                       + parallelUniverseVert(numEvenInFull, numOddInFull, bScore, numStepsLeft - 65, True)
    #                       + parallelUniverseHoriz(numEvenInFull, numOddInFull, rScore, rtScore, rbScore,
    #                                               numStepsLeft - 65, True)
    #                       + parallelUniverseHoriz(numEvenInFull, numOddInFull, lScore, ltScore, lbScore,
    #                                               numStepsLeft - 65, True))
    return totalCurrentPoints


def parallelUniverseHoriz(numEvenInFull, numOddInFull, hScore, htScore, hbScore, stepsLeft, evenStep):
    s = stepsLeft
    sc = 0
    es = evenStep
    print(s)
    while s > 131:
        if str(s)[-2:] == '00':
            print(s)
        thisScore = numEvenInFull if evenStep else numOddInFull
        uScore = parallelUniverseVert(numEvenInFull, numOddInFull, htScore, s - 131, not evenStep)
        lScore = parallelUniverseVert(numEvenInFull, numOddInFull, hbScore, s - 131, not evenStep)
        sc += (thisScore + uScore + lScore)
        es = not es
        s -= 131
    return sc + hScore
    # thisScore = numEvenInFull if evenStep else numOddInFull
    # print(stepsLeft)
    # if stepsLeft > 131:
    #     return (thisScore
    #             + parallelUniverseHoriz(numEvenInFull, numOddInFull, hScore, htScore, hbScore, stepsLeft - 131,
    #                                     not evenStep)
    #             + parallelUniverseVert(numEvenInFull, numOddInFull, htScore, stepsLeft - 131, not evenStep)
    #             + parallelUniverseVert(numEvenInFull, numOddInFull, hbScore, stepsLeft - 131, not evenStep))
    # else:
    #     return hScore


def parallelUniverseVert(numEvenInFull, numOddInFull, nScore, stepsLeft, evenStep):
    s = stepsLeft
    sc = 0
    es = evenStep
    while s > 131:
        thisScore = numEvenInFull if evenStep else numOddInFull
        sc += thisScore
        es = not es
        s -= 131
    score1 = sc + nScore
    # (numLeft1, numLeft2)= divmod(stepsLeft,131)
    # if evenStep:
    #     score2 = numLeft1 * numEvenInFull + numLeft2 * numOddInFull + nScore
    # else:
    #     score2 = numLeft1 * numOddInFull + numLeft2 * numEvenInFull + nScore
    # if(score1 != score2):
    #     raise Exception(score1,score2)
    return score1
    # thisScore = numEvenInFull if evenStep else numOddInFull
    # print(stepsLeft)
    # if stepsLeft > 131:
    #     return thisScore + parallelUniverseVert(numEvenInFull, numOddInFull, nScore, stepsLeft - 131, not evenStep)
    # else:
    #     return nScore


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
