#coding=utf-8

import sys

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

def dumpResult(ANRCount, CrashCount):
	print '{0:10}\t{1:10}\n{2:10}\t{3:10}'.format("ANRCount", str(ANRCount), "CrashCount", str(CrashCount))

def main(argc, argv):
	if not argCheck(argc, argv):
		return
	try :
		log = open(path, "r")
	except IOError:
		print "No such file or directory: %s"%path
	else :
		ANRCount = 0
		CrashCount = 0
		line = log.readline()
		while line:
			line = line.replace("\n", " ")
			if "ANR in %s"%processName in line:
				ANRCount = ANRCount + 1;
			elif "// CRASH: %s"%processName in line:
				CrashCount = CrashCount + 1
			line = log.readline() 
		dumpResult(ANRCount, CrashCount)
		
# entry point.
main(len(sys.argv), sys.argv)