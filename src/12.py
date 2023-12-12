from functools import cache

from utils.api import get_input, get_test_input, print_hlight, print_tlight
import time

current_day = 12
input_str = get_input(current_day)
test_str = get_test_input(current_day)


def part1(fullInput):
    solnSizes = list(map(lambda x: picross(x), fullInput.splitlines()))
    return sum(solnSizes)


def part2(fullInput):
    solnSizes = []
    for line in fullInput.splitlines():
        l, r = line.split()
        lFold = [l] * 5
        ls = '?'.join(lFold)
        rFold = [r] * 5
        rs = ','.join(rFold)
        fullL = "{} {}".format(ls, rs)
        solnSizes.append(picross(fullL))
    return sum(solnSizes)


def picross(line):
    guide, rawNums = line.split()
    nums = list(map(lambda x: int(x), rawNums.split(',')))
    totalNumBoxes = len(guide)
    totalNumFilled = sum(nums)
    numDots = totalNumBoxes - totalNumFilled

    @cache
    def fillNum(currentString, numIdx, remainingDots, justPlacedBox):
        if len(currentString) == 0:
            return 1
        else:
            c = currentString[0]
            if c == '.' and remainingDots > 0:
                return fillNum(currentString[1:], numIdx, remainingDots - 1, False)
            elif c == '#' and numIdx < len(nums) and not justPlacedBox:
                num = nums[numIdx]
                if len(currentString) < num or not all(map(lambda x: x == '#' or x == '?', currentString[:num])):
                    return 0
                else:
                    return fillNum(currentString[num:], numIdx + 1, remainingDots, True)
            elif c == '?':
                dotSide = 0
                if remainingDots > 0:
                    dotSide = fillNum(currentString[1:], numIdx, remainingDots - 1, False)
                boxSide = 0
                if numIdx < len(nums) and not justPlacedBox:
                    num = nums[numIdx]
                    if len(currentString) >= num and all(map(lambda x: x == '#' or x == '?', currentString[:num])):
                        boxSide = fillNum(currentString[num:], numIdx + 1, remainingDots, True)
                return dotSide + boxSide
            else:
                return 0

    sols = fillNum(guide, 0, numDots, False)
    return sols


# solutions corner

startTime = time.time()

part1Test = part1(test_str)
part1TestExpected = 21
if part1Test != part1TestExpected:
    raise Exception(part1Test, part1TestExpected)
print_hlight(part1(input_str))
#
part2Test = part2(test_str)
part2TestExpected = 525152
if part2Test != part2TestExpected:
    raise Exception(part2Test, part2TestExpected)
print_hlight(part2(input_str))

print_tlight("--- %s seconds ---" % (time.time() - startTime))
