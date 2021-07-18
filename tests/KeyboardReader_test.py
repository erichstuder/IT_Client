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

import time
import lib.KeyboardReader as KeyboardReader

def test_keyboardReader_threadCreation(mocker):
	Thread_mock = mocker.patch.object(KeyboardReader.Thread, '__init__')
	mocker.patch.object(KeyboardReader.Thread, 'daemon')
	parser_stub = mocker.stub()

	keyboardReader = KeyboardReader.KeyboardReader(parser_stub)
	Thread_mock.assert_called_once_with(target=mocker.ANY)
	assert keyboardReader.daemon is True


def test_keyboardReader_threadStart(mocker):
	Thread_start_mock = mocker.patch.object(KeyboardReader.Thread, 'start')

	keyboardReader = KeyboardReader.KeyboardReader(None)
	Thread_start_mock.assert_not_called()
	keyboardReader.start()
	Thread_start_mock.assert_called_once_with()


def test_keyboardReader(mocker):
	inputValue = 'a'
	input_mock = mocker.patch('builtins.input', return_value=inputValue)
	parser_stub = mocker.stub()

	keyboardReader = KeyboardReader.KeyboardReader(parser_stub)
	keyboardReader.start()
	time.sleep(0.1)
	keyboardReader.stop()

	parser_stub.assert_called_with(inputValue)
