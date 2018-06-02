# coding:utf-8
"""
语音合成功能
逻辑实现：调用免费http://developer.baidu.com/vcast平台合成语音链接url
用linux平台下mpg123对语音链接实现执行，即播报

１、sudo apt-get install mgp123
２、每次播报的内容必须通过爬虫来是实现语音链接的实现，用步骤１读出来

"""

# 爬虫脚本
# 提交文字的地址

import requests
import os
def voice(title,content,speed=5,sex=2):
	s = requests.session()
	s.cookies['cookie']= 'BAIDUID=5F3DFCDFEDAC0639C33E6B7440030EFC:FG=1; BIDUPSID=5F3DFCDFEDAC0639C33E6B7440030EFC; PSTM=1513442712; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; H_PS_PSSID=1444_21124_22159; BDSFRCVID=pa-sJeCCxG3AXbJ7B256Diy95p4f9TOb_rbj3J; H_BDCLCKID_SF=tJPH_I8MJDt3qR5gMJ5q-n3HKUrL5t_XbI6y3JjOHJOoDDvDbPR5y4LdjG5thUKLWGuf5qk-WhvTs433bf4KbDup3-Aq54RXbj-joR3VHRROJJj63frcQfbQ0hQOqP-jW5TaBUjK0J7JOpvtbUnxy50S0aCDq68JfnPHoKv-5RbEqR5n5KT5MtuV-eTJ54RaKC8X3b7EfhcS_PO_bf--DRbX-4FeLTbGWbbHahOIbM7qOIoNqf6xy5K_hn6JQRTn-G6QbfJF3h54MPnHQT3mbRvbbN3i-4j7beuOWb3cWhoJ8UbSj-bme6oM-fuX5to05TIX3b7Ef-JHKtO_bfbT2MbyLJ7aBjbGtJIqKnTXfC52MbLw3MnDBnDVMGbZqtJHKbDJ_DthtU5; Hm_lvt_3abe3fb0969d25e335f1fe7559defcc6=1527524294; PSINO=7; BDRCVFR[feWj1Vr5u3D]=I67x6TjHwwYf0; FP_UID=9e88b762dd47a724aef5d5afa3692369; BDUSS=BBNzJGbzE2MlpYMlVaRXdNREV0TEk5UkQ0V2dXWEt0Q1Q2QkpBNzZubDUxVE5iQVFBQUFBJCQAAAAAAAAAAAEAAAASt-WLyubQ8r3cAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAHlIDFt5SAxbNl; Hm_lpvt_3abe3fb0969d25e335f1fe7559defcc6=1527531652'
	post_url = 'http://developer.baidu.com/vcast/getVcastInfo'
	# 表单参数
	data = {'title':title,
			'content':content,
			'sex':sex,
			'speed':speed,
			'volumn':'15',
			'pit':'5',
			'method': 'TRADIONAL'}
	headers = {
				'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
				'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8'
				}
	res = s.post(url=post_url,data=data,headers=headers)
	data =res.json()
	mp3_link = data['bosUrl']  # 获取语音合成链接
	# 用os模块执行语音输出命令
	order = 'mpg123 {}'.format(mp3_link)
	return order
	# print(res)