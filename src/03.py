from utils.api import get_input, get_test_input
import time

current_day = 3
input_str = get_input(current_day)
test_str = get_test_input(current_day)


def part1(inp):
    lines = inp.splitlines()
    okNums = []

    # iterate over every line in the input
    for lineNum in range(0, len(lines)):
        # track the current number we are building
        currentNum = ''
        # track whether the num has a nearby symbol
        numOk = False
        line = lines[lineNum]
        # iterate over every character in the line
        for colNum in range(0, len(line)):
            myChr = lines[lineNum][colNum]
            # it's the end of a number, make sure we're currently parsing one
            if not myChr.isnumeric() and currentNum != '':
                # if we found a match in the part, append to list
                if numOk:
                    okNums.append(int(currentNum))
                # clear the number and ok status
                currentNum = ''
                numOk = False
            # a number to append onto currentNum
            elif myChr.isnumeric():
                currentNum += myChr
                # check all spaces around this number for a symbol
                for i in range(-1, 2):
                    for j in range(-1, 2):
                        location = (lineNum + i, colNum + j)
                        if 0 <= location[0] < len(lines):
                            if 0 <= location[1] < len(line):
                                chk = lines[location[0]][location[1]]
                                if not chk.isnumeric() and chk != '.':
                                    numOk = True
        # end of line, append if we need to
        if numOk:
            okNums.append(int(currentNum))
    return sum(okNums)


def inBubble(numLoc, bubble):
    for loc in numLoc[1]:
        if loc in bubble:
            return True
    return False


def part2(inp):
    lines = inp.splitlines()
    numberLocs = []
    gearLocs = []
    rashos = []
    for lineNum in range(0, len(lines)):
        line = lines[lineNum]
        currentNum = ''
        currentNumLocs = []
        for colNum in range(0, len(line)):
            myChr = lines[lineNum][colNum]
            if myChr.isnumeric():
                currentNum += myChr
                currentNumLocs.append((lineNum, colNum))
            elif currentNum != '':
                numberLocs.append((int(currentNum), currentNumLocs))
                currentNum = ''
                currentNumLocs = []
            if myChr == '*':
                gearLocs.append((lineNum, colNum))
        if currentNum != '':
            numberLocs.append((int(currentNum), currentNumLocs))
    for loc in gearLocs:
        bubble = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                bubble.append((loc[0] + i, loc[1] + j))
        nearGear = list(filter(lambda x: inBubble(x, bubble), numberLocs))
        if len(nearGear) == 2:
            s = 1
            for g in nearGear:
                s = s * g[0]
            rashos.append(s)
    return sum(rashos)


startTime = time.time()

part1TestExpected = 4361
part1Test = part1(test_str)
if part1Test != part1TestExpected:
    raise Exception("TEST FAILED! Expected {exp}, Got {rel}".format(exp=part1TestExpected, rel=part1Test))
part1Real = part1(input_str)

part2TestExpected = 467835
part2Test = part2(test_str)
if part2Test != part2TestExpected:
    raise Exception("TEST FAILED! Expected {exp}, Got {rel}".format(exp=part2TestExpected, rel=part2Test))
part2Real = part2(input_str)

print(part1Real)
print(part2Real)

print("--- %s seconds ---" % (time.time() - startTime))
