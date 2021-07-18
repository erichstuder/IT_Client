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
import time
import lib.KeyboardReader as KeyboardReader

@pytest.fixture()
def keyboardReader(mocker):
	mocker.patch('builtins.input')
	parser_stub = mocker.stub()
	keyboardReader = KeyboardReader.KeyboardReader(parser_stub)
	yield keyboardReader
	keyboardReader.stop()
	while keyboardReader.is_alive():
		pass


def test_keyboardReader_threadCreation(mocker):
	Thread_mock = mocker.patch.object(KeyboardReader.Thread, '__init__')
	mocker.patch.object(KeyboardReader.Thread, 'daemon')
	keyboardReader = KeyboardReader.KeyboardReader(None)
	Thread_mock.assert_called_once_with(target=mocker.ANY)


def test_keyboardReader_daemon(keyboardReader):
	assert keyboardReader.daemon is True


def test_keyboarReader_start(keyboardReader, mocker):
	assert keyboardReader.is_alive() is False
	keyboardReader.start()
	assert keyboardReader.is_alive() is True
	

def test_keyboardReader(mocker):
	inputValue = 'a'
	input_mock = mocker.patch('builtins.input', return_value=inputValue)
	parser_stub = mocker.stub()

	keyboardReader = KeyboardReader.KeyboardReader(parser_stub)
	keyboardReader.start()

	parser_stub.assert_called_with(inputValue)

	keyboardReader.stop()
	while keyboardReader.is_alive():
		pass
