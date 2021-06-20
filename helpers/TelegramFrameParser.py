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

class TelegramFrameParserException(Exception):
	pass

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

	@classmethod
	def extractContent(cls, telegram):
		if telegram[0] != cls.__TelegramStartId:
			raise TelegramFrameParserException('Unexpected Start')
		if telegram[-1] != cls.__TelegramEndId:
			raise TelegramFrameParserException('Unexpected End')
		content = b''
		offset = 0
		for byte in telegram[1:-1]:
			if byte == cls.__ReplacementMarker:
				offset += 1
			else:
				content += bytes([byte + offset])
				offset = 0
		if offset != 0:
			raise TelegramFrameParserException('Unresolvable Replacement Marker')
		return content
