import os

l = filter(lambda x: "__" not in x and ".py" in x, os.listdir("src"))
l = list(l)
n = int(sorted(l)[-1][:2]) + 1 if len(l) > 0 else 1

DEFAULT_FILE = "from utils.api import get_input, get_test_input, print_hlight, print_tlight\nimport time\n\ncurrent_day = {d}\ninput_str = get_input(current_day)\ntest_str = get_test_input(current_day)\n\ndef part1(fullInput):\n    print(fullInput)\n\ndef part2(fullInput):\n    print(fullInput)\n\n# solutions corner\n\nstartTime = time.time()\n\npart1Test = part1(test_str)\nprint_hlight(part1(input_str))\n\npart2Test = part2(test_str)\nprint_hlight(part2(test_str))\n\nprint_tlight(\"--- %s seconds ---\" % (time.time() - startTime))\n"
fileName = "src/{d:02d}.py"
pth = fileName.format(d=n)
with open(pth, "w") as f:
    f.write(DEFAULT_FILE.format(d=n))

print("\033[46m\033[35mEnter your solution in {path}\033[0m".format(path=pth))
