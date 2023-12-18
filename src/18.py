from utils.api import get_input, get_test_input, print_hlight, print_tlight
import time

current_day = 18
input_str = get_input(current_day)
test_str = get_test_input(current_day)


def part1(fullInput):
    location = (0, 0)
    locs = set()
    # going to take a wild guess and paint right side
    insideLocs = set()
    locs.add(location)
    for line in fullInput.splitlines():
        dir_, amt, _ = line.split()
        trns = {'R': (0, 1), 'L': (0, -1), 'U': (-1, 0), 'D': (1, 0)}[dir_]
        pntLoc = {'R': (1, 0), 'L': (-1, 0), 'U': (0, 1), 'D': (0, -1)}[dir_]
        for i in range(int(amt)):
            location = (location[0] + trns[0], location[1] + trns[1])
            insideLocs.add((location[0] + pntLoc[0], location[1] + pntLoc[1]))
            locs.add(location)
    insideLocs = insideLocs - locs
    workingLocs = insideLocs.copy()
    while workingLocs:
        w = set()
        for loc in workingLocs.copy():
            for (i, j) in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                trns = (loc[0] + i, loc[1] + j)
                if trns not in insideLocs and trns not in locs:
                    w.add(trns)
        workingLocs = w
        insideLocs = insideLocs | workingLocs
    # s = ''
    # for i in range(minRow, maxRow + 1):
    #     for j in range(minCol, maxCol + 1):
    #         if (i, j) in locs:
    #             s += '\033[96m#\033[0m'
    #         elif (i, j) in insideLocs:
    #             s += '\033[95m#\033[0m'
    #         else:
    #             s += '\033[30m.\033[0m'
    #     s += '\n'
    # print(s)
    return len(insideLocs) + len(locs)


def part2(fullInput):
    print(fullInput)


# solutions corner

startTime = time.time()

part1Test = part1(test_str)
part1TestExpected = 62
if part1Test != part1TestExpected:
    raise Exception(part1Test, part1TestExpected)
print_hlight(part1(input_str))

# part2Test = part2(test_str)
# print_hlight(part2(input_str))

print_tlight("--- %s seconds ---" % (time.time() - startTime))
