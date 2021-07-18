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

from threading import Thread
from threading import Event

class ComportLogger(Thread):
	def __init__(self, comportHandler, logFile):
		self.__comportHandler = comportHandler
		self.__logFile = logFile
		self.__stopEvent = Event()
		super().__init__(target=self.__logComport)
		self.daemon = True

	def __logComport(self):
		with open(self.__logFile, "a+b") as logFile:
			while not self.__stopEvent.is_set():
				data = self.__comportHandler.read()
				if data is not None:
					logFile.write(data)
					logFile.flush()

	def stop(self):
		self.__stopEvent.set()
