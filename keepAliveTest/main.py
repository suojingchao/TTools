#coding=utf-8

import sys
import re
from processRecord import ProcessRecord
from processRecord import STATUS_NORMAL
from processRecord import STATUS_ONLY_END
from processRecord import STATUS_ONLY_BEGIN

DEFAULT_INPUT_PATH = "./tracker.txt"
path = DEFAULT_INPUT_PATH
processName = None

def dumpHelp():
	print '''Usage :
	-p: （required）process name.
	-i: （optional）input file path(default ./tracker.txt).
	-h:  dump help info.
	'''

def argCheck(argc, argv):
	global processName
	global path
	cmd = ""
	for index in range(len(argv)):
		# index 0 is xxxx.py
		if index == 0:
			continue
		arg = argv[index]
		print arg
		if arg[:1] == "-":
			cmd = arg
			if cmd == "-h":
				dumpHelp()
				return
		elif cmd == "-p":
			processName = arg
		elif cmd == "-i":
			path = arg
		else :
			dumpHelp()
			return
	return 1

def dumpResult(processRecords):
	result = ""
	keepAliveDuration = 0
	for processRecord in processRecords.values():
		result = result + processRecord.dumpSelf()
		keepAliveDuration = keepAliveDuration + processRecord.duration()
	print (('results: \n{0:%d}\t{1:5}\t{2:12}\t{3:12}\t{4:^}\n%s'%(len(processName), result)).format('processName', 'pid', 'begin', 'end', 'duration')) + ('{0:%d}\t{1:5}\t{2:12}\t{3:12}\t{4:^}'%len(processName)).format("Total:", "%5s"%"", "%12s"%"", "%12s"%"", (str(keepAliveDuration)))

def main(argc, argv):
	if not argCheck(argc, argv):
		return
	log = open(path, "r")
	line = log.readline()
	processRecords = {}
	while line:
		line = line.replace("\n", " ")
		if re.match(r"^\d\d-\d\d", line):
			outArray = re.split(r"\s+", line)
			date = outArray[0]
			time = outArray[1]
			action = outArray[5]		
			if processName in line and "[" in line and "]" in line: 
				processBegin = line.index("[")
				processEnd = line.index("]")
				processSection = line[processBegin:processEnd+1]
				processArray = processSection.split(",")
				pid = processArray[1]
				curProcess = processRecords.get(pid, None)
				if (action == "am_proc_start:" and processArray[3] == processName) or (action == "am_proc_bound:" and processArray[2] == processName):					
					curProcess = ProcessRecord(pid, processName)
					curProcess.setBegin(time)
					curProcess.setStatus(STATUS_ONLY_BEGIN)
					processRecords[pid] = curProcess

				elif (action == "am_proc_died" or action == "am_kill") and processArray[2] == processName:
					if curProcess:
						curProcess.setEnd(time)
						curProcess.setStatus(STATUS_NORMAL)
					else :
						curProcess = ProcessRecord(pid, processName)
						curProcess.setEnd(time)
						curProcess.setStatus(STATUS_ONLY_END)						
				#print date + " " + time + " " + pid + " " + processSection
		line = log.readline() 
	dumpResult(processRecords)	
		
# entry point.
main(len(sys.argv), sys.argv)

	
	