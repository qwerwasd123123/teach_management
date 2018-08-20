#-*- coding:utf-8 -*-
####系统入口

import os
import pymysql
import Student
import Teacher
import Login
import SystemManager

if __name__ == '__main__':
	conn = pymysql.connect("locakhost",passwd = 'zz1zz2zz3',db = 'db_educationalmanagementsystem')
	log = Login.Login(conn)
	if log.MainFunc():
		account = log.GetLoginAccount()
		if account[2] == 0:
			usr = SystemManager.SystemManager(conn,account[0],account[1])
			usr.MainFunc()
		elif account[2] == 1:
			usr = Teacher.Teacher(conn,account[0],account[1])
			usr.MainFunc()
		elif account[2] == 2:
			usr = Student.Student(conn,account[0],account[1])
			usr.MainFunc()
		else : 
			conn.close()
			raise exception()
	conn.close()
	