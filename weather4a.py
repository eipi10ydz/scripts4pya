#-*- coding:utf-8 -*-

import urllib2
import re
import android

class weather(object):
	def __init__(self,province,city):
		self.pattern = ur'<div class="cname">\s*<a target="_blank" href="/publish/forecast/A' + province + u'/' + city + ur'.html">\s*(\S*)\s*</a>\s*</div>\s*<div class="weather">\s*(\S*)\s*</div>\s*<div class="temp">\s*(\S*)\s*</div>\s*</li>' 
	def weather(self):
		try:
			res = urllib2.urlopen('http://www.nmc.cn/publish/forecast/china.html').read().decode('utf-8')	
		except urllib2.URLError:pass
			droid.notify('网络错误','无法获取天气信息')
		else:
			match = re.findall(self.pattern,res,re.M)
			if match:
				self.temperature = match[0][2]
				self.weather = match[0][1]
				self.combine = self.temperature + '  ' + self.weather
				self.city = match[0][0]
				droid.notify(city,combine)
				
droid = android.droid()

#you can use the class weather as my codes below

#hf = weather('AH','hefei')
#hf.weather()