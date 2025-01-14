import requests
from os.path import exists


def get_session_id(filename):
    with open(filename) as f:
        return f.read().strip()


def get_url(year, day):
    return f"https://adventofcode.com/{year}/day/{day}/input"


def print_hlight(text):
    print('\033[43m\033[92m', text, '\033[0m')

def print_tlight(text):
    print('\033[93m', text, '\033[0m')


YEAR = 2023
SESSION_ID_FILE = "session.cookie"
SESSION = get_session_id(SESSION_ID_FILE)
HEADERS = {
    "User-Agent": "github.com/nrsherr2/advent-of-code-2023-python"
}
COOKIES = {"session": SESSION}


def get_input(day):
    path = f"inputs/{day:02d}"

    if not exists(path):
        url = get_url(YEAR, day)
        response = requests.get(url, headers=HEADERS, cookies=COOKIES)
        if not response.ok:
            raise RuntimeError(
                f"Request failed\n\tstatus code: {response.status_code}\n\tmessage: {response.content}"
            )
        with open(path, "w") as f:
            f.write(response.text[:-1])

    with open(path, "r") as f:
        return f.read()


def get_test_input(day):
    path = f"test_inputs/{day:02d}"
    if not exists(path):
        with open(path, "w") as f:
            f.write("")
        return None
    with open(path, "r") as f:
        return f.read()
