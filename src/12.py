from functools import lru_cache

from utils.api import get_input, get_test_input, print_hlight, print_tlight
import time

current_day = 12
input_str = get_input(current_day)
test_str = get_test_input(current_day)

def part1(fullInput):
    solnSizes = list(map(lambda x: picross(x), fullInput.splitlines()))
    return sum(solnSizes)


def part2(fullInput):
    solnSizes = []
    for line in fullInput.splitlines():
        # l = the line to decode, r = the block sizes of #
        l, r = line.split()
        # make 5 copies of the initial line, and join them with a `?` as per PS
        lFold = [l] * 5
        ls = '?'.join(lFold)
        # make 5 copies of the number array and join them with a `,` as per PS
        rFold = [r] * 5
        rs = ','.join(rFold)
        # join those 2 parts back together to disguise it as a regular input line
        fullL = "{} {}".format(ls, rs)
        # it's actually the same formula to solve parts 1 and 2, so that's why I have to disguise it
        solnSizes.append(picross(fullL))
    return sum(solnSizes)


def picross(line):
    """
    I'm going to define this like Picross, the game I am familiar with. In Picross, the player is given a line of boxes.
    Above/To the side of those boxes is a list of numbers. These numbers correspond with a number of boxes that the
    player must fill in a row. These boxes must be separated by one or more unfilled boxes. You may also have 0 or more
    unfilled boxes at the start and end of the row.
    Please look up what a Picross puzzle looks like.
    This problem statement is very similar to the mid-game of Picross, where the player has a few rows that they are
    100% sure where they should/should not fill in a box. A filled box will be filled, and a confirmed non-fill box will
    be marked with an X (`.` in this puzzle). These rows will intersect with a column. So now, you know what some of the
    spots in this column will look like, but not all of them. In my mind, I will be coming up with permutations to solve
    the row, but this function should do the same thing.
    :param line: the line of input given by AoC
    :return: the number of ways you can solve this line.
    """
    # guide is the string to match against, rawNums is the block sizes
    guide, rawNums = line.split()
    nums = list(map(lambda x: int(x), rawNums.split(',')))
    # another way to think about filling a row in picross is that you need to have some number of Xs, that when added
    # to the given number of filled boxes, will equal the total length of the line. We can filter out solutions that put
    # too much space between numbers by counting how many Xs they have left to put in a line before we know it will
    # over fill.
    totalNumBoxes = len(guide)
    totalNumFilled = sum(nums)
    numDots = totalNumBoxes - totalNumFilled

    @lru_cache(maxsize=None)
    def fillNum(currentString, numIdx, remainingDots, justPlacedBox):
        """
        work your way through the guide string, branching on the letter given in the guide

        by the way, this is all cached so that we can quickly look up the results of the end steps. Eventually, we will
        have a sort of tree of every state, and we'll know what happens if you take the tree for a certain state and
        not have to calculate everything below.
        :param currentString: the letters we have left in the guide
        :param numIdx: the index into the nums array (defined outside the function) we're at. [1,2,1][1] = 2
        :param remainingDots: how many dots we have left before we consider this solution invalid for too many Xs
        :param justPlacedBox: groups of squares must be separated by at least one X, so this disables filling in
                              a square after you have just filled one in
        :return: 1 if the solution is solved correctly, 0 if we can't solve from here. If we have not finished the
                 guide, and the solution is still valid, we will recurse down another layer, using less of the string.
        """
        if len(currentString) == 0:
            # we have reached the end while still being valid. Proudly return that one.
            return 1
        else:
            # examine the current first character
            c = currentString[0]
            # we need available dots if we want to add them to the soln. If no dots are available, we go to else.
            if c == '.' and remainingDots > 0:
                # recurse down. start the string 1 further. Use 1 fewer dot.
                return fillNum(currentString[1:], numIdx, remainingDots - 1, False)
            # we need to have an available number if we want to mark boxes, and we can't have just marked a box.
            elif c == '#' and numIdx < len(nums) and not justPlacedBox:
                # the number of boxes we will be marking
                num = nums[numIdx]
                # make sure there are no confirmed dots in the space we will be marking
                if len(currentString) < num or not all(map(lambda x: x == '#' or x == '?', currentString[:num])):
                    return 0
                else:
                    # recurse down, skipping `num` characters, preventing boxes from being placed next cycle
                    return fillNum(currentString[num:], numIdx + 1, remainingDots, True)
            elif c == '?':
                # branching condition here. We could place another X, or we could start the next set of marked boxes
                dotSide = 0
                boxSide = 0
                if remainingDots > 0:
                    # if we can place a dot, branch the tree and return the result of placing a dot
                    dotSide = fillNum(currentString[1:], numIdx, remainingDots - 1, False)
                if numIdx < len(nums) and not justPlacedBox:
                    # if we can place a box, branch the tree and return the result of filling a box.
                    num = nums[numIdx]
                    if len(currentString) >= num and all(map(lambda x: x == '#' or x == '?', currentString[:num])):
                        boxSide = fillNum(currentString[num:], numIdx + 1, remainingDots, True)
                # return the result of both branches. Has the chance to return 0 if we reach an error case either way
                return dotSide + boxSide
            else:
                # it's an error case. We either can't place another dot when it's all we can do, or we can't fill a box
                # when it's all we can do.
                return 0

    # initial recursion step. Supply the full guide, start on num index 0, with the full dots, and we have not filled.
    sols = fillNum(guide, 0, numDots, False)
    return sols


# solutions corner

startTime = time.time()

part1Test = part1(test_str)
part1TestExpected = 21
if part1Test != part1TestExpected:
    raise Exception(part1Test, part1TestExpected)
print_hlight(part1(input_str))
#
part2Test = part2(test_str)
part2TestExpected = 525152
if part2Test != part2TestExpected:
    raise Exception(part2Test, part2TestExpected)
print_hlight(part2(input_str))

print_tlight("--- %s seconds ---" % (time.time() - startTime))
