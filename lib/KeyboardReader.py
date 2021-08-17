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
from queue import Queue

class KeyboardReader(Thread):	
	def __init__(self, queue: Queue):
		self.__queue = queue
		super().__init__(target=self.__keyboardReader)
		self.daemon = True

	def __keyboardReader(self):
		while True:
			self.__queue.put(input().strip())
