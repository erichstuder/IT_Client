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

import os
from .TelegramContentParser import _TelegramContentParser


class TelegramReaderException(Exception):
	pass


class _TelegramReader:

	#TODO: these should be only defined in one place
	__TelegramStartId = b'\xAA'
	__TelegramEndId = b'\xBB'

	
	def __init__(self, filePath):
		self.__filePath = filePath
		self.__fileSize = 0
		self.__startIndexOfLastTelegram = 0
		self.__telegrams = self.__getNewTelegrams()


	def getTelegrams(self):
		fileSizeTemp = os.path.getsize(self.__filePath)
		if fileSizeTemp != self.__fileSize:
			self.__fileSize = fileSizeTemp
			newTelegrams = self.__getNewTelegrams()
			_TelegramContentParser.parseTelegrams(newTelegrams)
			self.__telegrams += newTelegrams
		return self.__telegrams


	def __getNewTelegrams(self):
		startNewTelegram = True
		with open(self.__filePath, 'rb') as sessionFile:
			telegrams = []
			sessionFile.seek(self.__startIndexOfLastTelegram)
			while True:
				byte = sessionFile.read(1)
				if byte == b'':
					break
				if startNewTelegram or byte == self.__TelegramStartId:
					startNewTelegram = False
					telegrams.append({'raw': b''})
					self.__startIndexOfLastTelegram = sessionFile.tell() - 1
				telegrams[-1]['raw'] += byte
				if byte == self.__TelegramEndId:
					startNewTelegram = True
		return telegrams
