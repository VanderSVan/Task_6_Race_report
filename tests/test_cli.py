import pytest
from src.reporting.cli import create_arguments


class TestCreateArguments:
    @pytest.mark.parametrize('arguments, result', [
        (["-f", "files_folder"],
         "Namespace(files='files_folder', driver=None, desc=False)"),
        (["-f", "files_folder", "--desc"],
         "Namespace(files='files_folder', driver=None, desc=True)"),
        (["-f", "files_folder", "-d", "Lewis Hamilton"],
         "Namespace(files='files_folder', driver='Lewis Hamilton', desc=False)")
    ])
    def test_create_arguments(self, arguments, result):
        assert str(create_arguments(arguments)) == result
