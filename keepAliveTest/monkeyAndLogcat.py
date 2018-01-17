#coding=utf-8

import os
import time
import re
import sys
import io

# a helper for logcat and monkey working together.
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
	os.system('adb -s %s logcat -b events -v threadtime  > %s &' % (device, logcatPath))
	#adb shell monkey -v -v --ignore-crashes --ignore-native-crashes --ignore-timeouts  --throttle 200  100000
	os.system('adb -s %s shell monkey -v -v -v --ignore-security-exceptions --ignore-crashes --ignore-native-crashes --ignore-timeouts  --throttle 200  --pkg-blacklist-file /sdcard/blacklist.txt 100000 > %s' % (device, monkeyLogPath))
	#out = os.popen('jobs').read()
	#print out
	#outArray = re.split(r"\s+", out)
	#os.system('kill %s' % outArray[2])
	end = time.time()
	print 'duration: %d' % (end - begin)
main(sys.argv)