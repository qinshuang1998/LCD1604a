#!/usr/bin/env python
# -*- coding: UTF-8 -*-  
import urllib2
import json
import time
import re
import pi1604

def GetInfo(url): 
	request = urllib2.Request(url)
	response = urllib2.urlopen(request)
	result = response.read().strip('(').strip(')')
	info = json.loads(result)
	speed = {'input':info['NetInputSpeed3'],'output':info['NetOutSpeed3'],'mem':info['memRealPercent'],'time':info['uptime']}
	return speed

def ForDight(Dight,Time,How):
	if Dight<0:
		Last=0+"B/s"
	elif Dight<1024:
		Last=str(round(Dight,How))+"B/s"
	elif Dight<1048576:
		Dight=Dight/1024/Time
		Last=str(round(Dight,How))+"K/s"
	else:
		Dight=Dight/1048576/Time
		Last=str(round(Dight,How))+"M/s"
	return Last

if __name__=="__main__":
	try:
		url = "http://music.qugcloud.cn/tz.php?act=rt"
		lcd = pi1604.LCD1604()
		lcd.lcd_clear()
		day = [0x1F,0x04,0x04,0x1F,0x04,0x0A,0x11,0x00]
		lcd.create_char(0,day)
		speed1 = GetInfo(url)
		time1 = time.time()
		while 1:
			speed = speed1
			speed1 = GetInfo(url)
			time0 =time1
			time1 = time.time()
			result_in = "In:"+ForDight(float(speed1['input'])-float(speed['input']),float(time1)-float(time0),3)
			result_out = "Out:"+ForDight(float(speed1['output'])-float(speed['output']),float(time1)-float(time0),3)
			mem = "Memory:"+speed['mem']+"%"
			runtmp = "Run:"+speed['time']
			run = re.sub(u'[\u5929].*',"",runtmp)+"\x00"
			lcd.lcd_clear()
			lcd.lcd_string(result_in,1)
			lcd.lcd_string(result_out,2)
			lcd.lcd_string(mem,3)
			lcd.lcd_string(run,4)
	except ValueError:
		print "No valid JSON data"
		lcd.cleanup()
	except:
		print "Unexpected Error"
		lcd.cleanup()