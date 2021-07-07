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

import lib.ComportAccess
from lib.ComportAccess import _ComportAccess
from lib.ComportAccess import ComportAccessException

class Device:
	def __init__(self, pid=None, port=None):
		self.__pid = pid
		self.device_node = port

	def get(self, value):
		if value == 'ID_MODEL_ID':
			return self.__pid
		else:
			raise Exception('unexpected value: ' + value)


def test_findPortByVidAndPid_listDevices(mocker):
	mocker.patch.object(lib.ComportAccess.pyudev.Context, 'list_devices', return_value=[])

	vid = 42
	with pytest.raises(ComportAccessException):
		_ComportAccess.findPortByVidAndPid(vid=vid, pid=None)

	lib.ComportAccess.pyudev.Context.list_devices.assert_called_once_with(subsystem='tty', ID_VENDOR_ID=vid)


def test_findPortByVidAndPid_noDeviceFound(mocker):
	mocker.patch.object(lib.ComportAccess.pyudev.Context, 'list_devices', return_value=[])

	with pytest.raises(ComportAccessException, match="^no device found$"):
		_ComportAccess.findPortByVidAndPid(vid=5643, pid=None)


def test_findPortByVidAndPid_tooManyDevices(mocker):
	pid = 632545
	device = Device(pid=pid)
	mocker.patch.object(lib.ComportAccess.pyudev.Context, 'list_devices', return_value=[device, device])

	with pytest.raises(ComportAccessException, match="^more than one device found$"):
		_ComportAccess.findPortByVidAndPid(vid=None, pid=pid)


def test_findPortByVidAndPid(mocker):
	pid = 632545
	port = 'COM5632'
	mocker.patch.object(lib.ComportAccess.pyudev.Context, 'list_devices', return_value=[Device(pid=pid, port=port)])

	assert _ComportAccess.findPortByVidAndPid(vid=None, pid=pid) == port
