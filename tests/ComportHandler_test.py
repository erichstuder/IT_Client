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
import helpers.ComportHandler
from helpers.ComportHandler import ComportHandler
from helpers.ComportHandler import ComportHandlerException

@pytest.fixture
def serialMocking(mocker):
	mocker.patch.object(helpers.ComportHandler.serial.Serial, 'setPort')
	mocker.patch.object(helpers.ComportHandler.serial.Serial, 'open')


def test_init():
	h = ComportHandler()
	assert h.connectionType == None
	assert h.vid == None
	assert h.pid == None
	assert h.port == None


def test_open_USB_RS232(serialMocking, mocker):
	port = 'COM1'
	mocker.patch.object(helpers.ComportHandler._ComportAccess, 'findPortByVidAndPid', return_value=port)
	mocker.patch.object(helpers.ComportHandler.serial.Serial, 'isOpen', return_value=True)

	vid = 3245
	pid = 963
	h = ComportHandler()
	h.connectionType = "USB_RS232"
	h.pid = pid
	h.vid = vid
	h.open()

	helpers.ComportHandler._ComportAccess.findPortByVidAndPid.assert_called_once_with(vid=vid, pid=pid)
	helpers.ComportHandler.serial.Serial.setPort.assert_called_once_with(port)
	helpers.ComportHandler.serial.Serial.open.assert_called_once()
	helpers.ComportHandler.serial.Serial.isOpen.assert_called_once()
	

def test_open_RS232(serialMocking, mocker):
	mocker.patch.object(helpers.ComportHandler.serial.Serial, 'isOpen', return_value=True)

	port = "myPort"
	h = ComportHandler()
	h.connectionType = "RS232"
	h.port = port
	h.open()

	helpers.ComportHandler.serial.Serial.setPort.assert_called_once_with(port)
	helpers.ComportHandler.serial.Serial.open.assert_called_once()
	helpers.ComportHandler.serial.Serial.isOpen.assert_called_once()


def test_open_unsupportedConnectionType():
	h = ComportHandler()
	myConnectionType = "myConnectionType"
	h.connectionType = myConnectionType
	with pytest.raises(ComportHandlerException, match="^unsupported connectionType: " + myConnectionType + "$"):
		h.open()


def test_open_portWontOpen(serialMocking, mocker):
	mocker.patch.object(helpers.ComportHandler.serial.Serial, 'isOpen', return_value=False)

	h = ComportHandler()
	h.connectionType = "RS232"
	h.port = "myPort"
	startTime = time.time()
	with pytest.raises(ComportHandlerException, match="^comport open timeout$"):
		h.open()

	assert 2.9 <= time.time()-startTime < 3.5
