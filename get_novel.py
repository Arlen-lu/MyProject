#-*- coding:utf-8 -*-
import io
import sys
from bs4 import BeautifulSoup
import time
import requests
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8') #改变标准输出的默认编码


class downloader(object):

	def __init__(self):
		self.server = "http://www.biqukan.com"
		self.target = self.server +'/'+'2_2822'
		self.headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:60.0) Gecko/20100101 Firefox/60.0'}
		#存放章节名
		self.names = []
		#存放章节链接
		self.urls = []
		self.nums = 0

	def get_catalog(self):
		#获取目录
		req = requests.get(url=self.target,headers=self.headers)
		html=req.text
		div_bf = BeautifulSoup(html,'html5lib')
		#匹配class属性为listmain的div标签
		div = div_bf.find_all('div',class_ = 'listmain')
		a_bf = BeautifulSoup(str(div),'html5lib')
		a = a_bf.find_all('a')
		# print(a[1])
		#剔除不必要的章节,前11章
		a = a[12:]
		self.nums = len(a)
		for each in a:
			self.names.append(each.string)
			self.urls.append(self.server + each.get('href'))
		return [self.names,self.urls,self.nums]

	def get_content(self,target):
		req = requests.get(url=target,headers=self.headers)
		html = req.text
		bf = BeautifulSoup(html,'html5lib')
		texts = bf.find_all('div',class_ = 'showtxt')
		# print(texts)
		# 去除div标签
		texts = texts[0].text
		# print(type(texts))
		#去除空格,得到内容正文
		texts = texts.replace('<br/>','')
		return texts

	def writer(self,name,path,text):
		#name-章节名称，path当前路径下，保存的书名，text-书名称
		with open(path,'a',encoding='utf-8') as f:
			f.write(name + '\n')
			f.writelines(text)
			f.write('\n\n')

if __name__ =="__main__":
	dl = downloader()
	dl.get_catalog()
	print("《雪中悍刀行》开始下载:")
	print(dl.nums)
	print(dl.names[1])
	print(dl.urls[1])
	for i in range(dl.nums):
		dl.writer(dl.names[i],'雪中悍刀行.txt',dl.get_content(dl.urls[i]))
		sys.stdout.write("已下载:%.3f%%" %  float(i/dl.nums) + '\r')
		#刷新输出
		sys.stdout.flush()
		time.sleep(1)
	print("download successfully!")