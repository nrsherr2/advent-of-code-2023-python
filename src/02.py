from utils.api import get_input, get_test_input, print_hlight, print_tlight
import re
import time

current_day = 2
input_str = get_input(current_day)
test_str = get_test_input(current_day)



def part1(inputStr):
    redMax = 12
    greenMax = 13
    blueMax = 14

    results = []
    for line in inputStr.splitlines():
        results.append(onEachLine(line, redMax, greenMax, blueMax))

    finalNum = 0
    for i in range(0, len(results)):
        if results[i]:
            finalNum += i + 1

    return finalNum


def onEachLine(line, redMax, greenMax, blueMax):
    for blueStr in re.findall(r"\d+ blue", line):
        if int(blueStr.split(" ")[0]) > blueMax:
            return False
    for greenStr in re.findall(r"\d+ green", line):
        if int(greenStr.split(" ")[0]) > greenMax:
            return False
    for redStr in re.findall(r"\d+ red", line):
        if int(redStr.split(" ")[0]) > redMax:
            return False
    return True


def part2(lines):
    scores = []
    for line in map(lambda x: x.split(": ")[1], lines.splitlines()):
        reds = re.findall(r"\d+ red", line)
        maxRed = max(list(map(lambda x: int(x.split(" ")[0]), reds)))
        blues = re.findall(r"\d+ blue",line)
        maxBlue = max(list(map(lambda x: int(x.split(" ")[0]), blues)))
        greens = re.findall(r"\d+ green",line)
        maxGreen = max(list(map(lambda x: int(x.split(" ")[0]), greens)))
        scores.append(maxRed * maxBlue * maxGreen)
    return sum(scores)



startTime = time.time()
p1TestExpected = 8
part1Test = part1(test_str)
if part1Test != p1TestExpected:
    raise Exception("TEST FAILED! Expected {exp}, Got {rel}".format(exp=p1TestExpected, rel=part1Test))
part1True = part1(input_str)

p2TestExpected = 2286
part2Test = part2(test_str)
if part2Test != p2TestExpected:
    raise Exception("TEST FAILED! Expected {exp}, Got {rel}".format(exp=p2TestExpected, rel=part2Test))
part2True = part2(input_str)
print_hlight(part1True)
print_hlight(part2True)

print_tlight("--- %s seconds ---" % (time.time() - startTime))
