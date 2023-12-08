import functools
import math

from utils.api import get_input, get_test_input, print_hlight, print_tlight
from queue import Queue
import time

current_day = 8
input_str = get_input(current_day)
test_str_1 = get_test_input(81)
test_str_2 = get_test_input(82)
test_str_3 = get_test_input(83)


def part1(fullInput):
    nodes, steps = parse_input(fullInput)

    currentNode = 'AAA'

    return solveSteps(currentNode, nodes, steps)


def solveSteps(currentNode, nodes, steps):
    q = Queue(len(steps))
    for s in steps:
        q.put(s)
    numSteps = 0
    while currentNode[-1] != 'Z':
        step = q.get()
        numSteps += 1
        direction = 0 if step == 'L' else 1
        # cn = currentNode
        currentNode = nodes[currentNode][direction]
        # print("{} -{}-> {}".format(cn,step, currentNode))
        q.put(step)
    return numSteps


def part2(fullInput):
    nodes, steps = parse_input(fullInput)
    startingNodes = list(filter(lambda x: x[-1] == 'A', nodes.keys()))
    r = 1
    for s in startingNodes:
        solved = solveSteps(s, nodes, steps)
        r = math.lcm(r, solved)
    return r


def parse_input(fullInput):
    (steps, nodesStr) = fullInput.split("\n\n")

    nodes = {}
    for line in nodesStr.splitlines():
        nodes[line[0:3]] = (line.split('(')[1].split(',')[0], line.split(', ')[1].split(')')[0])
    return nodes, steps


# solutions corner


startTime = time.time()

part1Test = [(part1(test_str_1), 2), (part1(test_str_2), 6)]
for test, expected in part1Test:
    if test != expected:
        raise Exception("expected {}, got {}".format(expected, test))

print_hlight(part1(input_str))

part2Test = part2(test_str_3)
part2TestExpected = 6
if part2Test != part2TestExpected:
    raise Exception("expected {}, got {}".format(part2TestExpected, part2Test))
print_hlight(part2(input_str))

print_tlight("--- %s seconds ---" % (time.time() - startTime))
