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

from helpers.TelegramFrameParser import _TelegramFrameParser

__TelegramStartId = 0xAA
__TelegramEndId = 0xBB
__ReplacementMarker = 0xCC

def test_splitEmptyStream():
	telegrams = _TelegramFrameParser.splitIntoTelegrams([])
	assert telegrams == []

""" def test_parseEmptyTelegram():
	telegrams = _TelegramFrameParser.parseFrame([])
	assert telegrams == []

def test_parseTelegramWithOnlyStart():
	resultingTelegram = {'raw': b'\xaa', 'valid': False}

	telegrams = _TelegramFrameParser.parseFrame([__TelegramStartId])
	assert telegrams == [resultingTelegram]

	telegrams = _TelegramFrameParser.parseFrame([__TelegramStartId, __TelegramStartId])
	assert telegrams == [resultingTelegram, resultingTelegram]

	telegrams = _TelegramFrameParser.parseFrame([__TelegramStartId, __TelegramStartId, __TelegramStartId])
	assert telegrams == [resultingTelegram, resultingTelegram, resultingTelegram]

def test_parseTelegramWithOnlyEnd():
	resultingTelegram = {'raw': b'\xbb', 'valid': False}

	telegrams = _TelegramFrameParser.parseFrame([__TelegramEndId])
	assert telegrams == [resultingTelegram]

	telegrams = _TelegramFrameParser.parseFrame([__TelegramEndId, __TelegramEndId])
	assert telegrams == [resultingTelegram, resultingTelegram]

	telegrams = _TelegramFrameParser.parseFrame([__TelegramEndId, __TelegramEndId, __TelegramEndId])
	assert telegrams == [resultingTelegram, resultingTelegram, resultingTelegram]

def test_parseTelegramWithOnlyStartAndEnd():
	telegrams = _TelegramFrameParser.parseFrame([__TelegramStartId, __TelegramEndId])
	assert telegrams == [{'raw': b'\xaa\xbb', 'valid': False}]

	telegrams = _TelegramFrameParser.parseFrame([__TelegramStartId, __TelegramEndId, __TelegramStartId])
	assert telegrams == [{'raw': b'\xaa\xbb', 'valid': False}, {'raw': b'\xaa', 'valid': False}]

	telegrams = _TelegramFrameParser.parseFrame([__TelegramStartId, __TelegramEndId, __TelegramEndId])
	assert telegrams == [{'raw': b'\xaa\xbb', 'valid': False}, {'raw': b'\xbb', 'valid': False}] """
