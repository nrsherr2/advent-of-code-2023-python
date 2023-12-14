from utils.api import get_input, get_test_input, print_hlight, print_tlight
import time
from queue import Queue

current_day = 14
input_str = get_input(current_day)
test_str = get_test_input(current_day)


def tiltEntry(pebbs, cubes, tableLength, tableWidth, direction):
    if direction == 'N':
        return tiltNorth(pebbs, cubes)
    elif direction == 'E':
        return tiltEast(pebbs, cubes, tableWidth)
    elif direction == 'S':
        return tiltSouth(pebbs, cubes, tableLength)
    elif direction == 'W':
        return tiltWest(pebbs, cubes)
    else:
        raise Exception('INVALID DIRECTION')


def tilt(pebbs, cubes, transformation, outOfBoundsCheck):
    pbs = pebbs.copy()

    newPebs = []
    for peb in pbs:
        oldLoc = peb
        testLoc = (peb[0] + transformation[0], peb[1] + transformation[1])
        while outOfBoundsCheck(testLoc) and testLoc not in newPebs and testLoc not in cubes:
            oldLoc = testLoc
            testLoc = (testLoc[0] + transformation[0], testLoc[1] + transformation[1])
        newPebs.append(oldLoc)
        pbs = newPebs
    if not all(map(lambda x: outOfBoundsCheck(x), pbs)):
        raise Exception()
    return pbs


def tiltNorth(pebbs, cubes):
    pebbs = sorted(pebbs, key=lambda x: x[0])
    return tilt(pebbs, cubes, (-1, 0), lambda x: x[0] >= 0)


def tiltWest(pebbs, cubes):
    pebbs = sorted(pebbs, key=lambda x: x[1])
    return tilt(pebbs, cubes, (0, -1), lambda x: x[1] >= 0)


def tiltSouth(pebbs, cubes, tableLength):
    pebbs = sorted(pebbs, key=lambda x: x[0], reverse=True)
    return tilt(pebbs, cubes, (1, 0), lambda x: x[0] < tableLength)


def tiltEast(pebbs, cubes, tableWidth):
    pebbs = sorted(pebbs, key=lambda x: x[1], reverse=True)
    return tilt(pebbs, cubes, (0, 1), lambda x: x[1] < tableWidth)


def parseInput(fullInput):
    lines = fullInput.splitlines()
    tableLen = len(lines)
    tableWidth = len(lines[0])
    pebbs = []
    cubes = []
    for rowNum, line in enumerate(lines):
        for colNum, char in enumerate(line):
            if char == '#':
                cubes.append((rowNum, colNum))
            elif char == 'O':
                pebbs.append((rowNum, colNum))
    return tableLen, tableWidth, pebbs, cubes


def rotate(queue):
    q = queue.get()
    queue.put(q)
    return q


def part1(fullInput):
    tableLen, tableWidth, pebbs, cubes = parseInput(fullInput)
    pebbs = tiltNorth(pebbs, cubes)
    return sum(map(lambda x: tableLen - x[0], pebbs))


def part2(fullInput, totalSteps=1_000_000_000):
    tableLen, tableWidth, pebbs, cubes = parseInput(fullInput)
    states = []
    step = 0
    patternStart = None
    otherCondition = True
    while step < totalSteps:
        step += 1
        for pebState, oStep in states:
            # taken from my day 17 solution last year
            if all(map(lambda x: x in pebState, pebbs)):
                print('cycle between', oStep, 'and', step)
                ps = step
                if not patternStart:
                    patternStart = ps
                    states = []
                elif otherCondition:
                    stepsPerCycle = ps - patternStart
                    stepsLeft = totalSteps - step
                    numPatternsLeft, stepsLeftOver = divmod(stepsLeft, stepsPerCycle)
                    step = totalSteps - stepsLeftOver
                    # print(ps, patternStart, stepsPerCycle, stepsLeft, numPatternsLeft, stepsLeftOver, step)
                    otherCondition = False
                break
        states.append((pebbs, step))
        for direction in ['N', 'W', 'S', 'E']:
            pebbs = tiltEntry(pebbs, cubes, tableLen, tableWidth, direction)
        # print('rotation', step, ':', sum(map(lambda x: tableLen - x[0], pebbs)))

    return sum(map(lambda x: tableLen - x[0], pebbs))


# solutions corner

startTime = time.time()

part1Test = part1(test_str)
part1TestExpected = 136
if part1Test != part1TestExpected:
    raise Exception(part1TestExpected, part1Test)
print_hlight(part1(input_str))

part2Test = part2(test_str)
part2TestExpected = 64
if part2Test != part2TestExpected:
    raise Exception(part2TestExpected, part2Test)
print_hlight(part2(input_str))

print_tlight("--- %s seconds ---" % (time.time() - startTime))
