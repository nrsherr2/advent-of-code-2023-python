import os

base_link = "https://github.com/nrsherr2/advent-of-code-2023-python/blob/main/src/"


def parse(e):
    name = e.replace(".py", "")
    # name = " ".join(name.split("_")[1:])
    # return f"[{name}]({base_link}{e})"
    return "[{}]({}{})".format(name, base_link, e)


solutions = filter(lambda x: ".py" in x and "init" not in x and "all" not in x, os.listdir("src"))

readme_content = "# Advent of code\nProblems list:\n"
tmp = ["{}. {}".format(i + 1, parse(e)) for i, e in enumerate(sorted(solutions))]
# tmp = [f"{i+1}. {parse(e)}" for i, e in enumerate(sorted(solutions))]
readme_content += "\n".join(tmp)

with open("README.md", "w") as f:
    f.write(
        readme_content
        + """ 
## Creating a new solution

```make new``` creates a new file for today, it checks for the files in `src/` and creates the "next int" one. On the first run it will create `01.py`, later `02.py`, and so on.

A new solution is initialized as follows: 
```python
from utils.api import get_input, get_test_input, print_hlight, print_tlight
import time

current_day = 1
input_str = get_input(current_day)
test_str = get_test_input(current_day)

def part1(fullInput):
    print(fullInput)

def part2(fullInput):
    print(fullInput)

# solutions corner

startTime = time.time()

part1Test = part1(test_str)
print_hlight(part1(input_str))

part2Test = part2(test_str)
print_hlight(part2(test_str))

print_tlight("--- %s seconds ---" % (time.time() - startTime))

```
The `get_input` function takes a day and returns the content of the input for that day, this internally makes a request to obtain the input if it is not found on disk. 

## Running a new solution

From the main directory, run `python src/<DAY>.py`.
        """
        + "\n\nCreated via: [advent-of-code-setup](https://github.com/tomfran/advent-of-code-setup)"
    )
