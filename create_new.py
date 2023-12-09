from io import TextIOWrapper
from os.path import exists

import click

YEAR = 2023


def parse_lines(file: TextIOWrapper, day_number: int):
    for line in file:
        if "input_N" in line:
            yield line.replace("input_N", f"input_{day_number}")
        else:
            yield line


def create_new(day_number: int):
    with open("solution_template.py", "r", newline="\n") as in_file:
        with open(f"{YEAR}/solution_{day_number}.py", "w", newline="\n") as out_file:
            out_file.writelines(parse_lines(in_file, day_number))

    with open(f"{YEAR}/input_{day_number}_full", "x"):
        pass
    with open(f"{YEAR}/input_{day_number}_test", "x"):
        pass


@click.command()
@click.option("-d", "--day", type=int, required=True)
def main(day: int):
    if exists(f"{YEAR}/solution_{day}.py"):
        raise FileExistsError(f"File for day {day} already exists, exiting...")
    create_new(day)


if __name__ == "__main__":
    main()
