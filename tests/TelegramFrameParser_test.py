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

def test_splitEmptyStream():
	telegrams = _TelegramFrameParser.splitIntoTelegrams([])
	assert telegrams == []

def test_splitEmptyTelegram():
	data = [0xAA, 0xBB]
	telegrams = _TelegramFrameParser.splitIntoTelegrams(data)
	assert len(telegrams) == 1
	assert telegrams[0]['raw'] == bytes(data)

def test_splitTelegrams():
	telegram1 = [0xAA, 1, 2, 3, 0xBB]
	telegram2 = [0xAA, 9, 8, 7, 6, 0xBB]
	telegrams = _TelegramFrameParser.splitIntoTelegrams(telegram1 + telegram2)
	assert len(telegrams) == 2
	assert telegrams[0]['raw'] == bytes(telegram1)
	assert telegrams[1]['raw'] == bytes(telegram2)

def test_splitStreamWithNoStart():
	invalidStart = [1, 2, 3, 0xBB]
	telegram = [0xAA, 9, 8, 7, 6, 0xBB]
	telegrams = _TelegramFrameParser.splitIntoTelegrams(invalidStart + telegram)
	assert len(telegrams) == 2
	assert telegrams[0]['raw'] == bytes(invalidStart)
	assert telegrams[1]['raw'] == bytes(telegram)

def test_splitTelegramWithNoStart():
	telegram1 = [0xAA, 9, 8, 7, 6, 0xBB]
	invalidStart = [1, 2, 3, 0xBB]
	telegram2 = [0xAA, 22, 0xBB]
	telegrams = _TelegramFrameParser.splitIntoTelegrams(telegram1 + invalidStart + telegram2)
	assert len(telegrams) == 3
	assert telegrams[0]['raw'] == bytes(telegram1)
	assert telegrams[1]['raw'] == bytes(invalidStart)
	assert telegrams[2]['raw'] == bytes(telegram2)

def test_splitStreamWithNoEnd():
	telegram = [0xAA, 9, 8, 7, 6, 0xBB]
	invalidEnd = [0xAA, 1, 2, 3]
	telegrams = _TelegramFrameParser.splitIntoTelegrams(telegram + invalidEnd)
	assert len(telegrams) == 2
	assert telegrams[0]['raw'] == bytes(telegram)
	assert telegrams[1]['raw'] == bytes(invalidEnd)

def test_splitTelegramWithNoEnd():
	telegram1 = [0xAA, 9, 8, 7, 6, 0xBB]
	invalidEnd = [0xAA, 1, 2, 3]
	telegram2 = [0xAA, 22, 0xBB]
	telegrams = _TelegramFrameParser.splitIntoTelegrams(telegram1 + invalidEnd + telegram2)
	assert len(telegrams) == 3
	assert telegrams[0]['raw'] == bytes(telegram1)
	assert telegrams[1]['raw'] == bytes(invalidEnd)
	assert telegrams[2]['raw'] == bytes(telegram2)

def test_splitTelegramWithNoEndAndEmpty():
	telegram1 = [0xAA, 9, 8, 7, 6, 0xBB]
	onlyStart = [0xAA]
	telegram2 = [0xAA, 22, 0xBB]
	telegrams = _TelegramFrameParser.splitIntoTelegrams(telegram1 + onlyStart + telegram2)
	assert len(telegrams) == 3
	assert telegrams[0]['raw'] == bytes(telegram1)
	assert telegrams[1]['raw'] == bytes(onlyStart)
	assert telegrams[2]['raw'] == bytes(telegram2)

def test_splitStreamWithInvalidStart():
	invalidStart = [0x12, 0x34, 0x56]
	telegram = [0xAA, 22, 0xBB]
	telegrams = _TelegramFrameParser.splitIntoTelegrams(invalidStart + telegram)
	assert len(telegrams) == 2
	assert telegrams[0]['raw'] == bytes(invalidStart)
	assert telegrams[1]['raw'] == bytes(telegram)

def test_splitStreamWithInvalidEnd():
	telegram = [0xAA, 22, 0xBB]
	invalidEnd = [0x78, 0x9A, 0xBC, 0xCC]
	telegrams = _TelegramFrameParser.splitIntoTelegrams(invalidEnd + telegram)
	assert len(telegrams) == 2
	assert telegrams[1]['raw'] == bytes(telegram)
	assert telegrams[0]['raw'] == bytes(invalidEnd)
