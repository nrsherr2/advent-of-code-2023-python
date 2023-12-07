import functools

from utils.api import get_input, get_test_input, print_hlight, print_tlight
import time

current_day = 7
input_str = get_input(current_day)
test_str = get_test_input(current_day)


def part1(fullInput):
    return doYoshi(fullInput, False)


def part2(fullInput):
    return doYoshi(fullInput, True)


class Kira:
    def __init__(self, textLine, isPart2=False):
        (h, b) = textLine.split()
        self.cards = (h.replace('T', ':').replace('J', '1' if isPart2 else ';').replace('Q', '<').replace('K', '=')
                      .replace('A', '>'))
        self.bet = int(b)
        self.tier = 0


def doYoshi(fullInput, isPart2):
    # parse input
    yoshi = list(map(lambda x: Kira(x, isPart2), fullInput.splitlines()))
    for k in yoshi:
        # see cards.png
        if isPart2:
            getTiersPart2(k)
        else:
            getTiersPart1(k)
    # sort cards. lowest tier first. Ties are broken by string compare
    sortedYoshi = sorted(yoshi, key=functools.cmp_to_key(compareKira), reverse=True)
    sm = 0
    for i in range(0, len(sortedYoshi)):
        # print("{} | {} * {} = {}".format(sortedYoshi[i].cards, sortedYoshi[i].bet, i + 1, sortedYoshi[i].bet * (i + 1)))
        # score is position in list (1 indexed) times starting bet
        sm += (i + 1) * sortedYoshi[i].bet
    return sm


def getTiersPart2(k):
    # get num occurrences of joker in hand
    jokerCount = k.cards.count('1')
    # get number of occurrences of each card in the hand, and tack on joker
    withJoker = list(map(lambda x: (x, k.cards.count(x), jokerCount), char_range('2', '>')))
    # order cards by num appearances
    srt = sorted(withJoker, key=functools.cmp_to_key(compareBySum))
    # set base tier based on number of kind
    k.tier = (srt[0][1] + srt[0][2]) * 2
    # handle case for 2 pair or full house
    if (k.tier == 4 or k.tier == 6) and srt[1][1] == 2:
        k.tier += 1


def getTiersPart1(k):
    # get num occurrences of each card
    counts = list(map(lambda x: (x, k.cards.count(x)), char_range('2', '>')))
    # order cards by num appearances
    srt = sorted(counts, key=functools.cmp_to_key(compareBySecond))
    # set base tier based on number of kind
    k.tier = srt[0][1] * 2
    # handle case for 2 pair or full house
    if (srt[0][1] == 2 or srt[0][1] == 3) and srt[1][1] == 2:
        k.tier += 1


def char_range(c1, c2):
    """Generates the characters from `c1` to `c2`, inclusive."""
    for c in range(ord(c1), ord(c2) + 1):
        yield chr(c)


def compareBySum(p1, p2):
    s1 = p1[1] + p1[2]
    s2 = p2[1] + p2[2]
    if s2 < s1:
        return -1
    elif s2 < s1:
        return 1
    else:
        return 0


def compareBySecond(p1, p2):
    if p2[1] < p1[1]:
        return -1
    elif p2[1] > p1[1]:
        return 1
    else:
        return 0


def compareKira(k1, k2):
    if k2.tier < k1.tier:
        return -1
    elif k2.tier > k1.tier:
        return 1
    elif k2.cards < k1.cards:
        return -1
    elif k2.cards > k1.cards:
        return 1
    else:
        return 0


# solutions corner

startTime = time.time()

part1Test = part1(test_str)
part1Expected = 6440
if part1Test != part1Expected:
    raise Exception(part1Test, part1Expected)
print_hlight(part1(input_str))

part2Test = part2(test_str)
part2TestExpected = 5905
if part2Test != part2TestExpected:
    raise Exception(part2Test, part2TestExpected)
print_hlight(part2(input_str))

print_tlight("--- %s seconds ---" % (time.time() - startTime))
