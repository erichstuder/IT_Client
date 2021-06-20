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

class TelegramContentParserException(Exception):
	pass

class _TelegramContentParser:

	@staticmethod
	def parseTelegramType(telegram, telegramStream):
		telegramTypes = {
			1: 'value',
			2: 'string',
		}
		if len(telegramStream) < 1:
			raise TelegramContentParserException('stream is empty')
		telegramType = telegramTypes.get(telegramStream[0])
		if telegramType == None:
			raise TelegramContentParserException('invalid telegram type')
		telegram['telegramType'] = telegramType
		newTelegramStream = telegramStream[1:]
		return newTelegramStream

	@classmethod
	def parseValueName(cls, telegram, telegramStream):
		name, newTelegramStream = cls.__parseString(telegramStream)
		telegram['valueName'] = name
		return newTelegramStream

	@staticmethod
	def parseValueType(telegram, telegramStream):
		valueTypes = {
			1: 'int8',
			2: 'uint8',
			3: 'ulong',
			4: 'float',
		}
		if len(telegramStream) == 0:
			raise TelegramContentParserException('no value to parse')
		valueType = valueTypes.get(telegramStream[0])
		if valueType == None:
			raise TelegramContentParserException('invalid value type')
		telegram['valueType'] = valueType
		return telegramStream[1:]

	@staticmethod
	def parseValue(telegram, telegramStream):
		if telegram['valueType'] == 'uint8':
			size = 1
			if len(telegramStream) < size:
				raise ValueError('not enough bytes to parse uint8')
			telegram['value'] = struct.unpack('B', bytes(telegramStream[:size]))[0]
		elif telegram['valueType'] == 'ulong':
			size = 4
			if len(telegramStream) < size:
				raise ValueError('not enough bytes to parse ulong')
			telegram['value'] = struct.unpack('L', bytes(telegramStream[:size]))[0]
		elif telegram['valueType'] == 'float':
			size = 4
			if len(telegramStream) < size:
				raise ValueError('not enough bytes to parse float')
			telegram['value'] = struct.unpack('f', bytes(telegramStream[:size]))[0]
		return telegramStream[size:]

	@staticmethod
	def parseTimestamp(telegram, telegramStream):
		size = 4
		if len(telegramStream) < size:
			raise ValueError('not enough bytes to parse timestamp')
		telegram['timestamp'] = struct.unpack('L', bytes(telegramStream[:size]))[0]
		return telegramStream[size:]

	@classmethod
	def parseString(cls, telegram, telegramStream):
		name, newTelegramStream = cls.__parseString(telegramStream)
		telegram['value'] = name
		return newTelegramStream


	@staticmethod
	def __parseString(telegramStream):
		string = ''
		stringLength = 0
		for byte in telegramStream:
			if byte == 0:
				if len(string) < 2:
					raise TelegramContentParserException('string is empty')
				return string, telegramStream[stringLength+1:]
			string += chr(byte)
			stringLength += 1
		raise TelegramContentParserException('string has no terminator')
