import argparse
import pathlib, shutil
import os, sys
from datetime import date
import requests


def ask_user(message):
    if args.yes:
        print(message + "y")
        return True
    res = input(message)
    return res.lower() in ["y", "yes"]


def ask_to_continue(message):
    if not ask_user(message):
        print("Aborting...")
        sys.exit(1)


today = date.today()
parser = argparse.ArgumentParser(description="Initialize daily exercise")
parser.add_argument(
    "day",
    nargs="?",
    type=int,
    help=f"Day of advent. Default: today ({today.day})",
    default=today.day,
)
parser.add_argument(
    "--year",
    type=int,
    help=f"Year. Default: current year ({today.year})",
    default=today.year,
)
parser.add_argument(
    "--dir",
    type=str,
    help=f"Directory. Default: './day<n>'",
)
parser.add_argument(
    "--yes",
    help="Answer yes to all questions",
    action="store_true",
    default=False,
)

args = parser.parse_args()

day = args.day
year = args.year
directory = args.dir or f"./day{day}"
template = "./template.py"

print(f"Initializing day {day} {year}, in {directory}\n")

print(f" - Creating directory: {directory}")
if os.path.exists(directory):
    ask_to_continue(f" ! Directory already exists. Continue? (y/n) ")

path = pathlib.Path(directory)
path.mkdir(parents=True, exist_ok=True)

src = template
dst = os.path.join(directory, f"day{day}.py")
print(f" - Copy template: {src} -> {dst}")
skip = False
if os.path.exists(dst):
    if not ask_user(" ! File already exists. Overwrite? (y/n) "):
        skip = True
if not skip:
    shutil.copyfile(src, dst)

dst = os.path.join(directory, "example.txt")
print(f" - Create empty example data: {dst}")
if os.path.exists(dst):
    print(f" ! Example data already exists. Skipping...")
else:
    with open(dst, "w") as fp:
        pass

dst = os.path.join(directory, "input.txt")
print(f" - Downloading and writing input data to {dst}")
skip = False
if os.path.exists(dst):
    skip = True
    if ask_user(" ! File already exists. Overwrite? (y/n) "):
        skip = False

src = "./.cookie"
print(f" - Reading cookie from {src}")
try:
    with open(src) as f:
        cookie = f.read()
except FileNotFoundError as e:
    print(e)
    print(" ! Cookie not found! Please copy from browser and save as './cookie'")
    print("Aborting...")
    sys.exit(1)

base_url = f"https://adventofcode.com/{year}/day/{day}"

if not skip:
    print("   - Downloading input")
    input_url = f"{base_url}/input"
    cookies = {"session": cookie.strip()}
    res = requests.get(input_url, cookies=cookies)
    if res.status_code == 404:
        print("   ! Got a 404. Is the input not released yet? Try again later...")
        print("Aborting ...")
        sys.exit(1)
    res.raise_for_status()
    data = res.text

    print(f"   - Writing input to {dst}")
    with open(dst, "w") as f:
        f.write(data)

print("\nAll done. Good luck!")
