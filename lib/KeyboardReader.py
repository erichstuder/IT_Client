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

class KeyboardReader(Thread):	
	def __init__(self, parser):
		self.__keyboardInputParser = parser.parse
		super().__init__(target=self.__keyboardReader)
		self.daemon = True
		self.__stopEvent = Event()

	def __keyboardReader(self):
		while not self.__stopEvent.is_set():
			self.__keyboardInputParser(input().strip())

	def stop(self):
		self.__stopEvent.set()
