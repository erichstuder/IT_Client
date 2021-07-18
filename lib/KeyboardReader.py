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

import threading

class KeyboardReader:	
	def __init__(self, parser):
		self.__keyboardInputParser = parser
		self.__keyboardReaderThread = threading.Thread(target=self.__keyboardReader)
		self.__keyboardReaderThread.daemon = True

	def __keyboardReader(self):
		while self.__running:
			self.__keyboardInputParser(input().strip())

	def start(self):
		self.__running = True
		self.__keyboardReaderThread.start()

	def stop(self):
		self.__running = False
