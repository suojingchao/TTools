#coding=utf-8

import os
import time
import re
import sys
import io

def main(argv):
	device = argv[1]
	logcatPath = argv[2]
	monkeyLogPath = argv[3]

	os.remove(logcatPath)
	os.remove(monkeyLogPath)

	begin = time.time()
	os.system('adb logcat -b events -v threadtime  > %s &' % logcatPath)
	os.system('adb -s %s shell monkey -v -v --ignore-crashes --ignore-native-crashes --ignore-timeouts  --throttle 20  500 > %s' % (device, monkeyLogPath))
	#out = os.popen('jobs').read()
	#print out
	#outArray = re.split(r"\s+", out)
	#os.system('kill %s' % outArray[2])
	end = time.time()
	duration = str(end - begin)
 	file = io.open(logcatPath, mode='w+', encoding='utf-8')
	file.write('finish! duration: ' + duration)
	file.close()

main(sys.argv)