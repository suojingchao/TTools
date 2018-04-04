#coding=utf-8
# a helper for logcat and monkey working together.

import os
import time
import re
import sys
import io
import threading


def runLogcat(device, logcatPath):
	print 'runLogcat begin'
	result = os.system('adb -s %s logcat -c && adb -s %s logcat -b events -v threadtime  > %s' % (device, device, logcatPath))
	print 'runLogcat end. result=%d' % result

def runMonkey(device, monkeyLogPath):
	print 'runMonkey begin'
	result = os.system('adb -s %s shell monkey -v -v -v --ignore-security-exceptions --ignore-crashes --ignore-native-crashes --ignore-timeouts  --throttle 200 --pkg-blacklist-file /sdcard/blacklist.txt 1000000 > %s' % (device, monkeyLogPath))
	print 'runMonkey end. result=%d' % result
	os._exit(0)

def main(argv):
	device = argv[1]
	logcatPath = argv[2]
	monkeyLogPath = argv[3]

	try:
		os.remove(logcatPath)
		os.remove(monkeyLogPath)
	except OSError:
		print 'IOError'

	begin = time.time()
	print 'begin %d' % begin
	
	t1 = threading.Thread(target=runLogcat, args=(device, logcatPath))
	t2 = threading.Thread(target=runMonkey, args=(device, monkeyLogPath))

	t2.start()
	t1.start()
	

	end = time.time()
	print 'end %d' % end
	print 'duration: %d' % (end - begin)
	#os._exit(0)


main(sys.argv)