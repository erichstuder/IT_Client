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
import threading
import lib.ComportLogger as ComportLogger

def test_comportLogger(mocker, tmpdir):
	comportHandler_stub = mocker.stub()
	logValue = b'abc'
	mocker.patch.object(comportHandler_stub, 'read', create=True, return_value=logValue)
	filePath = str(tmpdir)+'/mySession.file'
	comportLogger = ComportLogger.ComportLogger(comportHandler_stub, filePath)
	t = threading.Thread(target=comportLogger.run)
	t.daemon = True
	t.start()
	time.sleep(0.1)
	comportLogger.stop()

	with open(filePath, 'r') as f:
		assert f.read().startswith(logValue.decode('utf-8'))
