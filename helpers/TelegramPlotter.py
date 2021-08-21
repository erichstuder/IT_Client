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
	def __init__(self):
		plt.ion()
		plt.style.use('dark_background')
		self.__plotData = {}


	def plot(self, telegrams):
		name = telegrams[0]['valueName']
		if name not in self.__plotData:
			self.__plotData[name] = {}
		value = []
		timestamp = []
		for telegram in telegrams:
			if telegram['valueName'] != name:
				raise TelegramPlotterException('Telegrams must all have the same name.')
			if telegram['valid'] != True:
				raise TelegramPlotterException('Telegrams must all be valid.')
			value += [telegram['value']]
			timestamp += [telegram['timestamp']]
		self.__plotData[name]['value'] = value
		self.__plotData[name]['timestamp'] = timestamp


	def update(self):
		figure = plt.figure(num='myPlot', figsize=(8, 4))
		plt.clf()
		plt.grid(color='grey')
		for key in self.__plotData:
			value = self.__plotData[key]['value']
			timestamp = self.__plotData[key]['timestamp']
			plt.step(timestamp, value, where='post')
		figure.canvas.flush_events()

		# desiredValue_timeSeconds = [x/1e6 for x in desiredValue_time]
		# actualValue_timeSeconds = [x/1e6 for x in actualValue_time]

		# plt.legend(['desiredValue', 'actualValue'], loc='lower left')
		# plt.xlabel('time [s]')
