"""
IT - Internal Tracer
Copyright (C) 2019 Erich Studer

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
import pytest
import Client
import lib

def test_init(mocker):
	value = 42
	mocker.patch.object(Client.Client, 'start', return_value=value)
	mocker.patch.object(Client, '__name__', '__main__')
	exit_mock = mocker.patch.object(Client.sys, 'exit')

	Client.init()
	exit_mock.assert_called_once_with(value)


def test_start_startupMessage(mocker):
	print_mock = mocker.patch('builtins.print')
	mocker.patch.object(Client.ClientParser, 'run')

	Client.Client.start()

	print_mock.assert_called_once_with('client started')


def test_start_setupWindow(mocker):
	mocker.patch('builtins.print')
	setupWindow_mock = mocker.patch.object(Client.Client, '_setupWindow')
	mocker.patch.object(Client.ClientParser, 'run')

	Client.Client.start()

	setupWindow_mock.assert_called_once_with()

	
def test_start_runClientParser(mocker):
	mocker.patch('builtins.print')
	
	initFile = 'myInitFile'
	sessionFile = 'mySessionFile'
	mocker.patch.object(Client.Client, '_parseArguments', return_value={'initFile': initFile, 'sessionFile': sessionFile})
	run_mock = mocker.patch.object(Client.ClientParser, 'run')

	Client.Client.start()

	run_mock.assert_called_once_with(initFile=initFile, sessionFile=sessionFile)


def test_setupWindow_win(mocker):
	system_mock = mocker.patch.object(Client.sys, 'platform', 'win')
	system_mock = mocker.patch.object(Client.os, 'system')

	Client.Client._setupWindow()

	system_mock.assert_any_call("mode 70,15")
	system_mock.assert_any_call("title IT client")
	assert system_mock.call_count == 2


def test_setupWindow_notWin(mocker):
	mocker.patch.object(Client.sys, 'platform', 'myOs')
	system_mock = mocker.patch.object(Client.os, 'system')

	Client.Client._setupWindow()

	system_mock.assert_not_called()


@pytest.mark.parametrize('arguments, expectation',
			 [([], {'initFile': None, 'sessionFile': 'mySession.session'}),
			  (['', '-initFile', 'myInitFile'], {'initFile': 'myInitFile', 'sessionFile': 'mySession.session'}),
			  (['', '-sessionFile', 'mySessionFile'], {'initFile': None, 'sessionFile': 'mySessionFile'}),
			  (['', '-initFile', 'myInitFile', '-sessionFile', 'mySessionFile'], {'initFile': 'myInitFile', 'sessionFile': 'mySessionFile'}),
			  (['', '-sessionFile', 'mySessionFile', '-initFile', 'myInitFile'], {'initFile': 'myInitFile', 'sessionFile': 'mySessionFile'}),
			 ])
def test_parseArguments(mocker, arguments, expectation):
	mocker.patch.object(Client.sys, 'argv', arguments)

	assert Client.Client._parseArguments() == expectation
