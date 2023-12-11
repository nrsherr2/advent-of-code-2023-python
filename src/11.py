from utils.api import get_input, get_test_input, print_hlight, print_tlight
import time

current_day = 11
input_str = get_input(current_day)
test_str = get_test_input(current_day)


def part1(fullInput):
    lines = fullInput.splitlines()
    indicesToExpand = []
    for i in range(len(lines)):
        if all(map(lambda x: x == '.', lines[i])):
            indicesToExpand.append(i)
    insertString = ''
    for i in range(len(lines[0])):
        insertString += '.'
    for e in reversed(indicesToExpand):
        lines.insert(e, insertString)
    indicesToExpand = []
    for i in range(len(lines[0])):
        if all(map(lambda x: x[i] == '.', lines)):
            indicesToExpand.append(i)
    for e in reversed(indicesToExpand):
        lines = list(map(lambda x: x[:e] + '.' + x[e:], lines))
    starIndices = []
    for i in range(len(lines)):
        for j in range(len(lines[0])):
            if lines[i][j] != '.':
                starIndices.append((i, j))
    sums = []
    for i in range(len(starIndices) - 1):
        for j in range(i + 1, len(starIndices)):
            m = calcManhattanDistance(starIndices[i], starIndices[j])
            sums.append(m)
    return sum(sums)


def part2(fullInput, expansionFactor):
    lines = fullInput.splitlines()
    emptyRows = []
    emptyColumns = []
    for i in range(len(lines)):
        if all(map(lambda x: x == '.', lines[i])):
            emptyRows.append(i)
    for i in range(len(lines[0])):
        if all(map(lambda x: x[i] == '.', lines)):
            emptyColumns.append(i)
    starIndices = []
    for i in range(len(lines)):
        for j in range(len(lines[0])):
            if lines[i][j] != '.':
                starIndices.append((i, j))
    sums = []
    for i in range(len(starIndices) - 1):
        for j in range(i + 1, len(starIndices)):
            star1 = starIndices[i]
            star2 = starIndices[j]
            diffRow = abs(star1[0] - star2[0])
            for r in emptyRows:
                if star1[0] < r < star2[0] or star2[0] < r < star1[0]:
                    diffRow += expansionFactor - 1
            diffCol = abs(star1[1] - star2[1])
            for c in emptyColumns:
                if star1[1] < c < star2[1] or star2[1] < c < star1[1]:
                    diffCol += expansionFactor - 1
            m = diffRow + diffCol
            sums.append(m)
    return sum(sums)


def calcManhattanDistance(star1, star2):
    return abs(star1[0] - star2[0]) + abs(star1[1] - star2[1])


# solutions corner

startTime = time.time()

part1Test = part1(test_str)
if part1Test != 374:
    raise Exception(part1Test, 374)
print_hlight(part1(input_str))

part2BonusTest = part2(test_str,2)
if part2BonusTest != 374:
    raise Exception(part2BonusTest, 374)
part2Test = part2(test_str, 100)
if part2Test != 8410:
    raise Exception(part2Test, 8410)
print_hlight(part2(input_str, 1_000_000))

print_tlight("--- %s seconds ---" % (time.time() - startTime))
