from utils.api import get_input, get_test_input
import time

current_day = 1
input_str = get_input(current_day)
test_str = get_test_input(current_day)

startTime = time.time()

part1Nums = []
for line in input_str.splitlines():
    firstNum = '0'
    lastNum = '0'
    for char in line:
        if char.isnumeric():
            firstNum = char
            break
    for char in reversed(line):
        if char.isnumeric():
            lastNum = char
            break
    fullNum = firstNum + lastNum
    part1Nums.append(int(fullNum))
print(sum(part1Nums))

nums = {"one": '1', "two": '2', "three": '3', "four": '4', "five": '5', "six": '6', "seven": '7', "eight": '8',
        "nine": '9'}
part2Nums = []
for line in input_str.splitlines():
    firstNum = '0'
    lastNum = '0'
    # iterate forwards
    for pos, char in enumerate(line):
        # look for number
        if char.isnumeric():
            # print(char)
            firstNum = char
            break

        # iterate over dict keys to find a word
        for numStr in nums:
            # if the char is the start of one of the words, and the word wouldn't exceed the length of the line, take a
            # substring from the position to (that position + the num string's length)
            if char == numStr[0] and (pos + len(numStr)) <= len(line) and numStr == line[pos:(pos + len(numStr))]:
                # if it's a match, set first num
                firstNum = nums[numStr]
                break
        # if we've found something, break
        if firstNum != '0':
            break

    for pos in range(len(line) - 1, -1, -1):
        char = line[pos]

        # look for number
        if char.isnumeric():
            lastNum = char
            break
        # iterate over dict keys to find a word
        for numStr in nums:
            # if the char is the start of one of the words, and the word wouldn't exceed the length of the line, take a
            # substring from the position to (that position + the num string's length)
            if char == numStr[0] and (pos + len(numStr)) <= len(line) and numStr == line[pos:(pos + len(numStr))]:
                # if it's a match, set first num
                lastNum = nums[numStr]
                break
        # if we've found something, break
        if lastNum != '0':
            break

    # print(firstNum, lastNum)
    fullNum = firstNum + lastNum
    part2Nums.append(int(fullNum))

print(sum(part2Nums))

print("--- %s seconds ---" % (time.time() - startTime))


# this is a fancier solution method I saw on reddit for dealing with the issues of replace, so I decided to implement
# it here. Not original thought, but decided I might as well implement it

newTime = time.time()
repls = {'one': 'one1one', 'two': 'two2two', 'three': 'three3three', 'four': 'four4four', 'five': 'five5five',
         'six': 'six6six', 'seven': 'seven7seven', 'eight': 'eight8eight', 'nine': 'nine9nine'}
part3Nums = []
for line in input_str.splitlines():
    ln = line
    for r in repls:
        ln = ln.replace(r, repls[r])
    newL = ''
    for r in ln:
        if r.isnumeric():
            newL = newL + r
    fullNum = newL[0] + newL[-1]
    part3Nums.append(int(fullNum))
print(sum(part3Nums))
print("--- %s seconds ---" % (time.time() - newTime))
