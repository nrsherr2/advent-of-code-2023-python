from utils.api import get_input, get_test_input, print_hlight, print_tlight
import time

current_day = 5
input_str = get_input(current_day)
test_str = get_test_input(current_day)


class AlmRange:
    def __init__(self, inputRange, destOffset):
        self.inputRange = inputRange
        self.destOffset = destOffset

    def inpR(self):
        return self.inputRange.start


def part1(inpStr):
    (seedStr, seedSoilStr, soilFertStr, fertWatStr, watLiteStr, liteTempStr, tempHumeStr, humeLocStr) = list(
        map(lambda x: x.split(":")[1].strip(), inpStr.split("\n\n")))
    inputSeeds = seedStr.split()
    return doCalcs(inputSeeds, fertWatStr, humeLocStr, liteTempStr, seedSoilStr, soilFertStr, tempHumeStr, watLiteStr)


def part2(inpStr):
    (seedStr, seedSoilStr, soilFertStr, fertWatStr, watLiteStr, liteTempStr, tempHumeStr, humeLocStr) = list(
        map(lambda x: x.split(":")[1].strip(), inpStr.split("\n\n")))
    inputRanges = list(map(lambda x: range(int(x[0]), int(x[0]) + int(x[1])), chunk(seedStr.split())))
    seedSoil = mapInput(seedSoilStr, True)
    soilFert = mapInput(soilFertStr, True)
    fertWat = mapInput(fertWatStr, True)
    watLite = mapInput(watLiteStr, True)
    liteTemp = mapInput(liteTempStr, True)
    tempHume = mapInput(tempHumeStr, True)
    humeLoc = mapInput(humeLocStr, True)

    # I made these all different for debugging purposes
    upRange = cutSplit(inputRanges, seedSoil)
    upRange = cutSplit(upRange, soilFert)
    upRange = cutSplit(upRange, fertWat)
    upRange = cutSplit(upRange, watLite)
    upRange = cutSplit(upRange, liteTemp)
    upRange = cutSplit(upRange, tempHume)
    upRange = cutSplit(upRange, humeLoc)
    minStart = 9999999999
    for r in upRange:
        if r.start < minStart:
            minStart = r.start
    return minStart


def doCalcs(inputSeeds, fertWatStr, humeLocStr, liteTempStr, seedSoilStr, soilFertStr, tempHumeStr, watLiteStr):
    seedSoil = mapInput(seedSoilStr, False)
    soilFert = mapInput(soilFertStr, False)
    fertWat = mapInput(fertWatStr, False)
    watLite = mapInput(watLiteStr, False)
    liteTemp = mapInput(liteTempStr, False)
    tempHume = mapInput(tempHumeStr, False)
    humeLoc = mapInput(humeLocStr, False)
    minNum = 9999999999
    for seed in inputSeeds:
        acc = int(seed)
        for m in [(seedSoil, 'soil'), (soilFert, 'fertilizer'), (fertWat, 'water'), (watLite, 'light'),
                  (liteTemp, 'temperature'), (tempHume, 'humidity'), (humeLoc, 'location')]:
            acc = modify(acc, m[0], m[1])
        if acc < minNum:
            minNum = acc
    return minNum


def chunk(listOfWords):
    for i in range(0, len(listOfWords), 2):
        yield listOfWords[i: i + 2]


def buildRange(line):
    (destStart, srcStart, rangeSize) = map(lambda x: int(x), line.split())
    offset = destStart - srcStart
    myRange = range(srcStart, srcStart + rangeSize)
    return AlmRange(myRange, offset)


def mapInput(baseStr, fillInGaps):
    lines = baseStr.splitlines()
    withGaps = list(map(lambda x: buildRange(x), lines))
    if not fillInGaps:
        return withGaps
    i = 0
    withoutGaps = sorted(withGaps, key=AlmRange.inpR)
    firstStart = withoutGaps[0].inputRange.start
    withoutGaps.append(AlmRange(range(withoutGaps[-1].inputRange.stop, 9999999999), 0))
    if firstStart != 0:
        withoutGaps.append(AlmRange(range(0, firstStart), 0))
    withoutGaps = sorted(withoutGaps, key=AlmRange.inpR)
    while i < len(withoutGaps) - 1:
        (currentEl, nextEl) = withoutGaps[i:i + 2]
        if currentEl.inputRange.stop < nextEl.inputRange.start:
            # print('added')
            withoutGaps.append(AlmRange(range(currentEl.inputRange.stop, nextEl.inputRange.start), 0))
            i = 0
            withoutGaps = sorted(withoutGaps, key=AlmRange.inpR)
            # print(list(map(lambda x: "{} {}".format(x.inputRange, x.destOffset), withoutGaps)))
            continue
        i += 1
    return withoutGaps


def modify(num, almRanges, rangeName):
    acc = num
    for r in almRanges:
        if num in r.inputRange:
            acc = num + r.destOffset
            break
    # print("{} {}".format(rangeName, acc))
    return acc


def cutSplit(ranges, almList):
    oldRanges = ranges
    newRanges = []
    while oldRanges:
        r = oldRanges[0]
        oldRanges.remove(r)
        for a in almList:
            if a.inputRange.start <= r.start < a.inputRange.stop:
                if a.inputRange.start <= r.stop <= a.inputRange.stop:
                    newRanges.append(range(r.start + a.destOffset, r.stop + a.destOffset))
                else:
                    rangeLow = range(r.start, a.inputRange.stop)
                    newRanges.append(rangeLow)
                    rangeHigh = range(a.inputRange.stop, r.stop)
                    oldRanges.append(rangeHigh)
    return newRanges


part1TestExpected = 35
part2TestExpected = 46

startTime = time.time()
# WRITE YOUR SOLUTION HERE
p1Test = part1(test_str)
if p1Test != part1TestExpected:
    raise Exception("Test Failed! Expected {}, Received {}".format(part1TestExpected, p1Test))
# print(p1Test)
print_hlight(part1(input_str))

p2Test = part2(test_str)
if p2Test != part2TestExpected:
    raise Exception("Test Failed! Expected {}, Received {}".format(part2TestExpected, p2Test))
print_hlight(part2(input_str))

print_tlight("--- %s seconds ---" % (time.time() - startTime))
