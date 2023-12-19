from utils.api import get_input, get_test_input, print_hlight, print_tlight
import time

current_day = 19
input_str = get_input(current_day)
test_str = get_test_input(current_day)


def part1(fullInput):
    workflowInput, itemInput = fullInput.split('\n\n')
    items = list(map(lambda x: parseItem(x), itemInput.splitlines()))
    accepted = []
    workflows = {}
    for w in workflowInput.splitlines():
        wf = parseWorkflow(w)
        workflows[wf.name] = wf
    while items:
        newItems = []
        for item in items:
            currentWorkflow = workflows[item.currentWorkflow]
            res = currentWorkflow.eval(item)
            if res == 'A':
                accepted.append(item)
            elif res == 'R':
                continue
                # do something
            else:
                newItems.append(item.copyTo(res))
        items = newItems
    return sum(list(map(lambda x: x.rating(), accepted)))


def part2(fullInput):
    workflowInput = fullInput.split('\n\n')[0]
    workflows = {}
    for w in workflowInput.splitlines():
        wf = parseWorkflow(w)
        workflows[wf.name] = wf
    ranges = [XmasRange()]
    finishedRanges = []
    # go through each range we have available
    while ranges:
        # compile ranges for next time
        newRanges = []
        for r in ranges:
            # get the workflow at the current eval step
            workflow = workflows[r.currentEval]
            bk = False
            # iterate through all the workflow statements
            for statement in workflow.statements:
                # if it's a final statement in the workflow, we have one of three steps
                if not statement.register:
                    # put it in the finish
                    if statement.destination == 'A':
                        finishedRanges.append(r)
                        break
                    # do nothing
                    elif statement.destination == 'R':
                        break
                    # move the workflow
                    else:
                        newRanges.append(XmasRange(r.xRange, r.mRange, r.aRange, r.sRange, statement.destination))
                        break
                # not a final statement
                else:
                    # pull out the range we will be comparing with
                    cmp = {'x': r.xRange, 'm': r.mRange, 'a': r.aRange, 's': r.sRange}[statement.register]
                    # the false case. It doesn't satisfy the condition here, so we go to the next statement
                    if (statement.function == '<' and cmp.start >= statement.compare) or (
                            statement.function == '>' and (cmp.stop - 1) <= statement.compare):
                        continue
                    # the true case. The statement completely satisfies conditions here, so we move to next spot
                    elif (statement.function == '>' and cmp.start > statement.compare) or (
                            statement.function == '<' and (cmp.stop - 1) < statement.compare):
                        # put it in the finish
                        if statement.destination == 'A':
                            finishedRanges.append(r)
                            break
                        # do nothing
                        elif statement.destination == 'R':
                            break
                        # move the workflow
                        else:
                            newRanges.append(XmasRange(r.xRange, r.mRange, r.aRange, r.sRange, statement.destination))
                            break
                    # the iffy case. We'll have to split this range in two.
                    else:
                        lSide = XmasRange(r.xRange, r.mRange, r.aRange, r.sRange, r.currentEval)
                        rSide = XmasRange(r.xRange, r.mRange, r.aRange, r.sRange, r.currentEval)
                        splitNum = statement.compare if statement.function == '<' else (statement.compare + 1)
                        if statement.register == 'x':
                            lSide.xRange = range(lSide.xRange.start, splitNum)
                            rSide.xRange = range(splitNum, rSide.xRange.stop)
                        elif statement.register == 'm':
                            lSide.mRange = range(lSide.mRange.start, splitNum)
                            rSide.mRange = range(splitNum, rSide.mRange.stop)
                        elif statement.register == 'a':
                            lSide.aRange = range(lSide.aRange.start, splitNum)
                            rSide.aRange = range(splitNum, rSide.aRange.stop)
                        else:
                            lSide.sRange = range(lSide.sRange.start, splitNum)
                            rSide.sRange = range(splitNum, rSide.sRange.stop)
                        newRanges.append(lSide)
                        newRanges.append(rSide)
                        break
        ranges = newRanges
    s = 0
    for r in finishedRanges:
        s += r.score()
    return s


class XmasRange:
    def __init__(self, xRange=range(1, 4001), mRange=range(1, 4001), aRange=range(1, 4001), sRange=range(1, 4001),
                 currentEval='in'):
        self.xRange = xRange
        self.mRange = mRange
        self.aRange = aRange
        self.sRange = sRange
        self.currentEval = currentEval

    def toString(self):
        return "{} - x:{}, m:{}, a:{}, s:{}, score: {}".format(self.currentEval, self.xRange, self.mRange, self.aRange,
                                                               self.sRange, self.score())

    def score(self):
        return len(self.xRange) * len(self.mRange) * len(self.aRange) * len(self.sRange)


def parseWorkflow(line):
    workflowName = line.split('{')[0]
    conditionStmts = line.split('{')[1][:-1].split(',')
    statements = list(map(lambda x: parseStatement(x), conditionStmts))
    return Workflow(workflowName, statements)


def parseStatement(stmt):
    if ':' not in stmt:
        return Statement(None, None, None, stmt)
    condition, destination = stmt.split(':')
    register = condition[0]
    function = condition[1]
    compare = int(condition[2:])
    return Statement(register, function, compare, destination)


def parseItem(line):
    xPart, mPart, aPart, sPart = list(map(lambda x: int(x.split('=')[1]), line[1:-1].split(',')))
    return Item(xPart, mPart, aPart, sPart)


class Statement:
    def __init__(self, register, function, compare, destination):
        self.register = register
        self.function = function
        self.compare = compare
        self.destination = destination

    def eval(self, item):
        itemReg = {'x': item.x, 'm': item.m, 'a': item.a, 's': item.s, None: None}[self.register]
        if not self.function:
            returnDest = True
        elif self.function == '<':
            returnDest = itemReg < self.compare
        else:
            returnDest = itemReg > self.compare
        return self.destination if returnDest else None


class Workflow:
    def __init__(self, name, statements):
        self.name = name
        self.statements = statements

    def eval(self, item):
        for statement in self.statements:
            ev = statement.eval(item)
            if ev:
                return ev


class Item:
    def __init__(self, x, m, a, s, currentWorkflow='in'):
        self.x = x
        self.m = m
        self.a = a
        self.s = s
        self.currentWorkflow = currentWorkflow

    def copyTo(self, newWorkflow):
        return Item(self.x, self.m, self.a, self.s, newWorkflow)

    def rating(self):
        return self.x + self.m + self.a + self.s


# solutions corner

startTime = time.time()

part1Test = part1(test_str)
part1TestExpected = 19114
if part1Test != part1TestExpected:
    raise Exception(part1Test, part1TestExpected)
print_hlight(part1(input_str))

part2Test = part2(test_str)
part2TestExpected = 167409079868000
if part2Test != part2TestExpected:
    raise Exception(part2Test, part2TestExpected)
print_hlight(part2(input_str))

print_tlight("--- %s seconds ---" % (time.time() - startTime))
