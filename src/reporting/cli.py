import argparse
from pyparsing import ParseException
from .report import abbreviations, start, end
from .report import create_drivers_dict
from .report import build_report
from .report import print_report
from .report import get_driver_stats
from .report import DriverNameException


def create_arguments(args_to_simulate_cli=None):
    """
    Create arguments: '--files'(file path),
                      '--driver'(driver's name),
                      '--desc'(descending order).
    """
    parser = argparse.ArgumentParser(prog="report.py",
                                     description="Create drivers report for race",
                                     epilog="Try '-f <folder_path> --desc'")
    parser.add_argument("-f", "--files", metavar="", type=str, required=True,
                        help="path to folder with race files")
    parser.add_argument("-d", "--driver", metavar="", type=str,
                        help="shows statistic about driver")
    parser.add_argument("--desc", action="store_const", const=True, default=False,
                        help="descending order (default: ascending order)")
    return parser.parse_args(args_to_simulate_cli)


def _print_exc(error):
    """
    Prints exception with description.
    """
    print(f"\n-----Error-----\n"
          f"{error}.\n")


def _print_parse_exc():
    """
    Prints exception 'ParseException' with description.
    """
    print(f"\n-----Error-----\n"
          f"Your file or files doesn't match patterns.\n"
          f"File '{abbreviations}' should contain the following spelling pattern: 'abbreviations_name_team'\n"
          f"Files '{start}' or '{end}' should contain the following spelling pattern: 'StringDate_Time'\n")


def main(args_to_simulate_cli=None):
    """
    Prints result working module 'report.py'.
    """
    args = create_arguments(args_to_simulate_cli)
    try:
        drivers = create_drivers_dict(args.files)
    except ValueError as err:
        _print_exc(err)
    except ParseException:
        _print_parse_exc()
    except Exception as err:
        _print_exc(err)
    else:
        if args.driver:
            try:
                print(get_driver_stats(drivers, args.driver))
            except DriverNameException as err:
                _print_exc(err)
        else:
            drivers_report = build_report(drivers, args.desc)
            print_report(drivers_report, args.desc)


if __name__ == '__main__':
    # If you want to simulate cli, then uncomment following line:
    # main(["-f", "D:/your/path/to/files_folder", "--desc"])
    main()
