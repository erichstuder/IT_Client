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

import struct
from helpers.TelegramParser import TelegramParser

def test_parseStream_noStream():
	telegrams = TelegramParser.parseStream([])
	assert telegrams == []

def test_parseStream_invalidTelegram():
	invalidTelegram = [7, 3, 56, 2, 1, 33]
	telegrams = TelegramParser.parseStream(invalidTelegram)
	assert len(telegrams) == 1
	assert telegrams[0]['raw'] == bytes(invalidTelegram)
	assert telegrams[0]['valid'] == False

def test_parseStream_valueTelegram():
	telegramTypeId = 1
	valueName = 'myValue'
	valueTypeId = 2
	value = 198
	timestamp = [0x56, 0x78, 0x90, 0x22]
	stream = [0xAA, telegramTypeId] + [ord(c) for c in valueName] + [0, valueTypeId, value] + timestamp + [0xBB]
	telegrams = TelegramParser.parseStream(stream)
	assert len(telegrams) == 1
	telegram = telegrams[0]
	assert telegram['telegramType'] == 'value'
	assert telegram['valueName'] == valueName
	assert telegram['valueType'] == 'uint8'
	assert telegram['value'] == value
	assert telegram['timestamp'] == 0x22907856
	assert telegram['valid'] == True

def test_parseStream_stringTelegram():
	telegramTypeId = 2
	value = 'thisIsMyStringValue'
	stream = [0xAA, telegramTypeId] + [ord(c) for c in value] + [0] + [0xBB]
	telegrams = TelegramParser.parseStream(stream)
	assert len(telegrams) == 1
	telegram = telegrams[0]
	assert telegram['telegramType'] == 'string'
	assert telegram['value'] == value
	assert telegram['valid'] == True
