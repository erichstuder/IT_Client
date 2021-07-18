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
import sys
import os

class Client:
	@classmethod
	def start(cls):
		print("client started")
		cls._setupWindow()

		args = cls._parseArguments()
		initFile = args['initFile']
		sessionFile = args['sessionFile']
		comportHandler = ComportHandler()
		commandParser = CommandParser(comportHandler)
		keyboardReader = KeyboardReader(commandParser)
		keyboardReader.start()
		if initFile != None:
			commandParser.parse("run " + initFile)
		comportLogger = ComportLogger(comportHandler, sessionFile)
		comportLogger.run()

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
