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

import time
import os
import threading

class CommandParserException(Exception):
	pass

class CommandParser:
	def __init__(self, comportHandler):
		self.__comPortHandler = comportHandler

	def parse(self, data):
		if data.startswith("set connectionType "):
			connectionType = data.split(" ")[2]
			self.__comPortHandler.connectionType = connectionType
			self.__printAnswer("connectionType set to: " + connectionType)
		elif data.startswith("set VID "):
			vid = data.split(" ")[2]
			self.__comPortHandler.vid = vid
			self.__printAnswer("VID set to: " + vid)
		elif data.startswith("set PID "):
			pid = data.split(" ")[2]
			self.__comPortHandler.pid = pid
			self.__printAnswer("PID set to: " + pid)
		elif data.startswith("set comport "):
			comPort = data.split(" ")[2]
			self.__comPortHandler.port = comPort
			self.__printAnswer("comport set to: " + comPort)
		elif data.startswith("run "):
			scriptFileName = data.split(" ")[1]

			if not os.path.isfile(scriptFileName):
				raise ClientParserException('error: file not found')

			with open(scriptFileName, "r") as scriptFile:
				if not scriptFileName.endswith(".py"):
					raise ClientParserException('unsupported file extension')
				t = threading.Thread(target=lambda: exec(scriptFile.read(), {"send": self.parse}) )
				t.daemon = True
				t.start()
								
		elif data == "exit":
			self.__printAnswer("goodbye...")
			time.sleep(0.5)
			exit() #TODO das Programm sollte nicht hier verlassen werden
		else:
			self.__comPortHandler.write(data + "\r")

	@staticmethod
	def __printAnswer(answer):
		print(">>  " + answer)


#kann das hier verwendet werden?
""" 	def __replaceEscapes(self, text):
		text = text.replace("\n", "\\n")
		text = text.replace("\r", "\\r")
		return text """

