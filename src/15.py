from utils.api import get_input, get_test_input, print_hlight, print_tlight
import time

current_day = 15
input_str = get_input(current_day)
test_str = get_test_input(current_day)


def part1(fullInput):
    phrases = fullInput.split(',')
    scores = []
    for p in phrases:
        scores.append(hashFun(p))
    return sum(scores)


def hashFun(p):
    acc = 0
    for char in p:
        acc += ord(char)
        acc *= 17
        acc = acc % 256
    return acc


def part2(fullInput):
    phrases = fullInput.split(',')
    lenses = {}
    for idx, p in enumerate(phrases):
        if p[-1] == '-':
            lenses.pop(p[:-1], None)
        else:
            label, lenLen = p.split('=')
            if label in lenses:
                lenses[label].lenLen = int(lenLen)
            else:
                lenses[label] = Lens(label, lenLen, idx)
    v = []
    for i in range(256):
        inBox = sorted(filter(lambda x: x.box == i, lenses.values()), key=lambda x: x.idx)
        # if inBox:
        #     print(list(map(lambda x: '{}: {}, {}, {}'.format(x.label, x.box, x.lenLen, x.idx), inBox)))
        for idx, p in enumerate(inBox):
            v.append((p.box + 1) * (idx + 1) * p.lenLen)
    return sum(v)


class Lens:
    def __init__(self, label, lenLen, idx):
        self.label = label
        self.box = hashFun(label)
        self.lenLen = int(lenLen)
        self.idx = idx


# solutions corner

startTime = time.time()

part1Test = part1(test_str)
part1TestExpected = 1320
if part1Test != part1TestExpected:
    raise Exception(part1TestExpected, part1Test)
print_hlight(part1(input_str))

part2Test = part2(test_str)
part2TestExpected = 145
if part2Test != part2TestExpected:
    raise Exception(part2TestExpected, part2Test)
print_hlight(part2(input_str))

print_tlight("--- %s seconds ---" % (time.time() - startTime))
