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

import matplotlib.pyplot as plt

class TelegramPlotterException(Exception):
	pass


class TelegramPlotter:
	def __init__(self, title):
		self.__plotTitle = title
		plt.ion()
		plt.style.use('dark_background')
		self.__plotData = {}
		self.__id = 0
		self.__plotNumber = 1


	def plot(self, *telegramsList):
		for telegrams in telegramsList:
			name = telegrams[0]['valueName']
			if name not in self.__plotData:
				self.__plotData[self.__id] = {}
			value = []
			timestamp = []
			for telegram in telegrams:
				if telegram['valueName'] != name:
					raise TelegramPlotterException('Telegrams must all have the same name.')
				if telegram['valid'] != True:
					raise TelegramPlotterException('Telegrams must all be valid.')
				value += [telegram['value']]
				timestamp += [telegram['timestamp']]
			self.__plotData[self.__id]['value'] = value
			self.__plotData[self.__id]['timestamp'] = timestamp
			self.__plotData[self.__id]['plotNumber'] = self.__plotNumber
			self.__plotData[self.__id]['name'] = name
			self.__id += 1
		self.__plotNumber += 1


	def update(self):
		figure = plt.figure(num=self.__plotTitle, figsize=(8, 4))
		plt.clf()
		plotNumber = 0
		legendStrings = []
		for key in self.__plotData:
			value = self.__plotData[key]['value']
			timestamp = self.__plotData[key]['timestamp']
			if plotNumber != self.__plotData[key]['plotNumber']:
				plotNumber = self.__plotData[key]['plotNumber']
				plt.subplot(self.__plotNumber-1, 1, plotNumber)
				plt.ticklabel_format(useOffset=False)
				legendStrings = []
			plt.grid(color='grey')
			plt.step(timestamp, value, where='post')
			legendStrings.append(self.__plotData[key]['name'])
			plt.legend(legendStrings, loc='lower left')
		figure.canvas.flush_events()
		self.__plotData = {}
		self.__id = 0
		self.__plotNumber = 1
