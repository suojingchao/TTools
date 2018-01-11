#coding=utf-8

STATUS_NORMAL = 0
STATUS_ONLY_END = 1
STATUS_ONLY_BEGIN = 2 

class ProcessRecord:
	'一次生命周期记录'

	name = ""
	pid = 0
	begin = ""
	end = ""
	status = STATUS_NORMAL
	

	def __init__(self, pid, name):
		self.name = name
		self.pid = pid

	def setBegin(self, begin):
		self.begin = begin

	def setEnd(self, end):
		self.end = end

	def setStatus(self, status):
		self.status = status


	def duration(self):
		beginTimeArray = self.begin.split(":")
		beginTimestamp = int(beginTimeArray[0]) * 3600 + int(beginTimeArray[1]) * 60 + int(beginTimeArray[2][:beginTimeArray[2].index(".")])

		endTimeArray = self.end.split(":")
		endTimestamp = int(endTimeArray[0]) * 3600 + int(endTimeArray[1]) * 60 + int(endTimeArray[2][:endTimeArray[2].index(".")])
		return int(endTimestamp) - int(beginTimestamp)

	def dumpSelf(self):
		return ('{0:%d}\t{1:^}\t{2:^}\t{3:^}\t{4:^}\t\n'%len(self.name)).format(self.name, str(self.pid), str(self.begin), str(self.end),self.duration())


