import os

l = filter(lambda x: "__" not in x and ".py" in x, os.listdir("src"))
l = list(l)
n = int(sorted(l)[-1][:2]) + 1 if len(l) > 0 else 1

DEFAULT_FILE = f"from utils.api import get_input, get_test_input\nimport time\n\ncurrent_day = {n}\ninput_str = get_input(current_day)\ntest_str = get_test_input(current_day)\nstartTime = time.time()\n\n# WRITE YOUR SOLUTION HERE\n\nprint(\"--- %s seconds ---\" % (time.time() - startTime))\n"

path = f"src/{n:02d}.py"
with open(path, "w") as f:
    f.write(DEFAULT_FILE)

print(f"Enter your solution in {path}")
