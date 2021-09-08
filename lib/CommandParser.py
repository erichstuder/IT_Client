'''
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
'''

import time
import os
import threading
from threading import Thread
from queue import Queue

class CommandParserException(Exception):
	pass

class CommandParser(Thread):
	def __init__(self, comportHandler, commandQueue: Queue, exceptionQueue: Queue):
		self.__comPortHandler = comportHandler
		self.__commandQueue = commandQueue
		self.__exceptionQueue = exceptionQueue
		super().__init__(target=self.__commandParser)
		self.daemon = True
		self.__isRunning = True

	def __commandParser(self):
		while self.__isRunning:
			try:
				cmd = self.__commandQueue.get(block=True)
				self.__parse(cmd)
			except Exception as e:
				self.__exceptionQueue.put(e)

	def __parse(self, data):
		if data.startswith('set connectionType '):
			connectionType = data.split(' ')[2]
			self.__comPortHandler.connectionType = connectionType
			print('connectionType set to: ' + connectionType + '\n')
		elif data.startswith('set VID '):
			vid = data.split(' ')[2]
			self.__comPortHandler.vid = vid
			print('VID set to: ' + vid + '\n')
		elif data.startswith('set PID '):
			pid = data.split(' ')[2]
			self.__comPortHandler.pid = pid
			print('PID set to: ' + pid + '\n')
		elif data.startswith('set comport '):
			comPort = data.split(' ')[2]
			self.__comPortHandler.port = comPort
			print('comport set to: ' + comPort + '\n')
		elif data.startswith('run '):
			scriptFileName = data.split(' ')[1]

			if not os.path.isfile(scriptFileName):
				raise CommandParserException('error: file not found')

			with open(scriptFileName, 'r') as scriptFile:
				if not scriptFileName.endswith('.py'):
					raise CommandParserException('unsupported file extension')
				t = threading.Thread(target=lambda: exec(scriptFile.read(), {'send': self.__commandQueue.put}) )
				t.daemon = True
				t.start()
								
		elif data == 'exit':
			print('goodbye...')
			time.sleep(0.5)
			self.__isRunning = False
		else:
			self.__comPortHandler.write(data + '\r')
