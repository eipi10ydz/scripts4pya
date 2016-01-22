#-*- coding:utf-8 -*-

import urllib
import urllib2
import cookielib
import re
import android

droid = android.Android()

cookie=cookielib.CookieJar()
opener=urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))

url = 'http://wlt.ustc.edu.cn/cgi-bin/ip'
postdata = urllib.urlencode({
		"cmd":"login",
		"url":"URL",
		"name":#your name here,
		"password":#your password here
	})
choice = 8
patternWwang = ur'<table border=0 width=620 cellspacing=0 bordercolor="#cccccc"><tr><td></td><td>(\S*)<font color=red>(\S*)<br>\s*</td></tr></table>'
patternNwang = ur'<tbody><tr><td>(\S*)<br>\s*(\S*)\s*(\S*?)<br>\s*(\S*)\s(\S*)'

try:
	req = urllib2.Request(url = url,data = postdata)
	result = opener.open(req)
except urllib2.URLError:
	droid.notify(u'网络错误',u'无法连接网络通网站')
else:
	try:
		req = urllib2.Request(url = url + '?cmd=set&url=URL&type=' + str(choice))
		result=opener.open(req).read()
	except urllib2.URLError:
		droid.notify(u'网络错误',u'无法登陆网络通')
	else:
		try:
			res = re.findall(patternWwang,result,re.M)
			if len(res[0]) == 2:
				droid.notify(u'注意',u'IP地址非科大IP地址,无法设置权限')
		except IndexError:
			res = re.findall(patternNwang,result,re.M)
			if len(res[0]) == 5:
				droid.notify(u'提示',u'登陆成功')