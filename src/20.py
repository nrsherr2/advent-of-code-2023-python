import math

from utils.api import get_input, get_test_input, print_hlight, print_tlight
import time
from abc import ABC, abstractmethod, abstractproperty

current_day = 20
input_str = get_input(current_day)
test_str = get_test_input(current_day)
test_str2 = get_test_input(201)


def part1(fullInput):
    network = parseInput(fullInput.splitlines())
    lowHits = 0
    highHits = 0
    for i in range(1000):
        q = [('button', 'broadcaster', 'l')]
        lowHits += 1
        while q:
            src, dest, mag = q.pop(0)
            if dest not in network:
                continue
            else:
                result = network[dest].sendPulse(src, mag)
                for r in result:
                    if r[2] == 'l':
                        lowHits += 1
                    else:
                        highHits += 1
                    q.append(r)
    return lowHits * highHits


def part2(fullInput):
    """
    The trick of part 2 was to map out the network yourself and notice that there are essentially 4 main chains of
    nodes. Each chain has its own conjunction node that it sends a signal to at the end of each loop, which then outputs
    to another conjunction node that acts as an inverter, as we were shown in the example. Then, there is one last node
    that feeds into rx. This one is another conjunction node that takes the results from these 4 inverters. Essentially,
    we are waiting for the one cycle where vg, kd, zf, and gs all happen to send a low signal to rg.
    """
    network = parseInput(fullInput.splitlines())
    # count number of times we press the button
    i = 0
    # keep track of when each loop finishes its cycle
    loopTimes = {}
    # the while true acts as pressing the button
    while True:
        q = [('button', 'broadcaster', 'l')]
        i += 1
        # disperse the signals
        while q:
            src, dest, mag = q.pop(0)
            if dest not in network:
                continue
            else:
                result = network[dest].sendPulse(src, mag)
                for r in result:
                    # a cycle happens when the conjunction node sends a low signal to our inverter.
                    if r[1] in ['vg', 'kd', 'zf', 'gs'] and r[2] == 'l':
                        # keep track of which inverter gets the signal at this button press
                        loopTimes[r[1]] = i
                    if r[1] == 'rx':
                        if r[0] == 'l':
                            return i
                    q.append(r)
        # we have our 4 cycle times for each loop, now we can find the LCM to find the cycle where all 4 will send
        # the l at the same time
        if len(loopTimes) == 4:
            p = 1
            for r in loopTimes:
                p = abs(p * loopTimes[r]) // math.gcd(p, loopTimes[r])
            return p


def memoizeState(network):
    s = ""
    for n in network:
        if n not in ['rg', 'zf', 'vg', 'gs']:
            s += "{},".format(network[n].memoize())
    return s


def parseInput(lines):
    switches = {}

    for line in lines:
        children = line.split(' -> ')[1].split(', ')
        if line.startswith('broadcaster'):
            switches['broadcaster'] = Broadcaster(children)
            continue
        elif line.startswith('%'):
            label = line.split(' -> ')[0][1:]
            switches[label] = FlipFlop(children, label)
        else:
            label = line.split(' -> ')[0][1:]
            parents = []
            for line2 in lines:
                c = line2.split(' -> ')[1]
                if label in c:
                    parents.append(line2.split(' -> ')[0][1:])
            switches[label] = Conjunction(children, parents, label)
    return switches


class Switch(ABC):
    def __init__(self, children, label):
        self.children = children
        self.label = label

    @abstractmethod
    def sendPulse(self, source, pulse):
        pass

    @property
    @abstractmethod
    def childLabels(self):
        return self.children

    @abstractmethod
    def memoize(self):
        pass


class Broadcaster(Switch):
    @property
    def childLabels(self):
        return self.children

    def memoize(self):
        return "B"

    def __init__(self, children):
        super().__init__(children, 'broadcaster')

    def sendPulse(self, source, pulse):
        return list(map(lambda c: ('broadcaster', c, pulse), self.children))


class FlipFlop(Switch):
    @property
    def childLabels(self):
        return self.children

    def memoize(self):
        return '1' if self.on else '0'

    def __init__(self, children, label):
        super().__init__(children, label)
        self.on = False

    def sendPulse(self, source, pulse):
        if pulse == 'h':
            return []
        else:
            self.on = not self.on
            newPulse = 'h' if self.on else 'l'
            return list(map(lambda c: (self.label, c, newPulse), self.children))


class Conjunction(Switch):
    def __init__(self, children, parents, label):
        super().__init__(children, label)
        self.parentStates = dict(map(lambda c: (c, 'l'), parents))

    def sendPulse(self, source, pulse):
        self.parentStates[source] = pulse
        if all(map(lambda h: self.parentStates[h] == 'h', self.parentStates)):
            return list(map(lambda c: (self.label, c, 'l'), self.children))
        else:
            return list(map(lambda c: (self.label, c, 'h'), self.children))

    @property
    def childLabels(self):
        return self.children

    def memoize(self):
        return self.parentStates


# solutions corner

startTime = time.time()

for testInput, testExpected in [(test_str, 32000000), (test_str2, 11687500)]:
    res = part1(testInput)
    if res != testExpected:
        raise Exception(testExpected, res)
print_hlight(part1(input_str))

# part2Test = part2(test_str)
print_hlight(part2(input_str))

print_tlight("--- %s seconds ---" % (time.time() - startTime))
