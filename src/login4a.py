#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import requests
import re
import time
import android
from bs4 import BeautifulSoup
from requests import Session

class jwxtLogin(object):
	def __init__(self, username, passwd, gpa):
		self.username = username
		self.passwd = passwd
		self.temp = gpa
		self.loginInit()

	def loginInit(self):
		self.s = Session()

		url = 'http://mis.teach.ustc.edu.cn/userinit.do'

		initheaders = {
			'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0',
			'Referer':'http://mis.teach.ustc.edu.cn/'
		}
		initdata = {'userbz':'s'}

		self.s.headers = initheaders
		try:
			resp = self.s.post(url,data=initdata)
		except:
			droid.notify('网络错误','无法连接教务系统网站')
		else:
			self.getCheckCode(resp)

	def getCheckCode(self, resp):
		soup = BeautifulSoup(resp.text,'html5lib')
		RANDOM = 4
		rand = soup.find_all('img')[RANDOM]['src']
		yzmUrl = "http://mis.teach.ustc.edu.cn/" + rand

		headers = {
			'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0',
			'Referer':'http://mis.teach.ustc.edu.cn/userinit.do',
		}
		self.s.headers = headers
		try:
			resp = self.s.get(yzmUrl)
		except:
			droid.notify('网络错误','无法获取验证码图片')
		else:
			with open('./1.jpg','wb') as f:
				f.write(resp.content)
			droid.notify('提示','请到sl4a文件夹获取验证码')
			yzm = input('验证码:')

			postdata = {
				'userbz':'s',
				'hidjym':'',
				'userCode':self.username,
				'passWord':self.passwd,
				'check':yzm
			}
			try:
				resp = self.s.post('http://mis.teach.ustc.edu.cn/login.do',data=postdata)
			except:
				droid.notify('网络错误','无法登陆教务系统')
			else:
				r = re.findall('confirm',resp.text)
				if not r:
					r = re.findall('alert\(\'(\S+)\'\)',resp.text)
					droid.notify('提示',r[0])
				else:
					droid.notify('提示','登陆成功！')
					while True:
						self.askForGrade()
						time.sleep(5)
	
	def askForGrade(self):
		resp = self.s.post('http://mis.teach.ustc.edu.cn/querycjxx.do')
		soup=BeautifulSoup(resp.text,'html5lib')
		res=soup.find_all('td')
		tempGPA = res[9].string[2:6]
		if tempGPA != self.temp:
			self.temp = tempGPA
			droid.notify('出成绩啦', ':(')
			with open('./cj.html','w') as f:
				f.write(resp.text)
			if self.showDialog() == 'positive':
				droid.notify(':(', tempGPA)
				droid.webViewShow('file:///storage/emulated/0/sl4a/cj.html')
			
	def showDialog(self):
		droid.dialogCreateAlert('是否查看', ':(')
		droid.dialogSetPositiveButtonText('好')
		droid.dialogSetNegativeButtonText('不')
		droid.dialogShow()
		return droid.dialogGetResponse()[1]['which']

if __name__ == '__main__':
	droid = android.Android()
#	jwxtLogin(your username, your password, your gpa)

