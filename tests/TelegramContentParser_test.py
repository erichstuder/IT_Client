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

import pytest
from helpers.TelegramContentParser import _TelegramContentParser
from helpers.TelegramContentParser import TelegramContentParserException

def test_parseTelegramType_emptyStream():
	with pytest.raises(TelegramContentParserException, match='stream is empty'):
		_TelegramContentParser.parseTelegramType(None, [])

@pytest.mark.parametrize('telegramType', [(0x00), (0x03)])
def test_parseTelegramType_invalidType(telegramType):
	with pytest.raises(TelegramContentParserException, match='invalid telegram type'):
		_TelegramContentParser.parseTelegramType(None, [telegramType])

@pytest.mark.parametrize('telegramType, telegramTypeString',
			 [(0x01,       'value'),
			  (0x02,       'string'),
			 ])
def test_parseTelegramType(telegramType, telegramTypeString): 	
	rest = 0x42
	telegram = {}
	newStream = _TelegramContentParser.parseTelegramType(telegram, [telegramType, rest])
	assert newStream == [rest]
	assert telegram['telegramType'] == telegramTypeString

def test_parseValueName_emptyStream():
	with pytest.raises(TelegramContentParserException, match='string has no terminator'):
		_TelegramContentParser.parseValueName(None, [])

def test_parseValueName_emptyString():
	with pytest.raises(TelegramContentParserException, match='string is empty'):
		_TelegramContentParser.parseValueName({}, [0x00])

def test_parseValueName():
	telegram = {}
	stream = [ord(c) for c in 'Hello'] + [0x00, 11, 22, 33]
	newStream = _TelegramContentParser.parseValueName(telegram, stream)
	assert telegram['valueName'] == 'Hello'
	assert newStream == [11, 22, 33]

def test_parseValueType_emptyStream():
	with pytest.raises(TelegramContentParserException, match='no value to parse'):
		_TelegramContentParser.parseValueType(None, [])

@pytest.mark.parametrize('valueType', [(0x00), (0x05)])
def test_parseValueType_invalidType(valueType):
	with pytest.raises(TelegramContentParserException, match='invalid value type'):
		_TelegramContentParser.parseValueType(None, [valueType])

@pytest.mark.parametrize('valueType, valueTypeString',
			 [(0x01,    'int8'),
			  (0x02,    'uint8'),
			  (0x03,    'ulong'),
			  (0x04,    'float'),
			 ])
def test_parseValueType(valueType, valueTypeString):
	telegram = {}
	newStream = _TelegramContentParser.parseValueType(telegram, [valueType])
	assert telegram['valueType'] == valueTypeString
	assert newStream == []

def test_parseValue_noTelegram():
	with pytest.raises(TelegramContentParserException, match='telegram is None'):
		_TelegramContentParser.parseValue(None, [])

def test_parseValue_noKey():
	with pytest.raises(TelegramContentParserException, match='telegram has no key \'valueType\''):
		_TelegramContentParser.parseValue({}, [])

def test_parseValue_unimplementedValueType():
	with pytest.raises(TelegramContentParserException, match='parsing for value type \'None\' not implemented'):
		_TelegramContentParser.parseValue({'valueType': None}, [])

@pytest.mark.parametrize('valueTypeString', [('int8'), ('uint8'), ('ulong'), ('float')])
def test_parseValue_noStream(valueTypeString):
	with pytest.raises(TelegramContentParserException, match='not enough bytes to parse ' + valueTypeString):
		_TelegramContentParser.parseValue({'valueType': valueTypeString}, [])

@pytest.mark.parametrize('valueTypeString, data, result',
			 [('int8',         [0xFE], -2),
			  ('int8',         [0x55], 0x55),
			  ('uint8',        [0x00], 0),
			  ('uint8',        [0xAB], 0xAB),
			  ('ulong',        [0x12, 0x34, 0x56, 0x78], 0x78563412),
			  ('ulong',        [0xEE, 0xEE, 0xEE, 0xEE], 0xEEEEEEEE),
			  ('float',        [0x00, 0x00, 0x00, 0x00], 0),
			  ('float',        [0x22, 0x44, 0x66, 0x88], -6.929319711261567e-34),
			 ])
def test_parseValue(valueTypeString, data, result):
	telegram = {'valueType': valueTypeString}
	newStream = _TelegramContentParser().parseValue(telegram, data)
	assert telegram['value'] == result

def test_parseTimestamp_noStream():
	with pytest.raises(TelegramContentParserException, match='not enough bytes to parse ulong'):
		_TelegramContentParser().parseTimestamp({}, [])

def test_parseTimestamp_noTelegram():
	with pytest.raises(TelegramContentParserException, match='telegram is None'):
		_TelegramContentParser().parseTimestamp(None, [5, 6, 7, 8])

def test_parseTimestamp_noTelegram():
	telegram = {}
	newStream = _TelegramContentParser().parseTimestamp(telegram, [5, 6, 7, 8])
	assert telegram['timestamp'] == 0x08070605
	assert newStream == []
