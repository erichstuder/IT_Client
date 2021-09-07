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

from lib.CommandParser import CommandParser
from lib.ComportHandler import ComportHandler
from lib.KeyboardReader import KeyboardReader
from lib.ComportLogger import ComportLogger
from lib.ExceptionHandler import ExceptionHandler
import sys
import os
from queue import Queue

class Client:
	@classmethod
	def start(cls):
		cls._setupWindow()
		print("client started")

		args = cls._parseArguments()
		initFile = args['initFile']
		sessionFile = args['sessionFile']

		commandQueue = Queue()
		exceptionQueue = Queue()

		KeyboardReader(commandQueue).start()

		if initFile != None:
			commandQueue.put("run " + initFile)

		comportHandler = ComportHandler()
		ComportLogger(comportHandler, sessionFile).start()

		ExceptionHandler(exceptionQueue).start()

		commandParser = CommandParser(comportHandler=comportHandler, commandQueue=commandQueue, exceptionQueue=exceptionQueue)
		commandParser.start()
		commandParser.join()

	@staticmethod
	def _setupWindow():
		if sys.platform.startswith('win'):
			os.system('mode 70,15')
			os.system('title IT client')

	@staticmethod
	def _parseArguments():
		initFile = None
		sessionFile = "mySession.session"
		for n in range(2, len(sys.argv), 2):
			argName = str(sys.argv[n-1])
			argValue = str(sys.argv[n])
			if argName == "-initFile":
				initFile = argValue
			elif argName == "-sessionFile":
				sessionFile = argValue
		return {'initFile': initFile, 'sessionFile': sessionFile}

def init():
	if __name__ == '__main__':
		sys.exit(Client.start())

init()


#kann das hier verwendet werden?
""" 	def __replaceEscapes(self, text):
		text = text.replace("\n", "\\n")
		text = text.replace("\r", "\\r")
		return text """
