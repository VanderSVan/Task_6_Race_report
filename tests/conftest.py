import pytest
from unittest.mock import Mock
from datetime import datetime as dt
from src.reporting.report import Driver
from tests.test_report import TestDriver


@pytest.fixture(scope='class')
def fixture_create_drivers():
    """
    Creates mocked instances of Driver.
    """
    abbreviations = ['DRR', 'SVF', 'BHS']
    brief_stats = [['Daniel Ricciardo', 'RED BULL RACING TAG HEUER', '2'],
                   ['Sebastian Vettel', 'FERRARI', '1'],
                   ['Brendon Hartley', 'SCUDERIA TORO ROSSO HONDA', '3']]
    time = [2, 1, 3]
    drivers = {abbr: Mock(time=time) for abbr, time in zip(abbreviations, time)}
    for name_driver, stats in zip(drivers, brief_stats):
        drivers[name_driver].get_stats = stats
    return drivers


@pytest.fixture()
def fixture_instance_driver():
    """
    Restores the values of an instance of the "Driver" class.
    """
    yield
    # format for datetime
    f = "%Y-%m-%d %I:%M:%S.%f"
    TestDriver.instance_driver = Driver('LHM', 'Lewis Hamilton', 'MERCEDES',
                                        dt.strptime('2018-05-24 12:18:20.125', f),
                                        dt.strptime('2018-05-24 1:11:32.585', f))
