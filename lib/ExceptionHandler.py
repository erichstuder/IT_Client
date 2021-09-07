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

from lib.ComportHandler import ComportHandlerException
from lib.ComportHandler import UnsupportedConnectionType

class ExceptionHandler(Thread):	
	def __init__(self, exceptionQueue: Queue):
		self.__exceptionQueue = exceptionQueue
		super().__init__(target=self.__exceptionHandler)
		self.daemon = True

	def __exceptionHandler(self):
		while True:
			exception = self.__exceptionQueue.get(block=True)
			assert isinstance(exception, Exception)
			if isinstance(exception, ComportHandlerException):
				if isinstance(exception, UnsupportedConnectionType):
					print('Error: ' + UnsupportedConnectionType.__name__)
					print('The comport connection type is unsupported: ' + str(exception))
					print('Possible causes:')
					print(' 1. Connection type not set.')
					print(' 2. Connection type set to an invalid value.')
					print()
			else:
				raise exception
