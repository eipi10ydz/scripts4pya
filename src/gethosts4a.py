# -*- coding:utf-8 -*-

import requests as req
import os
import android
import time
from multiprocessing import Process

def move():
	os.execlp('su', 'su', '-c', "mount -o rw,remount yaffs2 /system && mv ./hosts /etc/hosts")
	
if __name__ == '__main__':
	droid = android.Android()
	s = req.get('https://raw.githubusercontent.com/racaljk/hosts/master/hosts')
	if s.status_code == 200:
		with open('./hosts', 'w') as f:
			f.write(s.text)
		Process(target = move, args = ()).start()
		time.sleep(1)
		if time.time() - os.stat('/etc/hosts').st_ctime < 20:
			droid.notify('恭喜', '成功替换hosts文件')
		else:
			droid.notify('注意', '文件可能还在sl4a文件夹中')
	else:
		droid.notify('注意', '无法连接github...')