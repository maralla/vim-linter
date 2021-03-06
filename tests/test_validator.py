import json
import tempfile
import mock
import vim

from validator import Validator


class NoName(Validator):
    __filetype__ = 'no-name'

    checker = "ls"
    args = "-a -b -c -d"
    args_option = binary_option = 'no_name'
    regex = r"""
            (?P<lnum>\d+):
            (?P<col>\d+)
            \s
            (?P<type>\w+):
            \s
            (?P<text>.*)"""


def test_parse_loclist():
    loclist = [
        'hello world',
        '123:45 error: hello wrold',
        '456:9 warning: abcd'
    ]

    data = NoName().parse_loclist(loclist, 1)
    assert json.loads(data) == [
        {
            "lnum": "123",
            "text": "[ls]hello wrold",
            "enum": 2,
            "type": "E",
            "col": "45",
            "bufnr": 1
        },
        {
            "lnum": "456",
            "text": "[ls]abcd",
            "enum": 3,
            "type": "W",
            "col": "9",
            "bufnr": 1
        }
    ]


def test_format_cmd():
    with tempfile.NamedTemporaryFile() as fp:
        cmd = NoName().format_cmd(fp.name)

    assert cmd == 'ls -a -b -c -d {}'.format(fp.name)


def test_binary():
    assert NoName().binary == 'ls'
    with mock.patch.dict(vim.vars, {'validator_no_name_binary': b'lls'}):
        assert NoName().binary == 'lls'


def test_args():
    assert NoName().cmd_args == '-a -b -c -d'
    with mock.patch.dict(vim.vars, {'validator_no_name_args': b'-l'}):
        assert NoName().cmd_args == '-l'
