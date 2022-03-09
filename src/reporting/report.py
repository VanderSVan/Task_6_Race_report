import os
from pyparsing import Word, alphas, nums, Suppress, pyparsing_unicode
from datetime import datetime as dt
from datetime import timedelta
from dataclasses import dataclass
from collections import OrderedDict
from beautifultable import BeautifulTable as BT

# These files are required for the module to work.
abbreviations = 'abbreviations.txt'
start = 'start.log'
end = 'end.log'


@dataclass
class Driver:
    """
    Creates instances of a class that has the following parameters:
    abbreviation, full name, team, race start time, race end time.
    """
    abbr: str
    name: str
    team: str
    start: dt
    end: dt

    @property
    def time(self) -> timedelta or None:
        """
        Subtracts the start time from the end time.
        :return: instance 'datetime.timedelta'.
        """
        if self.end and self.start:
            delta = self.end - self.start
            if delta.total_seconds() <= 0:
                delta = None
        else:
            delta = None
        return delta

    @property
    def get_stats(self) -> [str, str, str]:
        """
        Generates statistic for driver.
        """
        output_time = ('incorrect time' if isinstance(self.time, type(None))
                       else str(self.time)[:-3])
        return [self.name, self.team, output_time]


@dataclass
class DriverNameException(Exception):
    """
    :raises Exception if the driver's name does not exist
    """
    text_err: str


def print_report(report: list, desc=False):
    """
    Gets a report in the form of a list and prints it item by item.
    """
    top_drivers_number = abs(len(report) - 15) if desc else 15
    table1 = BT()
    table2 = BT()
    for i, driver in enumerate(report, 1):
        if i > top_drivers_number:
            table2.rows.append([f"{i}. {driver[0]}", driver[1], driver[2]])
        else:
            table1.rows.append([f"{i}. {driver[0]}", driver[1], driver[2]])
    for table in table1, table2:
        table.columns.alignment = BT.ALIGN_LEFT
        table.set_style(BT.STYLE_NONE)
        table.columns.separator = "|"
    if len(report) > 15:
        table1.border.bottom = "_"
        print(table1)
        print(table2)
    else:
        print(table1)
    print("\n", end='')


def build_report(drivers: dict, desc=False) -> [[str, str, str], ...]:
    """
    Creates a race report: [[Driver.name, Driver.team, Driver.time], ...]
    Default order of drivers from best time to worst.
    """
    sorted_drivers = sort_drivers_dict(drivers, desc)
    return [driver.get_stats for driver in sorted_drivers.values()]


def sort_drivers_dict(drivers: dict, desc=False) -> {str: Driver}:
    """
    Sorts the dictionary by the final race time.
    Default order of drivers from best time to worst.
    :return: sorted dict as
             keys: driver's abbreviation,
             values: instances of the 'Driver' class.
    """
    return OrderedDict(sorted(drivers.items(),
                              key=lambda items: (isinstance(items[1].time, type(None)), items[1].time),
                              reverse=desc))


def get_driver_stats(drivers: dict, abbreviation: str) -> str or DriverNameException:
    """
    Generates and returns statistics for the driver.
    If the driver's abbreviation not found raises error.
    """
    try:
        abbr = abbreviation.upper()
    except AttributeError:
        abbr = None
    if drivers.get(abbr):
        return " | ".join(drivers[abbr].get_stats)
    raise DriverNameException(f"Abbreviation '{abbreviation}' not found")


def create_drivers_dict(folder_path) -> {str: Driver}:
    """
    Main function.
    Creates instances of the 'Driver' class with all stats.
    :return: dict as
             keys: driver's abbreviation,
             values: instances of the 'Driver' class.
    """
    abbr_path = get_abs_file_path(folder_path, abbreviations)
    start_path = get_abs_file_path(folder_path, start)
    end_path = get_abs_file_path(folder_path, end)
    list_abbr = parse_abbreviations_file(abbr_path)
    dict_start = parse_time_file(start_path)
    dict_end = parse_time_file(end_path)
    return {abbr: Driver(abbr, name, team, dict_start.get(abbr), dict_end.get(abbr))
            for abbr, name, team in list_abbr}


def get_abs_file_path(folder_path, file_name: str) -> str:
    """
    Concatenates paths and checks the resulting path for existence, like that:
    'folder_path', 'file_name' -> D:/path/to/folder_path/file_name.
    """
    file_path = os.path.join(folder_path, file_name)
    if os.path.exists(file_path):
        return os.path.abspath(file_path)
    raise FileNotFoundError(f"Path '{file_path}' not found")


def parse_abbreviations_file(file_path) -> [[str, str, str], ...]:
    """
    Parses line by line, like that:
    'str1_str2_str3' -> ['str1', 'str2', 'str3']
    """
    list_lines = read_file(file_path)
    letters = pyparsing_unicode.Latin1.alphas
    expr = Word(letters + " ")
    full_expr = expr + Suppress("_") + expr + Suppress("_") + expr
    return [full_expr.parseString(line_).asList() for line_ in list_lines]


def parse_time_file(file_path) -> {str: dt}:
    """
    Parses line by line, like that:
    'StringDate_Time' -> {'String': datetime(y, m, d, H, M, S, mS)}
    """
    list_lines = read_file(file_path)
    datetime_format = "%Y-%m-%d %H:%M:%S.%f"
    abbr = Word(alphas)
    date = Word(nums + "-")
    time = Word(nums + ":" + ".")
    expr = abbr + date + Suppress("_") + time
    parsed_list = [expr.parseString(line_).asList() for line_ in list_lines]
    return {abbr: dt.strptime((date + " " + time), datetime_format) for abbr, date, time in parsed_list}


def read_file(file_path) -> [str, str, ...]:
    """
    Reads the file removing whitespace.
    :return: list of file lines.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            file_lines = [line.strip() for line in file if len(line.strip()) > 0]
            return file_lines
    except Exception as err:
        print(f"\n-----Error-----\n"
              f"{err}.\n")


if __name__ == '__main__':
    drivers_dict = create_drivers_dict("../../data_files")
    descending = False
    drivers_report = build_report(drivers_dict, descending)
    print_report(drivers_report, descending)