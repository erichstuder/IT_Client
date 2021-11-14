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

from multiprocessing import Process, Queue

class TelegramPlotterException(Exception):
	pass


class TelegramPlotter:
	def __init__(self, title):
		self.__plotTitle = title
		self.__plotData = {}
		self.__id = 0
		self.__queue = Queue(maxsize=1)
		plotterProcess = Process(target=self.__plotterProcess, daemon=True)
		plotterProcess.start()


	def __plotterProcess(self):

		# This import prevents a startup delay and an error message
		# The hint came from here: https://github.com/matplotlib/matplotlib/issues/21627
		# Not sure why this works
		import matplotlib.pyplot as plt

		plt.style.use('dark_background')
		numberOfPlots_old = -1
		while True:
			if not self.__queue.empty():
				plotData = self.__queue.get()
				plotNumber = 0
				legendString = []
				numberOfPlots = len(plotData)
				if numberOfPlots < 1:
					continue
				if numberOfPlots != numberOfPlots_old:
					figure, axes = plt.subplots(numberOfPlots, 1, sharex=True, figsize=(12, 6))
					figure.suptitle(self.__plotTitle)
					numberOfPlots_old = numberOfPlots
				for key in plotData:
					axis = axes[plotNumber]
					axis.clear()
					axis.ticklabel_format(useOffset=False)
					axis.grid(color='grey')
					value = plotData[key]['value']
					timestamp = plotData[key]['timestamp']
					axis.step(timestamp, value, where='post')
					legendString = plotData[key]['name']
					axis.legend([legendString], loc='lower left')
					plotNumber += 1
				plt.show(block=False)
			plt.pause(0.001)


	def plot(self, telegrams):
		if len(telegrams) < 1:
			return
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
		self.__plotData[self.__id]['name'] = name
		self.__id += 1


	def update(self):
		self.__queue.put(self.__plotData)
		self.__plotData = {}
		self.__id = 0
