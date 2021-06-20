#!/usr/bin/python3
#coding=utf8


import requests
import json 
from lxml import etree
import pysnooper

import yaml 

# proxies = {
# 	"http": "127.0.0.1:12639",
# }
def write_html(code, _page):
	with open("fund_data/html/" + code + ".html" , "w") as f:
		f.write(_page)

def read_html(code):
	with open("fund_data/html/" + code + ".html" , "r") as f:
		return f.read()

# @pysnooper.snoop()
def craw(code):
	stock_list = []

	url = "http://fund.eastmoney.com/" + code + ".html" 
	r = requests.get(url) 
	r.encoding='utf-8'

	_page = r.text 

	write_html(code, _page)

	_page = read_html(code)
	# print(_page)
	page = etree.HTML(_page)

	# print(page)
	# //*[@id="position_shares"]/div[1]/table/tbody/tr[2]
	# xpath = '//li[@id="position_shares"]/div[1]/table/tbody/tr'
	## 吐了 ， 爬下来的没有tbody , 浏览器里有 。。。！！！ 

	xpath = '//li[@id="position_shares"]/div[1]/table/tr'
	# xpath= "/html/body/div[1]/div[13]/div/div/div[1]/div[2]/div[2]/ul/li[1]/div[1]/table/tbody/"
	trList = page.xpath(xpath)

	# print(trList) 
	## 没有持仓数据 
	if len(trList) < 3:
		return stock_list 

	for lineNo, tr in enumerate(trList) :
		if lineNo == 0 :
			continue
		stock_dict = {}

		stock_url = tr.xpath('./td[1]/a/@href')[0]    ## 
		print(stock_url)
		uri = stock_url.replace("http://quote.eastmoney.com/", "").strip().replace(".html", "")

		print(uri)
		## aapl
		stock_code = ""
		if uri.startswith("us/") :
			stock_code = uri.replace("us/", "").lower()

		## hk700 
		if uri.startswith("hk/") :
			stock_code = "hk" + uri.replace("hk/", "")

		### 
		if uri.startswith("sz") :
			stock_code = uri.replace("sz", "")
		if uri.startswith("sh"): 
			stock_code = uri.replace("sh", "")

		stock_name = str(tr.xpath('./td[1]/a/text()')[0])  ## 

		ratio = float(tr.xpath("./td[2]/text()")[0].replace("%", ""))
		
		print(stock_code, stock_name, ratio)


		# stock_name = _type1.encode("utf8").rstrip("\n") 

		stock_dict["stock_code"] = stock_code
		stock_dict["stock_name"] = stock_name
		stock_dict["ratio"] = ratio
		stock_list.append(stock_dict)
	
	print(stock_list)
	return stock_list 
def gen_yaml(stock_data):
	fund_code = stock_data["fund_code"] 
	fund_name = stock_data["fund_name"]

	_filename = fund_name + "_" +  fund_code   + ".yaml"
	with open("fund_data/2021q1/" + _filename, "w") as fw :
		yaml.dump(stock_data, fw, default_flow_style=False,encoding='utf-8',allow_unicode=True)
 

def main():

	with open("./fund_data/fund_code.txt", "r") as f :
		for l in f :
			stock_data = {}
			if l.startswith("#"):
				continue
			data = l.strip("\n").split() 
			fund_code = data[0]
			fund_name = data[1]
			fund_money = int(data[2])

			
			stock_data["fund_code"] = fund_code
			stock_data["fund_name"] = fund_name
			stock_data["fund_money"] = fund_money

			fund_data = craw(fund_code)

			## 忽略 
			if len(fund_data) == 0 :
				continue 

			stock_data["fund_data"] = fund_data 
			gen_yaml(stock_data)

if __name__ == '__main__':
	main()