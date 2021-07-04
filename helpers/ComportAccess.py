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

import pyudev

class ComportAccessException(Exception):
	pass

class _ComportAccess:
	@staticmethod
	def findPortByVidAndPid(vid, pid):
		udev = pyudev.Context()
		devices = []
		for d in  udev.list_devices(subsystem="tty", ID_VENDOR_ID=vid):
			if d.get("ID_MODEL_ID") == pid:
				devices += [d]
		if len(devices) == 0:
			raise ComportAccessException("no device found")
		if len(devices) > 1:
			raise ComportAccessException("more than one device found")
		return devices[0].device_node	
