from utils.api import get_input, get_test_input, print_hlight, print_tlight
import time
from enum import Enum

current_day = 10
input_str = get_input(current_day)
test_str = get_test_input(current_day)
test2 = get_test_input(101)
test3 = get_test_input(102)
test4 = get_test_input(103)

connNorth = ['S', '|', 'L', 'J']
connEast = ['S', 'L', '-', 'F']
connWest = ['S', '-', '7', 'J']
connSouth = ['|', '7', 'F', 'S']


def part1(fullInput):
    startI, startJ = None, None
    lines = fullInput.splitlines()
    for i in range(len(lines)):
        for j in range(len(lines[i])):
            if lines[i][j] == 'S':
                startI, startJ = i, j
                break
        if startI:
            break

    currentNodes = [(startI, startJ)]
    visitedNodes = currentNodes
    currentStep = 0
    while currentNodes:
        # print(currentNodes)
        newNodes = []
        for si, sj in currentNodes:
            ltr = lines[si][sj]
            # print(si, sj, ltr)
            if ltr in connNorth:
                nLoc = (si - 1, sj)
                northChar = getOrNull(nLoc[0], nLoc[1], lines)
                if northChar and northChar in connSouth and nLoc not in newNodes and nLoc not in visitedNodes:
                    newNodes.append(nLoc)
            if ltr in connEast:
                eLoc = (si, sj + 1)
                eastChar = getOrNull(eLoc[0], eLoc[1], lines)
                if eastChar and eastChar in connWest and eLoc not in newNodes and eLoc not in visitedNodes:
                    newNodes.append(eLoc)
            if ltr in connSouth:
                sLoc = (si + 1, sj)
                southChar = getOrNull(sLoc[0], sLoc[1], lines)
                if southChar and southChar in connNorth and sLoc not in newNodes and sLoc not in visitedNodes:
                    newNodes.append(sLoc)
            if ltr in connWest:
                wLoc = (si, sj - 1)
                westChar = getOrNull(wLoc[0], wLoc[1], lines)
                if westChar and westChar in connEast and wLoc not in newNodes and wLoc not in visitedNodes:
                    newNodes.append(wLoc)
        if newNodes:
            currentStep += 1
        visitedNodes = visitedNodes + newNodes
        currentNodes = newNodes
    # print(visitedNodes)
    return currentStep


def getOrNull(i, j, lines):
    if 0 <= i < len(lines) and 0 <= j < len(lines[i]):
        return lines[i][j]
    else:
        return None


def part2(fullInput):
    startI, startJ = None, None
    lines = fullInput.splitlines()
    for i in range(len(lines)):
        for j in range(len(lines[i])):
            if lines[i][j] == 'S':
                startI, startJ = i, j
                break
        if startI:
            break

    currentNodes = [(startI, startJ)]
    pipes = currentNodes
    currentStep = 0
    while currentNodes:
        # print(currentNodes)
        newNodes = []
        for si, sj in currentNodes:
            ltr = lines[si][sj]
            # print(si, sj, ltr)
            if ltr in connNorth:
                nLoc = (si - 1, sj)
                northChar = getOrNull(nLoc[0], nLoc[1], lines)
                if northChar and northChar in connSouth and nLoc not in newNodes and nLoc not in pipes:
                    newNodes.append(nLoc)
            if ltr in connEast:
                eLoc = (si, sj + 1)
                eastChar = getOrNull(eLoc[0], eLoc[1], lines)
                if eastChar and eastChar in connWest and eLoc not in newNodes and eLoc not in pipes:
                    newNodes.append(eLoc)
            if ltr in connSouth:
                sLoc = (si + 1, sj)
                southChar = getOrNull(sLoc[0], sLoc[1], lines)
                if southChar and southChar in connNorth and sLoc not in newNodes and sLoc not in pipes:
                    newNodes.append(sLoc)
            if ltr in connWest:
                wLoc = (si, sj - 1)
                westChar = getOrNull(wLoc[0], wLoc[1], lines)
                if westChar and westChar in connEast and wLoc not in newNodes and wLoc not in pipes:
                    newNodes.append(wLoc)
        if newNodes:
            currentStep += 1
        pipes = pipes + newNodes
        currentNodes = newNodes
    lines[startI] = lines[startI].replace('S', determineDirectionOfS(startI, startJ, lines))

    currentPipe = (len(lines), len(lines[0]))
    for p in pipes:
        if lines[p[0]][p[1]] == '|' and p[1] <= currentPipe[1]:
            currentPipe = p
    usedPipes = []
    direction = 'd'
    bugLocs = set()
    while currentPipe not in usedPipes:
        testLoc = None
        nextLoc = None
        if direction == 'd':
            nextLoc = (currentPipe[0] + 1, currentPipe[1])
            testLoc = (currentPipe[0], currentPipe[1] - 1)
        if direction == 'u':
            nextLoc = (currentPipe[0] - 1, currentPipe[1])
            testLoc = (currentPipe[0], currentPipe[1] + 1)
        if direction == 'r':
            nextLoc = (currentPipe[0], currentPipe[1] + 1)
            testLoc = (currentPipe[0] + 1, currentPipe[1])
        if direction == 'l':
            nextLoc = (currentPipe[0], currentPipe[1] - 1)
            testLoc = (currentPipe[0] - 1, currentPipe[1])

        if 0 <= testLoc[0] < len(lines) and 0 <= testLoc[1] < len(lines[0]) and testLoc not in pipes:
            bugLocs.add(testLoc)

        usedPipes.append(currentPipe)
        currentPipe = nextLoc
        charAtNext = lines[currentPipe[0]][currentPipe[1]]
        if charAtNext == 'J':
            if direction == 'd':
                direction = 'l'
                testLoc = (currentPipe[0], currentPipe[1] - 1)
            elif direction == 'r':
                direction = 'u'
                testLoc = (currentPipe[0] + 1, currentPipe[1])
        elif charAtNext == 'L':
            if direction == 'd':
                direction = 'r'
                testLoc = (currentPipe[0], currentPipe[1] - 1)
            elif direction == 'l':
                direction = 'u'
                testLoc = (currentPipe[0] - 1, currentPipe[1])
        elif charAtNext == '7':
            if direction == 'r':
                direction = 'd'
                testLoc = (currentPipe[0] + 1, currentPipe[1])
            elif direction == 'u':
                direction = 'l'
                testLoc = (currentPipe[0], currentPipe[1] + 1)
        elif charAtNext == 'F':
            if direction == 'u':
                direction = 'r'
                testLoc = (currentPipe[0], currentPipe[1] + 1)
            elif direction == 'l':
                direction = 'd'
                testLoc = (currentPipe[0] - 1, currentPipe[1])
        if 0 <= testLoc[0] < len(lines) and 0 <= testLoc[1] < len(lines[0]) and testLoc not in pipes:
            bugLocs.add(testLoc)
    activeThisRound = set() | bugLocs
    while activeThisRound:
        # print(len(activeThisRound))
        newRound = set()
        for b in activeThisRound:
            for i in range(-1, 2):
                for j in range(-1, 2):
                    testLoc = (b[0] + i, b[1] + j)
                    if 0 <= testLoc[0] < len(lines) and 0 <= testLoc[1] < len(
                            lines[0]) and testLoc not in pipes and testLoc not in bugLocs:
                        bugLocs.add(testLoc)
                        newRound.add(testLoc)
        activeThisRound = newRound
    freeLocs = 0
    for i in range(len(lines)):
        for j in range(len(lines[i])):
            if (i, j) not in pipes and (i, j) not in bugLocs:
                freeLocs += 1
    # s = ''
    # for i in range(len(lines)):
    #     for j in range(len(lines[i])):
    #         myC = lines[i][j]
    #         if (i, j) in pipes and (i, j) in bugLocs:
    #             s += '\033[41m{}\033[0m'.format(myC)
    #         elif (i, j) in pipes:
    #             s += '\033[36m{}\033[0m'.format(myC)
    #         elif (i, j) in bugLocs:
    #             s += '\033[30m{}\033[0m'.format(myC)
    #         else:
    #             s += '\033[95m{}\033[0m'.format(myC)
    #             freeLocs += 1
    #     s += '\n'
    #
    # print(s)
    return freeLocs


def determineDirectionOfS(startI, startJ, lines):
    connectsBot = lines[startI + 1][startJ] in ['J', '|', 'L']
    connectsTop = lines[startI - 1][startJ] in ['7', '|', 'F']
    if connectsBot and connectsTop:
        return '|'
    connectsRight = lines[startI][startJ + 1] in ['J', '-', '7']
    if connectsBot and connectsRight:
        return 'F'
    if connectsTop and connectsRight:
        return 'L'
    connectsLeft = lines[startI][startJ - 1] in ['L', '-', 'F']
    if connectsLeft and connectsRight:
        return '-'
    if connectsBot and connectsLeft:
        return '7'
    if connectsTop and connectsLeft:
        return 'J'
    return 'S'


# solutions corner

startTime = time.time()

part1Test = part1(test_str)
part1TestExpected = 8
if part1Test != part1TestExpected:
    raise Exception(part1TestExpected, part1Test)
print_hlight(part1(input_str))

for (testStr, expected) in [(test2, 4), (test3, 8), (test4, 10)]:
    part2Test = part2(testStr)
    if part2Test != expected:
        raise Exception(expected, part2Test)
print_hlight(part2(input_str))

print_tlight("--- %s seconds ---" % (time.time() - startTime))
