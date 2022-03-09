import os
import pytest
from pathlib import Path
from unittest import mock
from datetime import datetime as dt
from src.reporting.report import read_file
from src.reporting.report import parse_abbreviations_file
from src.reporting.report import parse_time_file
from src.reporting.report import get_abs_file_path
from src.reporting.report import create_drivers_dict
from src.reporting.report import get_driver_stats
from src.reporting.report import sort_drivers_dict
from src.reporting.report import build_report
from src.reporting.report import Driver
from src.reporting.report import DriverNameException
from src.reporting.report import abbreviations, start, end

# format for datetime
f = "%Y-%m-%d %H:%M:%S.%f"
# Parametrize for TestCreateDriversDict:
list_param_for_create_drivers_dict = [
    ([['DRR', 'Daniel Ricciardo', 'RED BULL RACING TAG HEUER'], ['SVF', 'Sebastian Vettel', 'FERRARI']],  # parsed_abbr
     {'DRR': dt.strptime('2018-05-24 12:14:12.054', f),  # parsed_start
      'SVF': dt.strptime('2018-05-24 12:02:58.917', f)},
     {'DRR': dt.strptime('2018-05-24 1:11:24.067', f),  # parsed_end
      'SVF': dt.strptime('2018-05-24 1:04:03.332', f)},
     # result:
     {'DRR': Driver(abbr='DRR', name='Daniel Ricciardo', team='RED BULL RACING TAG HEUER',
                    start=dt.strptime('2018-05-24 12:14:12.054000', f),
                    end=dt.strptime('2018-05-24 1:11:24.067000', f)),
      'SVF': Driver(abbr='SVF', name='Sebastian Vettel', team='FERRARI',
                    start=dt.strptime('2018-05-24 12:02:58.917000', f),
                    end=dt.strptime('2018-05-24 1:04:03.332000', f))
      })
]


class TestDriver:
    attributes = ['LHM', 'Lewis Hamilton', 'MERCEDES',
                  dt.strptime('2018-05-24 12:18:20.125', f),
                  dt.strptime('2018-05-24 12:19:20.125', f)]
    instance_driver = Driver(*attributes)

    def test_initial_value(self):
        dict_atrrs = self.instance_driver.__dict__
        for i, attr in enumerate(dict_atrrs):
            assert dict_atrrs[attr] == self.attributes[i]

    def test_add_time(self):
        assert str(self.instance_driver.time) == '0:01:00'

    @pytest.mark.parametrize('start_time, end_time', [
        # delta = 0
        (dt.strptime('2018-05-24 12:14:12.054', f), dt.strptime('2018-05-24 12:14:12.054', f)),
        # negative delta
        (dt.strptime('2018-05-24 12:14:12.054', f), dt.strptime('2018-05-24 12:00:00.000', f)),
        # end_time is None
        (dt.strptime('2018-05-24 12:14:12.054', f), None),
        # start and end times is None
        (None, None)
    ])
    def test_give_wrong_time(self, start_time, end_time, fixture_instance_driver):
        self.instance_driver.start = start_time
        self.instance_driver.end = end_time
        assert self.instance_driver.time is None

    @pytest.mark.parametrize('start_time, end_time, result', [
        # correct delta_time
        (dt.strptime('2018-05-24 12:18:20.125', f), dt.strptime('2018-05-24 12:20:32.585', f),
         ['Lewis Hamilton', 'MERCEDES', '0:02:12.460']),
        # negative delta
        (dt.strptime('2018-05-24 12:14:12.054', f), dt.strptime('2018-05-24 12:00:00.000', f),
         ['Lewis Hamilton', 'MERCEDES', 'incorrect time']),
        # end time is None
        (dt.strptime('2018-05-24 12:14:12.054', f), None,
         ['Lewis Hamilton', 'MERCEDES', "incorrect time"])
    ])
    def test_get_stats(self, start_time, end_time, result, fixture_instance_driver):
        self.instance_driver.start = start_time
        self.instance_driver.end = end_time
        assert self.instance_driver.get_stats == result


class TestBuildReport:
    # See param for this class in conftest.py
    @pytest.mark.parametrize('descending, result', [
        (False, [['Sebastian Vettel', 'FERRARI', '1'],
                 ['Daniel Ricciardo', 'RED BULL RACING TAG HEUER', '2'],
                 ['Brendon Hartley', 'SCUDERIA TORO ROSSO HONDA', '3']]),
        (True, [['Brendon Hartley', 'SCUDERIA TORO ROSSO HONDA', '3'],
                ['Daniel Ricciardo', 'RED BULL RACING TAG HEUER', '2'],
                ['Sebastian Vettel', 'FERRARI', '1']],)
    ])
    def test_build_report(self, descending, result, fixture_create_drivers: dict):
        assert build_report(fixture_create_drivers, descending) == result


class TestSortDriversDict:
    # See param for this class in conftest.py
    @pytest.mark.parametrize('descending, result', [
        (False, ['SVF', 'DRR', 'BHS']),
        (True, ['BHS', 'DRR', 'SVF'])
    ])
    def test_sort_drivers_dict(self, descending, result, fixture_create_drivers: dict):
        assert list(sort_drivers_dict(fixture_create_drivers, descending).keys()) == result


class TestGetDriverStats:
    # See param for this class in conftest.py
    def test_get_wrong_name(self, fixture_create_drivers: dict):
        with pytest.raises(DriverNameException) as exc_info:
            get_driver_stats(fixture_create_drivers, 'Bobby Kotick')
        raised_exception = exc_info.value
        assert str(raised_exception) == "Abbreviation 'Bobby Kotick' not found"

    def test_get_driver_stats(self, fixture_create_drivers: dict):
        assert (get_driver_stats(fixture_create_drivers, 'BHS') ==
                "Brendon Hartley | SCUDERIA TORO ROSSO HONDA | 3")


class TestCreateDriversDict:
    @pytest.mark.parametrize('parsed_abbr, parsed_start, parsed_end, result', list_param_for_create_drivers_dict)
    @mock.patch('src.reporting.report.parse_time_file')
    @mock.patch('src.reporting.report.parse_abbreviations_file')
    @mock.patch('src.reporting.report.get_abs_file_path')
    def test_create_drivers_dict(self, mock_files_path, mock_parse_abbr, mock_parse_start_end,
                                 parsed_abbr, parsed_start, parsed_end, result):
        mock_parse_abbr.return_value = parsed_abbr
        mock_parse_start_end.side_effect = parsed_start, parsed_end
        assert create_drivers_dict('folder path') == result


@mock.patch('src.reporting.report.os.path.exists')
class TestGetAbsFilePath:
    @pytest.mark.parametrize('folder_path, file_name, result', [
        ('folder_path', abbreviations, f"Path 'folder_path\\{abbreviations}' not found"),
        ('path/to/folder', end, f"Path 'path/to/folder\\{end}' not found"),
        (Path('folder_path'), start, f"Path 'folder_path\\{start}' not found")
    ])
    def test_give_folder_without_required_file(self, mock_exists, folder_path, file_name: str, result: str):
        mock_exists.return_value = False
        with pytest.raises(FileNotFoundError) as exc_info:
            get_abs_file_path(folder_path, file_name)
        exception_raised = exc_info.value
        assert str(exception_raised) == result

    @pytest.mark.parametrize('folder_path, file_name, result', [
        ('folder_path', abbreviations, os.path.join(os.getcwd(), 'folder_path', abbreviations)),
        ('path/to/folder', start, os.path.join(os.getcwd(), 'path', 'to', 'folder', start)),
        (Path('folder_path'), end, os.path.join(os.getcwd(), 'folder_path', end))
    ])
    def test_get_abs_file_path(self, mock_exists, folder_path, file_name, result: str):
        mock_exists.return_value = True
        assert str(get_abs_file_path(folder_path, file_name)) == result


class TestParseAbbreviationsFile:
    @pytest.mark.parametrize('file_txt_content, result', [
        (
                ['DRR_Daniel Ricciardo_RED BULL RACING TAG HEUER'],
                [['DRR', 'Daniel Ricciardo', 'RED BULL RACING TAG HEUER']]),
        (
                ['DRR_Daniel Ricciardo_RED BULL RACING TAG HEUER', 'SVF_Sebastian Vettel_FERRARI'],
                [['DRR', 'Daniel Ricciardo', 'RED BULL RACING TAG HEUER'], ['SVF', 'Sebastian Vettel', 'FERRARI']]
        )
    ])
    def test_give_txt_file(self, file_txt_content: list, result: list):
        with mock.patch('src.reporting.report.read_file', return_value=file_txt_content):
            assert parse_abbreviations_file('file_path') == result


class TestParseTimeFile:
    @pytest.mark.parametrize('file_log_content, result', [
        (
                ['SVF2018-05-24_12:02:58.917'],
                "{'SVF': datetime.datetime(2018, 5, 24, 12, 2, 58, 917000)}"
        ),
        (
                ['MES2018-05-24_1:05:58.778', 'RGH2018-05-24_1:06:27.441'],
                "{'MES': datetime.datetime(2018, 5, 24, 1, 5, 58, 778000),"
                " 'RGH': datetime.datetime(2018, 5, 24, 1, 6, 27, 441000)}"
        )
    ])
    def test_give_log_file(self, file_log_content: list, result: dict):
        with mock.patch('src.reporting.report.read_file', return_value=file_log_content):
            assert str(parse_time_file('file_path')) == result


class TestReadFile:
    def test_read_file(self):
        with mock.patch('builtins.open', mock.mock_open(read_data="qwe\nrty\n   \n  ")):
            assert read_file("path/to/file") == ['qwe', 'rty']
