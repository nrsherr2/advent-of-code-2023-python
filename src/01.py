from utils.api import get_input, get_test_input

current_day = 1
input_str = get_input(current_day)
test_str = get_test_input(current_day)

nums = []
for l in input_str.splitlines():
    firstNum = '0'
    lastNum = '0'
    for j in l:
        if j.isnumeric():
            firstNum = j
            break
    for j in reversed(l):
        if j.isnumeric():
            lastNum = j
            break
    fullNum = firstNum + lastNum
    nums.append(int(fullNum))
print(sum(nums))

# WRITE YOUR SOLUTION HERE

