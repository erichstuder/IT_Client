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

import serial  # install pyserial to gain access
import sys
#import winreg
import logging
import time
from lib.ComportAccess import _ComportAccess

class ComportHandlerException(Exception):
	pass

class ComportHandler:
	def __init__(self):
		self.__serialPort = serial.Serial(None)
		self.__serialPort.timeout = 0
		self.connectionType = None
		self.vid = None
		self.pid = None
		self.port = None


	def open(self):
		if self.connectionType == "USB_RS232":
			self.__serialPort.setPort(_ComportAccess.findPortByVidAndPid(vid=self.vid, pid=self.pid))
		elif self.connectionType == "RS232":
			self.__serialPort.setPort(self.port)
		else:
			raise ComportHandlerException("unsupported connectionType: " + str(self.connectionType))
	
		self.__serialPort.open()
		timeout = time.time() + 3
		while True:
			if self.__serialPort.isOpen():
				break
			if time.time() > timeout:
				raise ComportHandlerException("comport open timeout")


	def write(self, data):
		if not self.__serialPort.isOpen():
			self.open()
		self.__serialPort.write(data.encode())


	def read(self):
		if not self.__serialPort.isOpen():
			self.open()
		value = self.__serialPort.read(self.__serialPort.inWaiting())
		if value == b"":
			return None
		else:
			return value

