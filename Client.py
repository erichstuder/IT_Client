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

from lib.ClientParser import ClientParser
import sys
import os

class Client:
	@classmethod
	def start(cls):
		print("client started")
		cls.setupWindow()
		args = cls.parseArguments()
		ClientParser().run(initFile=args['initFile'], sessionFile=args['sessionFile'])

	@staticmethod
	def setupWindow():
		if sys.platform.startswith('win'):
			os.system('mode 70,15')
			os.system('title IT client')

	@staticmethod
	def parseArguments():
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
