#-*- coding:utf-8 -*-

import urllib.request, urllib.parse, urllib.error
import urllib.request, urllib.error, urllib.parse
import http.cookiejar
import re
import android

droid = android.Android()

cookie=http.cookiejar.CookieJar()
opener=urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookie))

url = 'http://wlt.ustc.edu.cn/cgi-bin/ip'
postdata = urllib.parse.urlencode({
		"cmd":"login",
		"url":"URL",
		"name":#your name here,
		"password":#your password here
	}).encode()

choice = 8
patternWwang = r'<table border=0 width=620 cellspacing=0 bordercolor="#cccccc"><tr><td></td><td>(\S*)<font color=red>(\S*)<br>\s*</td></tr></table>'
patternNwang = r'<tbody><tr><td>(\S*)<br>\s*(\S*)\s*(\S*?)<br>\s*(\S*)\s(\S*)'

try:
	req = urllib.request.Request(url = url,data = postdata)
	result = opener.open(req)
except urllib.error.URLError:
	droid.notify('网络错误','无法连接网络通网站')
else:
	try:
		req = urllib.request.Request(url = url + '?cmd=set&url=URL&type=' + str(choice))
		result=opener.open(req).read().decode('gb2312')
	except urllib.error.URLError:
		droid.notify('网络错误','无法登陆网络通')
	else:
		try:
			res = re.findall(patternWwang,result,re.M)
			if len(res[0]) == 2:
				droid.notify('注意','IP地址非科大IP地址,无法设置权限')
		except IndexError:
			try:
				res = re.findall(patternNwang,result,re.M)
				if len(res[0]) == 5:
					droid.notify('提示','登陆成功')
			except IndexError:
				droid.notify('提示','未开通网络通')
				
#replace the #... with your username and password
#if you want to change the exit, please change the value of choice
#the value of choice equals to the number of exit minus 1