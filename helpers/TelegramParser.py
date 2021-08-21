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

from .TelegramReader import _TelegramReader

class TelegramParser:
	def __init__(self, sessionFilePath):
		self.__telegramReader = _TelegramReader(sessionFilePath)


	def getValues(self, name):
		telegrams = []
		for telegram in self.__telegramReader.getTelegrams():
			if telegram['valid'] == True and telegram['telegramType'] == 'value' and telegram['valueName'] == name:
				telegrams += [telegram]
		return telegrams


	def getLastValue(self, name):
		for telegram in reversed(self.__telegramReader.getTelegrams()):
			if telegram['valid'] == True and telegram['telegramType'] == 'value' and telegram['valueName'] == name:
				return telegram
		return None


	def getLastValues(self, name, timestampRange):
		telegrams = []
		lastTelegram = self.getLastValue(name)
		if lastTelegram is None:
			return None
		lastTimestamp = lastTelegram['timestamp']
		for telegram in reversed(self.__telegramReader.getTelegrams()):
			if telegram['valid'] == True:
				if telegram['timestamp'] < lastTimestamp - timestampRange:
					return telegrams
				if telegram['telegramType'] == 'value' and telegram['valueName'] == name:
					telegrams += [telegram]
		return reversed(telegrams)
