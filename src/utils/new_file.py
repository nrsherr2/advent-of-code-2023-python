import os

l = filter(lambda x: "__" not in x and ".py" in x, os.listdir("src"))
l = list(l)
n = int(sorted(l)[-1][:2]) + 1 if len(l) > 0 else 1

DEFAULT_FILE = "from utils.api import get_input, get_test_input\n\ncurrent_day = {d}\ninput_str = get_input(current_day)\ntest_str = get_test_input(current_day)\n\n# WRITE YOUR SOLUTION HERE\n"
fileName = "src/{d:02d}.py"
pth = fileName.format(d=n)
with open(pth, "w") as f:
    f.write(DEFAULT_FILE.format(d=n))

print("Enter your solution in {path}".format(path=pth))
