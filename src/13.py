from utils.api import get_input, get_test_input, print_hlight, print_tlight
import time

current_day = 13
input_str = get_input(current_day)
test_str = get_test_input(current_day)


def detectReflectHorizontal(block, i, exclude):
    lb = len(block)
    if i >= lb or i in exclude:
        return False
    offs = lb - i
    if offs < i:
        # print('c1', block[i - offs:i], list(reversed(block[i:])))
        return block[i - offs:i] == list(reversed(block[i:]))
    else:
        # print('c2', block[:i], block[i:2 * i])
        return block[:i] == list(reversed(block[i:2 * i]))


def transpose(block):
    v = [[block[j][i] for j in range(len(block))] for i in range(len(block[0]))]
    return list(map(lambda x: ''.join(x), v))


def detectReflect(block, excludeHorizontal, excludeVertical):
    # print(block)
    i = 1
    horizontalBlock = block.splitlines()
    # print('horiz', horizontalBlock)
    verticalBlock = transpose(block.splitlines())
    # print('verti', verticalBlock)
    horizontals = []
    verticals = []
    maxBound = max(len(horizontalBlock), len(verticalBlock))
    while i < maxBound:
        # print('reflect horizontal', i)
        if detectReflectHorizontal(horizontalBlock, i, excludeHorizontal):
            # print('detected horizontal', i)
            horizontals.append(i)
            return i * 100, horizontals,verticals
        # print('reflect vertical', i)
        if detectReflectHorizontal(verticalBlock, i, excludeVertical):
            # print('detected vertical', i)
            verticals.append(i)
            return i, horizontals,verticals
        i += 1
    raise Exception('no reflections found')


def num_char_difference(side1, side2):
    p = 0
    loc = -1, -1
    for i, s1 in enumerate(side1):
        s2 = side2[i]
        for j, c1 in enumerate(s1):
            c2 = s2[j]
            if c1 != c2:
                p += 1
                loc = i, j
    return p, loc


def attemptFixSmudgeHorizontal(block, i):
    lb = len(block)
    if i >= lb:
        return block, False
    offs = lb - i
    leftSide, rightSide = (block[i - offs:i], list(reversed(block[i:]))) if offs < i \
        else (block[:i], list(reversed(block[i:2 * i])))
    numDiff, loc = num_char_difference(leftSide, rightSide)
    if numDiff == 1:
        li, lj = loc
        if offs >= i:
            block[li] = block[li][:lj] + ('#' if block[li][lj] == '.' else '.') + block[li][lj + 1:]
        else:
            mb = block[i - offs + li]
            block[i - offs + li] = mb[:lj] + ('#' if mb[lj] == '.' else '.') + mb[lj + 1:]
        return block, True
    else:
        return block, False


def detectSmudgeAndReflect(block):
    _, oldHoriz, oldVerti = detectReflect(block, [], [])
    horizontalBlock = block.splitlines()
    # print(horizontalBlock)
    verticalBlock = transpose(block.splitlines())
    maxBound = max(len(horizontalBlock), len(verticalBlock))
    i = 1
    while i < maxBound:
        hb2, hRes = attemptFixSmudgeHorizontal(horizontalBlock, i)
        if hRes:
            horizontalBlock = hb2
            break
        vb2, vRes = attemptFixSmudgeHorizontal(verticalBlock, i)
        if vRes:
            horizontalBlock = transpose(vb2)
            break
        i += 1
    if i == maxBound:
        raise Exception('no smudge found')
    # print(horizontalBlock)
    # print(verticalBlock)
    # print(transpose(horizontalBlock))
    return detectReflect("\n".join(horizontalBlock), oldHoriz, oldVerti)[0]


def part1(fullInput):
    blocks = fullInput.split("\n\n")
    sums = []
    for block in blocks:
        sums.append(detectReflect(block.strip(), [], [])[0])
    return sum(sums)


def part2(fullInput):
    blocks = fullInput.split("\n\n")
    sums = []
    for block in blocks:
        sums.append(detectSmudgeAndReflect(block.strip()))
    return sum(sums)


# solutions corner

startTime = time.time()

part1Test = part1(test_str)
part1TestExpected = 405
if part1Test != part1TestExpected:
    raise Exception(part1Test, part1TestExpected)
print_hlight(part1(input_str))

part2Test = part2(test_str)
part2TestExpected = 400
if part2Test != part2TestExpected:
    raise Exception(part2Test, part2TestExpected)
print_hlight(part2(input_str))

print_tlight("--- %s seconds ---" % (time.time() - startTime))
