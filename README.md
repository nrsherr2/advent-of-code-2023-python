# Advent of code
Problems list:
1. [01](https://github.com/nrsherr2/advent-of-code-2023-python/blob/main/src/01.py)
2. [02](https://github.com/nrsherr2/advent-of-code-2023-python/blob/main/src/02.py)
3. [03](https://github.com/nrsherr2/advent-of-code-2023-python/blob/main/src/03.py)
4. [04](https://github.com/nrsherr2/advent-of-code-2023-python/blob/main/src/04.py)
5. [05](https://github.com/nrsherr2/advent-of-code-2023-python/blob/main/src/05.py)
6. [06](https://github.com/nrsherr2/advent-of-code-2023-python/blob/main/src/06.py)
7. [07](https://github.com/nrsherr2/advent-of-code-2023-python/blob/main/src/07.py)
8. [08](https://github.com/nrsherr2/advent-of-code-2023-python/blob/main/src/08.py)
9. [09](https://github.com/nrsherr2/advent-of-code-2023-python/blob/main/src/09.py)
10. [10](https://github.com/nrsherr2/advent-of-code-2023-python/blob/main/src/10.py)
11. [11](https://github.com/nrsherr2/advent-of-code-2023-python/blob/main/src/11.py)
12. [12](https://github.com/nrsherr2/advent-of-code-2023-python/blob/main/src/12.py)
13. [13](https://github.com/nrsherr2/advent-of-code-2023-python/blob/main/src/13.py)
14. [14](https://github.com/nrsherr2/advent-of-code-2023-python/blob/main/src/14.py)
15. [15](https://github.com/nrsherr2/advent-of-code-2023-python/blob/main/src/15.py)
16. [16](https://github.com/nrsherr2/advent-of-code-2023-python/blob/main/src/16.py)
17. [17](https://github.com/nrsherr2/advent-of-code-2023-python/blob/main/src/17.py)
18. [18](https://github.com/nrsherr2/advent-of-code-2023-python/blob/main/src/18.py)
19. [19](https://github.com/nrsherr2/advent-of-code-2023-python/blob/main/src/19.py)
20. [20](https://github.com/nrsherr2/advent-of-code-2023-python/blob/main/src/20.py) 
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
        

Created via: [advent-of-code-setup](https://github.com/tomfran/advent-of-code-setup)