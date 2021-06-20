#!/usr/bin/python3
#coding=utf8

from collections import defaultdict
import time 
import sys 
import re 
import ast
import json 
import os 
import datetime 
import glob
import yaml 
import pysnooper

from prettytable import PrettyTable
from prettytable import MSWORD_FRIENDLY, PLAIN_COLUMNS

# @pysnooper.snoop()
def looksup():
	fileName = "fund_data/2021q1/*.yaml"
	fileList = glob.glob(fileName)

	
	stock_dict = defaultdict()

	unique_stock_name = {}
	##{
	## 300122: {
		## { stock_code :
		##   stock_name: 
		##   stock_sub_fund_data_list: [{
		##      fund_name : 
		##      fund_code :
		##      fund_ratio_money:
		##  }]
		##   stock_sum_money: 
		##    }
	##}
	for _fileName in fileList:
		with open(_fileName, "r") as f :
			content = yaml.load(f, Loader=yaml.FullLoader)

			## process fund code 
			fund_code = content["fund_code"]

			# if str(fund_code).isdigit():
			# 	if len(str(fund_code)) < 6 :
			# 		fund_code_oct = oct(fund_code).lstrip("0o") ## str  
			# 		while len(fund_code_oct) < 6:
			# 			fund_code_oct = "0" + fund_code_oct
			# 		fund_code = fund_code_oct
			fund_code = code_trans(fund_code)
			fund_code = str(fund_code)
			###   
			# print(fund_code)


			fund_name = content["fund_name"]
			fund_money = content["fund_money"]

			fund_data_list = content["fund_data"]

			for fund_data in fund_data_list :

				### process stock code  002142 
				stock_code = fund_data["stock_code"]
				# print(stock_code)  ## 
				# if str(stock_code).isdigit():
				# 	if len(str(stock_code)) < 6 :
				# 		stock_code_oct = oct(stock_code).lstrip("0o") ## str  真是费劲啊 
				# 		while len(stock_code_oct) < 6:
				# 			stock_code_oct = "0" + stock_code_oct
				# 		stock_code = stock_code_oct
				stock_code = code_trans(stock_code)

				# print(stock_code)
				# print("---------------")
				stock_code = str(stock_code)
				#######

				
				## process name repeat case 
				stock_name = fund_data["stock_name"]
				if stock_code not in unique_stock_name.keys() :
					unique_stock_name[stock_code] = stock_name
				else :
					stock_name = unique_stock_name[stock_code]
				#####################################################################


				# print fund_data
				ratio = fund_data["ratio"]
				fund_ratio_money = int(float(fund_money) * float(ratio) / 100 )

				## exist
				if stock_code in stock_dict.keys():
					stock_sub_fund_data_list = stock_dict[stock_code]["stock_sub_fund_data_list"]
					stock_sub_fund_data_list.append({
							"fund_name" : fund_name,
							"fund_code" : str(fund_code),
							"fund_ratio_money" : fund_ratio_money
						})
					stock_dict[stock_code]["stock_sum_money"] += fund_ratio_money
				## new init 
				else :
					stock_sub_fund_data =  {
						"fund_name" : fund_name,
						"fund_code" : str(fund_code),
						"fund_ratio_money" : fund_ratio_money
					}
					stock_sum_money = fund_ratio_money

					stock_dict[stock_code] =  {
						"stock_code" : stock_code,
						"stock_name" : stock_name , 
						"stock_sub_fund_data_list": [stock_sub_fund_data], 
						"stock_sum_money": stock_sum_money
					}

	## write stock data
	# print stock_dict
	for stock_code, stock_data in stock_dict.items() : 
		
		# print(stock_code)
		stock_name = stock_data["stock_name"]
		# print(stock_data)
		dst = "stock_data/2021q1/" + stock_code + "_" + stock_name + ".yaml" 
		with open(dst, "w") as fw:
			yaml.dump(stock_data, fw, default_flow_style=False,encoding='utf-8',allow_unicode=True)

def code_trans(stock_code):
	if str(stock_code).isdigit():
		if len(str(stock_code)) < 6 :
			stock_code_oct = oct(stock_code).lstrip("0o") ## str  真是费劲啊 
			while len(stock_code_oct) < 6:
				stock_code_oct = "0" + stock_code_oct
			stock_code = stock_code_oct
	return stock_code

def tj():
	fileName = "stock_data/2021q1/*.yaml"
	fileList = glob.glob(fileName)

	all_money = 0 
	stock_summary_list = []

	x = PrettyTable()
	for _fileName in fileList: 
		with open(_fileName, "r") as f :
			content = yaml.load(f, Loader=yaml.FullLoader)

			stock_code = content["stock_code"]
			stock_name = content["stock_name"]
			stock_sum_money = content["stock_sum_money"]
			stock_summary_list.append({
				"stock_code" : stock_code, 
				"stock_name" : stock_name,
				"stock_sum_money": stock_sum_money,
				})
			all_money += stock_sum_money

	## add 比例
	for stock in stock_summary_list: 
		stock["ratio"] = "{:.2f}".format(stock["stock_sum_money"] / float(all_money) *100 ) + "%"

		x.field_names = ["股票code", "股票", "头寸", "占比"]
		x.add_row([stock["stock_code"], stock["stock_name"], stock["stock_sum_money"], stock["ratio"]])
	
	## 
	x.align = "c"
	## 不是全部价值	
	print("基金前10大持仓，总仓位：", all_money, "  RMB")
	print(x.get_string(sortby="头寸", reversesort=True))


def tj_by_fund_code(code):
	fileName = "fund_data/2021q1/*" + code+ "*.yaml"
	fileList = glob.glob(fileName)
	x = PrettyTable()

# 	fund_code: 003494
# fund_name: 富国天惠成长
# fund_money: 4770
# fund_data: 
#   - stock_name: 智飞生物
#     stock_code: 300122
#     ratio: 4.63

	x.field_names = ["股票code", "股票", "头寸", "占比"]
	for _fileName in fileList: 
		with open(_fileName, "r") as f :
			content = yaml.load(f, Loader=yaml.FullLoader)

			fund_name = content["fund_name"]
			print(fund_name)
			fund_data = content["fund_data"]
			fund_money = content["fund_money"]
			print("持仓: ", fund_money, " RMB")
			for stock in fund_data : 
				stock_money = int(fund_money * stock["ratio"] / 100 )
				x.add_row([code_trans(stock["stock_code"]),stock["stock_name"], stock_money, str(stock["ratio"]) + "%" ])

	print(x.get_string(sortby="头寸", reversesort=True))



def tj_by_stock_code(code):
	fileName = "stock_data/2021q1/*" + code + "*.yaml"
	fileList = glob.glob(fileName)

	## 
# 	stock_code: '600519'
# stock_name: 贵州茅台
# stock_sub_fund_data_list:
# - fund_code: 003494
#   fund_name: 富国天惠成长
#   fund_ratio_money: 201
# - fund_code: '180012'
#   fund_name: 银华富裕主题混合
#   fund_ratio_money: 236
# stock_sum_money: 437
	x = PrettyTable()
	x.field_names = ["基金code", "基金", "头寸", "占比"]
	for _fileName in fileList: 
		with open(_fileName, "r") as f :
			content = yaml.load(f, Loader=yaml.FullLoader)

			stock_name = content["stock_name"]
			print(stock_name)
			stock_sub_fund_data_list = content["stock_sub_fund_data_list"]
			stock_sum_money = content["stock_sum_money"]
			print("持仓: ", stock_sum_money, " RMB")
			for fund in stock_sub_fund_data_list : 
				ratio= "{:.2f}".format(fund["fund_ratio_money"] / float(stock_sum_money) *100 ) + "%"
				x.add_row([fund["fund_code"],fund["fund_name"], fund["fund_ratio_money"], ratio  ])
	x.align = "c"
	# x.align["基金"] = "c"
	# x.align["头寸"] = "r"
	# x.align["占比"] = "c"
	x.set_style(PLAIN_COLUMNS)  # 无边界样式，适合柱状数据

	print(x.get_string(sortby="头寸", reversesort=True))

def main():
	## 按股票倒排 
	## hk的开头加标注， 否则无法区别 、 默认0开头的数字给整成8进制了。。。。
	looksup()
	
	if len(sys.argv) > 1: 
		_t = sys.argv[1]  
		code = sys.argv[2] 
		## 按基金号码查询 
		## 支持模糊查找
		if _t == "-f": 
			tj_by_fund_code(code)
		## 按股票号码查询基金信息
		## 支持模糊查找
		if _t == "-s":
			tj_by_stock_code(code)
	else :
		tj()
if __name__ == '__main__':

	main()