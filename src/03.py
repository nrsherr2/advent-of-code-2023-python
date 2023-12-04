from utils.api import get_input, get_test_input

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


part1TestExpected = 413
part1Test = part1(test_str)
if part1Test != part1TestExpected:
    raise Exception("TEST FAILED! Expected {exp}, Got {rel}".format(exp=part1TestExpected, rel=part1Test))
part1Real = part1(input_str)

print(part1Real)
