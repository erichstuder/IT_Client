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
from .TelegramContentParser import TelegramContentParserException


class TelegramReaderException(Exception):
	pass


class _TelegramReader:

	__TelegramStartId = b'\xAA'
	__TelegramEndId = b'\xBB'
	__ReplacementMarker = b'\xCC'


	def __init__(self, filePath):
		self.__filePath = filePath
		self.__fileSize = 0
		self.__startIndexOfLastTelegram = 0
		self.__telegrams = []


	def getTelegrams(self):
		fileSizeTemp = os.path.getsize(self.__filePath)
		if fileSizeTemp != self.__fileSize:
			self.__fileSize = fileSizeTemp
			newTelegrams = self.__getNewTelegrams()
			self.__parseTelegrams(newTelegrams)
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


	def __parseTelegrams(self, telegrams):
		for telegram in telegrams:
			try:
				content = self.__extractContent(telegram)
				contentNoTelegramType = _TelegramContentParser.parseTelegramType(telegram, content)
				if telegram['telegramType'] == 'value':
					contentNoValueName = _TelegramContentParser.parseValueName(telegram, contentNoTelegramType)
					contentNoValueType = _TelegramContentParser.parseValueType(telegram, contentNoValueName)
					contentNoValue = _TelegramContentParser.parseValue(telegram, contentNoValueType)
					_TelegramContentParser.parseTimestamp(telegram, contentNoValue)
				elif telegram['telegramType'] == 'string':
					_TelegramContentParser.parseString(telegram, contentNoTelegramType)
				else:
					raise ValueError('unknown telegram type')
				telegram["valid"] = True
			except (TelegramContentParserException, TelegramReaderException):
				telegram["valid"] = False


	def __extractContent(cls, telegram):
		telegramRaw = telegram['raw']
		if telegramRaw[0:1] != cls.__TelegramStartId:
			raise TelegramReaderException('Unexpected Start')
		if telegramRaw[-1:] != cls.__TelegramEndId:
			raise TelegramReaderException('Unexpected End')
		content = b''
		offset = 0
		for byte in telegramRaw[1:-1]:
			if byte == cls.__ReplacementMarker[0]:
				offset += 1
			else:
				content += bytes([byte + offset])
				offset = 0
		if offset != 0:
			raise TelegramReaderException('Unresolvable Replacement Marker')
		return content
