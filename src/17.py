import heapq

from utils.api import get_input, get_test_input, print_hlight, print_tlight
import time

current_day = 17
input_str = get_input(current_day)
test_str = get_test_input(current_day)


def part1(fullInput):
    return solve(fullInput, 1)


def solve(fullInput, part):
    lines = fullInput.splitlines()
    nums = [[c for c in row] for row in lines]
    numRows = len(nums)
    numCols = len(nums[0])
    queue = [(0, 0, 0, -1, -1)]
    nodes = {}
    while queue:
        distance, rowNum, colNum, outDir, stepsInCurrDir = heapq.heappop(queue)
        if (rowNum, colNum, outDir, stepsInCurrDir) in nodes:
            continue
        nodes[(rowNum, colNum, outDir, stepsInCurrDir)] = distance
        for i, (dRow, dCol) in enumerate([[-1, 0], [0, 1], [1, 0], [0, -1]]):
            moddedRow = rowNum + dRow
            moddedCol = colNum + dCol
            newDirectionOut = i
            newStepsInCurr = 1 if newDirectionOut != outDir else stepsInCurrDir + 1
            isNotReversing = ((newDirectionOut + 2) % 4 != outDir)
            isValid = (newStepsInCurr <= 3) if part == 1 else (newStepsInCurr <= 10 and (newDirectionOut == outDir or stepsInCurrDir >= 4 or stepsInCurrDir == -1))
            if 0 <= moddedRow < numRows and 0 <= moddedCol < numCols and isNotReversing and isValid:
                cost = int(nums[moddedRow][moddedCol])
                if (moddedRow, moddedCol, newDirectionOut, newStepsInCurr) in nodes:
                    continue
                heapq.heappush(queue, (distance + cost, moddedRow, moddedCol, newDirectionOut, newStepsInCurr))
    res = 1e6
    for (row, col, otdur, stidir), v in nodes.items():
        if (row, col) == (numRows - 1, numCols - 1):
            res = min(res, v)
    return res


def part2(fullInput):
    return solve(fullInput,2)




# solutions corner

startTime = time.time()

part1Test = part1(test_str)
part1TestExpected = 102
if part1Test != part1TestExpected:
    raise Exception(part1Test, part1TestExpected)
print_hlight(part1(input_str))

part2Test = part2(test_str)
part2TestExpected = 94
if part2Test != part2TestExpected:
    raise Exception(part2Test, part2TestExpected)
print_hlight(part2(input_str))

print_tlight("--- %s seconds ---" % (time.time() - startTime))
