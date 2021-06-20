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

class _TelegramFrameParser:
	__TelegramStartId = 0xAA
	__TelegramEndId = 0xBB
	__ReplacementMarker = 0xCC

	@classmethod
	def splitIntoTelegrams(cls, stream: bytes):
		telegrams = []
		startNewTelegram = True
		for byte in stream:
			if startNewTelegram or byte == cls.__TelegramStartId:
				startNewTelegram = False
				telegrams.append({'raw': b''})
			telegrams[-1]['raw'] += bytes([byte])
			if byte == cls.__TelegramEndId:
				startNewTelegram = True
		return telegrams

	@staticmethod
	def __parse(telegrams):
		for telegram in telegrams:
			try:
				telegramNoStartAndEnd = _TelegramFrameParser.__parseStartAndEnd(telegram['raw'])
				telegramNoReplacementMarkers = _TelegramFrameParser.__parseReplacementMarkers(telegramNoStartAndEnd)
				telegram['valid'] = True
			except ValueError:
				telegram['valid'] = False

	@staticmethod
	def __parseStartAndEnd(telegramStream):
		if telegramStream[0] != _TelegramFrameParser.__TelegramStartId or telegramStream[-1] != _TelegramFrameParser.__TelegramEndId:
			raise ValueError('Parsing Start and End failed')
		return telegramStream[1:-1]

	@staticmethod
	def __parseReplacementMarkers(telegramStream):
		telegramStreamWithoutReplacementMarkers = b''
		offset = 0
		for byte in telegramStream:
			if byte == _TelegramFrameParser.__ReplacementMarker:
				offset += 1
			else:
				telegramStreamWithoutReplacementMarkers += bytes([byte + offset])
				offset = 0
		return telegramStreamWithoutReplacementMarkers

""" 	
	@classmethod
	def parseStream(cls, data: bytes):
		telegrams = cls.__splitIntoTelegrams(data)

		cls.__parse(telegrams)
		return telegrams
"""
