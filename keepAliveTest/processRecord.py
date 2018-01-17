#coding=utf-8

from datetime import *
import time

STATUS_NORMAL = 0
STATUS_ONLY_END = 1
STATUS_ONLY_BEGIN = 2 

class ProcessRecord:
	'进程记录'

	name = ""
	pid = 0
	begin = ""
	end = ""
	status = STATUS_NORMAL
	

	def __init__(self, pid, name):
		self.name = name
		self.pid = pid

	def setBegin(self, begin):
		self.begin = begin[:begin.index(".")]

	def setEnd(self, end):
		self.end = end[:end.index(".")]

	def setStatus(self, status):
		self.status = status

	def getStatus(self):
		return self.status

	def duration(self):
		if self.begin != "" and self.end != "":
			beginDate = datetime.strptime(self.begin, '%Y-%m-%d %H:%M:%S')
			endDate = datetime.strptime(self.end, '%Y-%m-%d %H:%M:%S')
			return time.mktime(endDate.timetuple()) - time.mktime(beginDate.timetuple())
		else :
			return 0

	def dumpSelf(self):
		return ('{0:%d}\t{1:^}\t{2:19}\t{3:19}\t{4:^}\t\n'%len(self.name)).format(self.name, str(self.pid), str(self.begin), str(self.end),self.duration())


