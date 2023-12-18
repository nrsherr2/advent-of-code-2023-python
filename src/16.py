from utils.api import get_input, get_test_input, print_hlight, print_tlight
import time

current_day = 16
input_str = get_input(current_day)
test_str = get_test_input(current_day)


def getTestLoc(cb):
    if cb[1] == 'R':
        return cb[0][0], cb[0][1] + 1
    elif cb[1] == 'D':
        return cb[0][0] + 1, cb[0][1]
    elif cb[1] == 'L':
        return cb[0][0], cb[0][1] - 1
    elif cb[1] == 'U':
        return cb[0][0] - 1, cb[0][1]
    else:
        raise Exception()


def determineDirections(currentDirection, charAtLoc):
    if charAtLoc == '.':
        return [currentDirection]
    elif charAtLoc == '\\':
        return [{'R': 'D', 'U': 'L', 'D': 'R', 'L': 'U'}[currentDirection]]
    elif charAtLoc == '/':
        return [{'R': 'U', 'D': 'L', 'L': 'D', 'U': 'R'}[currentDirection]]
    elif charAtLoc == '-':
        if currentDirection in ['R', 'L']:
            return [currentDirection]
        else:
            return ['L', 'R']
    elif charAtLoc == '|':
        if currentDirection in ['U', 'D']:
            return [currentDirection]
        else:
            return ['U', 'D']


def lightShow(grid, currentBeams):
    visited = {}
    while currentBeams:
        nBeams = []
        for cb in currentBeams:
            testLoc = getTestLoc(cb)
            if not (0 <= testLoc[0] < len(grid) and 0 <= testLoc[1] < len(grid[0])):
                continue
            charAtLoc = grid[testLoc[0]][testLoc[1]]
            directions = determineDirections(cb[1], charAtLoc)
            for direction in directions:
                if direction not in visited.get(testLoc, []):
                    visited[testLoc] = visited.get(testLoc, []) + [direction]
                    nBeams.append((testLoc, direction))
        currentBeams = nBeams
    return len(visited)


def part1(fullInput):
    grid = fullInput.splitlines()
    currentBeams = [((0, -1), 'R')]
    return lightShow(grid, currentBeams)


def part2(fullInput):
    grid = fullInput.splitlines()
    starts = []
    for i in range(len(grid)):
        starts.append([((i, -1), 'R')])
        starts.append([((i, len(grid[0])), 'L')])
    for j in range(len(grid[0])):
        starts.append([((-1, j), 'D')])
        starts.append([((len(grid), j), 'U')])
    return max(map(lambda x: lightShow(grid, x), starts))


# solutions corner

startTime = time.time()

part1Test = part1(test_str)
part1TestExpected = 46
if part1Test != part1TestExpected:
    raise Exception(part1Test, part1TestExpected)
print_hlight(part1(input_str))

part2Test = part2(test_str)
part2TestExpected = 51
if part2Test != part2TestExpected:
    raise Exception(part2Test, part2TestExpected)
print_hlight(part2(input_str))

print_tlight("--- %s seconds ---" % (time.time() - startTime))
