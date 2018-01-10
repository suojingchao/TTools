#coding=utf-8



log = open("./tracker.txt", "r")
line = log.readline()
lastStatus = 0
while line:
	outArray = line.split(" ")
	if len(outArray) > 4:
		date = outArray[0]
		time = outArray[1]
		#action = outArray[5]
		newline = line.replace("\n", " ")
		if "com.taidu8.datamanager" in line and "[" in line and "]" in line: 
			processBegin = newline.index("[")
			processEnd = newline.index("]")
			processSection = newline[processBegin:processEnd]
			array = processSection.split(",")		
			print date + " " + time + " "  + " " + array[len(array) - 1]
	line = log.readline() 
		
		


	
	