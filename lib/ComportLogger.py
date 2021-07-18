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

class ComportLogger:
	def __init__(self, comportHandler, logFile):
		self.__comportHandler = comportHandler
		self.__logFile = logFile

	def run(self):
		self.__running = True
		self.__runComportLogging()

	def __runComportLogging(self):
		with open(self.__logFile, "a+b") as logFile:
			while self.__running:
				data = self.__comportHandler.read()
				if data is not None:
					logFile.write(data)
					logFile.flush()

	def stop(self):
		self.__running = False
