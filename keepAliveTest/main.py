#coding=utf-8

import sys
import re
from datetime import *
import time
from processRecord import ProcessRecord
from processRecord import STATUS_NORMAL
from processRecord import STATUS_ONLY_END
from processRecord import STATUS_ONLY_BEGIN

DEFAULT_INPUT_PATH = "./tracker.txt"
path = DEFAULT_INPUT_PATH
processName = None

def dumpHelp():
	print '''Usage :python main.py -p process [-i] [logFile] [-h]
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
		if arg[:1] == "-":
			if cmd[:1] == "-" or cmd == "-h":
				dumpHelp()
				return
			else :
				cmd = arg
		elif cmd == "-p":
			processName = arg
			cmd = ""
		elif cmd == "-i":
			path = arg
			cmd = ""
		else :
			dumpHelp()
			return
	if not processName:
		dumpHelp()
		return
	else :
		return 1

def dumpResult(processRecords):
	result = ""
	keepAliveDuration = 0
	for processRecord in processRecords.values():
		result = result + processRecord.dumpSelf()
		keepAliveDuration = keepAliveDuration + processRecord.duration()
	print (('results: \n{0:%d}\t{1:5}\t{2:19}\t{3:19}\t{4:^}\n%s'%(len(processName), result)).format('processName', 'pid', 'begin', 'end', 'duration(s)')) + ('{0:%d}\t{1:5}\t{2:19}\t{3:19}\t{4:^}'%len(processName)).format("Total:", "%5s"%"", "%19s"%"", "%19s"%"", (str(keepAliveDuration)))

def main(argc, argv):
	if not argCheck(argc, argv):
		return
	year = date.today().year
	try :
		log = open(path, "r")
	except IOError:
		print "No such file or directory: %s"%path
	else :
		line = log.readline()
		processRecords = {}
		curProcess = None
		finalDate = None
		while line:
			line = line.replace("\n", " ")
			if re.match(r"^\d\d-\d\d", line):
				outArray = re.split(r"\s+", line)
				dateLog = outArray[0]
				t = outArray[1]
				finalDate = "%s-%s %s"%(year, dateLog, t)
				action = outArray[5]		
				if processName in line and "[" in line and "]" in line: 
					processBegin = line.index("[")
					processEnd = line.index("]")
					processSection = line[processBegin:processEnd]
					processArray = processSection.split(",")
					pid = processArray[1]
					curProcess = processRecords.get(pid, None)
					if ((action == "am_proc_start:" or action == "am_proc_start") and processArray[3] == processName) or ((action == "am_proc_bound:" or action == "am_proc_bound") and processArray[2] == processName):					
						curProcess = ProcessRecord(pid, processName)
						curProcess.setBegin(finalDate)
						curProcess.setStatus(STATUS_ONLY_BEGIN)
						processRecords[pid] = curProcess

					elif (action == "am_proc_died" or action == "am_kill" or action == "am_proc_died:" or action == "am_kill:") and processArray[2] == processName:
						if curProcess:
							curProcess.setEnd(finalDate)
							curProcess.setStatus(STATUS_NORMAL)
						else :
							curProcess = ProcessRecord(pid, processName)
							curProcess.setEnd(finalDate)
							curProcess.setStatus(STATUS_ONLY_END)
							processRecords[pid] = curProcess
					#else :
					#	print 'action[%s]pid[%s]name[%s]' % (action, pid, processArray[2])						
			line = log.readline()
		if curProcess and curProcess.getStatus() == STATUS_ONLY_BEGIN:
			curProcess.setEnd(finalDate)
			curProcess.setStatus(STATUS_NORMAL)
		else :
			print 'all match.'
		dumpResult(processRecords)	
		
# entry point.
main(len(sys.argv), sys.argv)

	
	