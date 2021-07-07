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

#import threading
#import time
#import os
#import sys
#import importlib


class ClientParser:
	def __init__(self):
		self.__running = True
		self.__comPortHandler = ComportHandler(self.__printAnswer)
		
		self.__keyboardReaderThread = threading.Thread(target=self.__keyboardReaderWorker)
		self.__keyboardReaderThread.daemon = True
		self.__keyboardReaderThread.start()

		self.__scriptCommands = {
			"send": self.__keyboardInputParser,
			"sleep": time.sleep
		}

	def __keyboardReaderWorker(self):
		while self.__running:
			self.__keyboardInputParser(input().strip())

	def run(self, initFile, sessionFile):
		if initFile != None:
			self.__keyboardInputParser("run " + initFile)

		with open(sessionFile, "a+b") as sessionFile:
			while True:
				data = self.__comPortHandler.read()
				if data is not None:
					sessionFile.write(data)
					sessionFile.flush()
				if not self.__running:
					break

	def __keyboardInputParser(self, keyboardInput):
		if keyboardInput.startswith("set connectionType "):
			connectionType = keyboardInput.split(" ")[2]
			self.__comPortHandler.setConnectionType(connectionType)
			self.__printAnswer("connectionType set to: " + connectionType)
		elif keyboardInput.startswith("set VID "):
			vid = keyboardInput.split(" ")[2]
			self.__comPortHandler.setVID(vid)
			self.__printAnswer("VID set to: " + vid)
		elif keyboardInput.startswith("set PID "):
			pid = keyboardInput.split(" ")[2]
			self.__comPortHandler.setPID(pid)
			self.__printAnswer("PID set to: " + pid)
		elif keyboardInput.startswith("set comport "):
			comPort = keyboardInput.split(" ")[2]
			self.__comPortHandler.setPort(comPort)
			self.__printAnswer("comport set to: " + comPort)
		elif keyboardInput.startswith("run "):
			scriptFileName = keyboardInput.split(" ")[1]

			if not os.path.isfile(scriptFileName):
				self.__printAnswer("error: file not found")
				return

			with open(scriptFileName, "r") as scriptFile:
				if not scriptFileName.endswith(".py"):
					self.__printAnswer("unsuported file extension")
					return
				t = threading.Thread(target=lambda: exec(scriptFile.read(), self.__scriptCommands) )
				t.daemon = True
				t.start()
					
								
		elif keyboardInput == "exit":
			self.__printAnswer("goodbye...")
			self.__running = False
			time.sleep(0.5)
		else:
			self.__comPortHandler.write(keyboardInput + "\r")

	@staticmethod
	def __printAnswer(answer):
		print(">>  " + answer)


#kann das hier verwendet werden?
""" 	def __replaceEscapes(self, text):
		text = text.replace("\n", "\\n")
		text = text.replace("\r", "\\r")
		return text """