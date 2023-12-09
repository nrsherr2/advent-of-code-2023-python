import functools

from utils.api import get_input, get_test_input, print_hlight, print_tlight
import time

current_day = 9
input_str = get_input(current_day)
test_str = get_test_input(current_day)


def part1(fullInput):
    results = list(map(lambda x: extrapolateLine(x)[0], fullInput.splitlines()))
    return sum(results)

def part2(fullInput):
    results = list(map(lambda x: extrapolateLine(x)[1], fullInput.splitlines()))
    return sum(results)


def extrapolateLine(line):
    samples = list(map(lambda x: int(x), line.split()))
    layersOfHell = [samples]
    currentHellLayer = samples
    while not allZero(currentHellLayer):
        nextLayer = []
        for i in range(0, len(currentHellLayer) - 1):
            nextLayer.append(currentHellLayer[i + 1] - currentHellLayer[i])
        layersOfHell.append(nextLayer)
        currentHellLayer = nextLayer
    layersOfHell[-1][-1] = 0
    for i in range(len(layersOfHell) - 2, -1, -1):
        lastPlus = layersOfHell[i+1][-1]
        currentLast = layersOfHell[i][-1]
        layersOfHell[i].append(lastPlus + currentLast)
        lastMinus = layersOfHell[i+1][0]
        currentMinus =layersOfHell[i][0]
        layersOfHell[i].insert(0, currentMinus - lastMinus)
    # print('')
    # for lay in layersOfHell:
    #     print(lay)
    return layersOfHell[0][-1], layersOfHell[0][0]


def allZero(layer):
    for l in layer:
        if l != 0:
            return False
    return True


# solutions corner

startTime = time.time()

part1Test = part1(test_str)
part1TestExpected = 114
if part1Test != part1TestExpected:
    raise Exception(part1TestExpected, part1Test)
print_hlight(part1(input_str))

part2Test = part2(test_str)
part2TestExpected = 2
if part2Test != part2TestExpected:
    raise Exception(part2TestExpected,part2Test)
print_hlight(part2(input_str))

print_tlight("--- %s seconds ---" % (time.time() - startTime))
