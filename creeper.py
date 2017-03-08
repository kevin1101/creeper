#字符编码声明
# -*- coding: utf-8 -*-
#导入/引入python标准模块
from bs4 import BeautifulSoup # BeautifulSoup4
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException # selenium操作浏览器
import threading # 多线程
from time import ctime,sleep # 时间
import re # 正则
import pymysql, pymysql.cursors # 数据库
import urllib.request
#===========================
#自定义函数
#---------------------------
#创建数据库存连接
def connDB():  
	conn=pymysql.connect(host="192.168.1.109",user="creeper",passwd="scrapy",db="scrapy")
	return conn
#关闭数据库存连接
def connClose(conn):
	conn.close();
#---------------------------
#设置浏览器
def driver_set():
	#浏览器设置
	#driver = webdriver.Chrome(executable_path = 'C:\Python36\chromedriver.exe')
	driver = webdriver.Chrome()
	driver.set_window_position(0,40)
	driver.set_window_size(1080,1040)
	driver.get('http://www.dianping.com/')
	sleep(30)
	return driver
#检查验证码

#---------------------------
#获取列表

#获取详情
def get_remark(soup):
	user = soup.find("a", "J_card")
	user_id = user['user-id']
	grade = soup.find("span", "item-rank-rst")
	if grade is None:
		u_grade = '无'
	else:
		u_grade = grade['class'][1].split("star")[-1]

	grades = soup.find_all("dd")

	if len(grades):
		grade_1 = grades[0].text.split("(")[0]
		grade_2 = grades[1].text.split("(")[0]
		grade_3 = grades[2].text.split("(")[0]
	else:
		grade_1 = ''
		grade_2 = ''
		grade_3 = ''

	remark_info = soup.find("div", attrs={"id":re.compile(r'^review_')}).get_text()
	remark_info.replace('\n','').replace(' ','')
	remark_time = soup.find("span", "time").text
	return user_id,u_grade,grade_1,grade_2,grade_3,remark_info,remark_time
#下一页
def next_page(driver):
	try:
		driver.find_element_by_link_text(u"下一页").click()
		sleep(1)
		return True
	except:
		return False
#结束
def finish():
	print('执行完毕！')
#---------------------------
#查询数据
def get_web_portal():
	#爬虫入口
	connection = connDB()
	try:
		with connection.cursor() as cursor:
			# Read a single record
			sql = "SELECT `id`, `s_id` FROM `store` WHERE `is_get`=%s LIMIT 1"
			cursor.execute(sql, ('0',))
			result = cursor.fetchone()
			#print(result)
	finally:
		connClose(connection)
	if result is not None:
		url = 'http://www.dianping.com/shop/'+str(result[1])+'/review_more'
		return url,result[0],result[1]
	else:
		url = 'http://www.dianping.com/'
		return url,None,None
#修改数据
def update_store(row_id):
	connection = connDB()
	try:
		with connection.cursor() as cursor:
			# Read a single record
			sql = "UPDATE store SET is_get='1' WHERE id='"+str(row_id)+"'"
			#print(sql)
			sta = cursor.execute(sql)
			if sta == 1:
				connection.commit()
				#print('Done')
			else:
				print('Failed')
			#print(result)
	finally:
		connClose(connection)
#===========================
#程序主体
def get_store_remarks(driver):
	store_url,row_id,s_id = get_web_portal()
	if row_id is None:
		driver.quit()
		return False
	else:
		print(row_id)
	#判断是否正常打开页面
	#print(driver.current_url)
	has_remark = True
	sleep(1)
	while has_remark:
		data = BeautifulSoup(driver.page_source, "html.parser").find_all("li", "comment-list-item")
		if data is None:
			print(u'此商家暂无评论！')
			break
		connection = connDB()
		for t in data:
			user_id,u_grade,grade_1,grade_2,grade_3,remark_info,remark_time = get_remark(t)
			#print(s_id)
			#print(user_id)
			#print(u_grade)
			#print(grade_1,grade_2,grade_3)
			#print(grades[1].text.split("(")[0])
			#print(grades[2].text.split("(")[0])
			#print(remark_info)
			#print(remark_time)
			with connection.cursor() as cursor:
				# Read a single record
				sql = "INSERT INTO `remark` (`s_id`, `user_id`, `u_grade`, `grade_1`, `grade_2`, `grade_3`, `content`, `remark_time`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
				cursor.execute(sql, (int(s_id), int(user_id), u_grade, grade_1, grade_2, grade_3, remark_info, remark_time))
				#print(sql)
			#connection.commit()
			#print("用户ID:"+str(user_id)+"评论数据写入失败！商家ID:"+str(s_id))
			has_remark = next_page(driver)
		connClose(connection)
		update_store(row_id)
		return True
#---------------------------
driver = driver_set()
res = True
while res:
	res = get_store_remarks(driver)
finish()