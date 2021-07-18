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
import threading
import lib.ComportLogger as ComportLogger

@pytest.fixture()
def comportLogger(mocker):
	mocker.patch('builtins.input')
	parser_stub = mocker.stub()
	comportLogger = ComportLogger.ComportLogger(parser_stub, None)
	yield comportLogger
	comportLogger.stop()
	while comportLogger.is_alive():
		pass


def test_comportLogger_threadCreation(mocker):
	Thread_mock = mocker.patch.object(ComportLogger.Thread, '__init__')
	mocker.patch.object(ComportLogger.Thread, 'daemon')
	comportLogger = ComportLogger.ComportLogger(None, None)
	Thread_mock.assert_called_once_with(target=mocker.ANY)


def test_comportLogger_daemon(comportLogger):
	assert comportLogger.daemon is True


def test_comportLogger_start(comportLogger, mocker):
	assert comportLogger.is_alive() is False
	comportLogger.start()
	assert comportLogger.is_alive() is True


def test_comportLogger(mocker, tmpdir):
	logValue = b'abc'
	comportHandler_stub = mocker.stub()
	mocker.patch.object(comportHandler_stub, 'read', create=True, return_value=logValue)
	filePath = str(tmpdir)+'/mySession.file'

	comportLogger = ComportLogger.ComportLogger(comportHandler_stub, filePath)
	comportLogger.start()
	time.sleep(0.1)
	with open(filePath, 'r') as f:
		assert f.read().startswith(logValue.decode('utf-8'))

	comportLogger.stop()
	while comportLogger.is_alive():
		pass
