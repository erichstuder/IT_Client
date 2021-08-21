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

from .TelegramFrameParser import _TelegramFrameParser
from .TelegramFrameParser import TelegramFrameParserException
from .TelegramContentParser import _TelegramContentParser
from .TelegramContentParser import TelegramContentParserException

class TelegramParser:
	def __init__(self, sessionFilePath):
		self.__sessionFilePath = sessionFilePath
		telegramFrameParser = _TelegramFrameParser(sessionFilePath)
		self.telegrams = telegramFrameParser.splitIntoTelegrams()
		for telegram in self.telegrams:
			TelegramParser.__parse(telegram)
		print(self.telegrams)


	def getLastValueByName(self, name):
		for telegram in reversed(self.telegrams):
			if telegram['valid'] == True and telegram['telegramType'] == 'value' and telegram['valueName'] == name:
				return telegram
		return None


	@staticmethod
	def parseLastValidTypeValueTelegram(data: bytes, valueName):
		lastDataIndex = len(data)-1
		endIndex = lastDataIndex
		for index in range(lastDataIndex, 0, -1):
			byte = data[index]
			if byte == TelegramParser.__TelegramEndId:
				endIndex = index
			elif byte == TelegramParser.__TelegramStartId:
				startIndex = index
				telegrams = TelegramParser.__splitTelegramStream(data[startIndex:endIndex+1])
				TelegramParser.__parse(telegrams)
				telegram = telegrams[0]
				if telegram["valid"] == True and telegram["telegramType"] == "value" and telegram["valueName"] == valueName:
					return telegram
		return None


	@staticmethod
	def getTypeValueTelegramsAfterTimestamp(data: bytes, valueName, lowestTimestamp):
		telegrams = []
		lastDataIndex = len(data)-1
		endIndex = lastDataIndex
		for index in range(lastDataIndex, 0, -1):
			byte = data[index]
			if byte == TelegramParser.__TelegramEndId:
				endIndex = index
			elif byte == TelegramParser.__TelegramStartId:
				startIndex = index
				telegramsTemp = TelegramParser.__splitTelegramStream(data[startIndex:endIndex+1])
				TelegramParser.__parse(telegramsTemp)
				telegram = telegramsTemp[0]
				if telegram["valid"] and telegram["telegramType"] == "value":
					if telegram["timestamp"] <= lowestTimestamp:
						break
					elif telegram["valueName"] == valueName:
						telegrams.insert(0, telegram)
		return telegrams


	@classmethod
	def parseStream(cls, data: bytes):
		telegrams = _TelegramFrameParser.splitIntoTelegrams(data)
		for telegram in telegrams:
			cls.__parse(telegram)
		return telegrams


	@staticmethod
	def __parse(telegram):
		try:
			contentStream = _TelegramFrameParser.extractContent(telegram['raw'])
			streamNoTelegramType = _TelegramContentParser.parseTelegramType(telegram, contentStream)
			if telegram['telegramType'] == 'value':
				streamNoValueName = _TelegramContentParser.parseValueName(telegram, streamNoTelegramType)
				streamNoValueType = _TelegramContentParser.parseValueType(telegram, streamNoValueName)
				streamNoValue = _TelegramContentParser.parseValue(telegram, streamNoValueType)
				_TelegramContentParser.parseTimestamp(telegram, streamNoValue)
			elif telegram['telegramType'] == 'string':
				_TelegramContentParser.parseString(telegram, streamNoTelegramType)
			else:
				raise ValueError('unknown telegram type')
			telegram["valid"] = True
		except TelegramFrameParserException or TelegramContentParserException as e:
			telegram["valid"] = False
