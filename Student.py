#-*- coding:utf-8 -*-
####学生账号

import pymysql
import os

class Student:
	def __init__(self,conn,account,passwd):				
		###构造,conn连接数据库
		cur = conn.cursor()
		sqlcmd = "select Name,Gender,Birth,Academy,Major,Grade,TeacherNo from StudentInfo where StudentNo = '%s'" % account
		cur.execute(sqlcmd)
		res = cur.fetchone()
		sqlcmd = "select Name from TeacherInfo where TeacherNo = '%s'" % res[6]
		cur.execute(sqlcmd)
		TeacherName = cur.fetchone()
		cur.close()
		
		self.width   = 150
		self.conn    = conn
		self.account = account
		self.Password= passwd
		self.Name    = res[0]
		self.Gender  = res[1]
		self.Birth   = res[2]
		self.Accademy= res[3]
		self.Major	 = res[4]
		self.Grade	 = res[5]
		self.Teacher = TeacherName[0]
		
	def MainFunc(self):
		###主要执行函数
		info = ''
		while True:
			self.MainSurface(info)
			choice = input('What to do?')
			choice = choice.upper()
			if choice != 'P' and choice != 'M' and choice != 'Q':
				info = 'Error Action!'
				continue
			if choice == 'P':
				info = self.PersonalInfo()
			elif choice == 'M':
				info = self.OperatMessage()
			else : break
			
	def PersonalInfo(self):
		###个人信息
		info = ''
		while True:
			self.PersonalInfoSurface(info)
			choice = input('What to do?')
			choice = choice.upper()
			if choice != 'C' and choice != 'Q':
				info = 'Error Action!'
				continue
			if choice == 'C':
				info = self.ChangePersonalInfo()
			else : break
		return info
			
	def ChangePersonalInfo(self):
		###修改个人信息
		NewGender = self.Gender
		NewBirth = self.Birth
		NewPw = self.Password
		while True:
			choice = input('Change Gender?(y/n)')
			choice = choice.lower()
			if choice == 'y':
				NewGender = input('New Gender:')
				break
			elif choice == 'n': break
			else : pass
		while True:
			choice = input('change Born Date?(y/n)')
			choice = choice.lower()
			if choice == 'y':
				NewBirth = input('New Born Date:')
				break
			elif choice == 'n': break
			else : pass
		while True:
			choice = input('change Password?(y/n)')
			choice = choice.lower()
			if choice == 'y':
				NewPw = input('New Password:')
				break
			elif choice == 'n': break
			else : pass
		info = 'Change Success!'
		cur = self.conn.cursor()
		if NewGender != self.Gender or NewBirth != self.Birth:
			sqlcmd = "update StudentInfo set Gender = '%s',Birth = '%s' where StudentNo = '%s'" % (NewGender,NewBirth,self.account)
			if cur.execute(sqlcmd) == 0:
				self.conn.rollback()
				cur.close()
				return 'Change Fail!'
		if NewPw != self.Password:
			sqlcmd = "update LoginAccount set Password = '%s' where Account='%s'" % (NewPw,self.account)
			if cur.execute(sqlcmd) == 0:
				self.conn.rollback()
				cur.close()
				return 'Change Fail!'
			else :
				self.conn.commit()
		self.Gender = NewGender
		self.Birth = NewBirth
		self.Password = NewPw
		cur.close()
		return 'Change Success!'
	
	def OperatMessage(self):
		info = ''
		while True:
			self.MessageSurface(info)
			self.MessageList()
			choice =  input('What to do?')
			choice = choice.upper()
			if choice == 'M':
				msg = input('Message Id:')
				info = self.MessageInfo(msg)
			elif choice == 'Q': break;
			else : info = 'Error Action!'
		return info
			
	def	MessageList(self):
		###查看消息列表
		cur = self.conn.cursor()
		print ('')
		sqlcmd = "select Id,SenderName,SendTime,Title from AllMessage where statu = 'pass' and MsgLevel = 1"
		if cur.execute(sqlcmd) == 0:  return 
		print ('-' * self.width)
		while True:
			temp = cur.fetchone()
			if not temp: break;
			print( '%3d%-20s%-50s%s' % (temp[0],temp[1],temp[3],temp[2]))
			print( '-' * self.width)
		cur.close()
		
	def MessageInfo(self,MsgNo):
		###查看详细消息, No消息编号
		cur = self.conn.cursor()
		sqlcmd = "select SenderName,SendTime,Title,Content from AllMessage where Id = %d" % MsgNo
		if cur.execute(sqlcmd) == 0:
			cur.close()
			return 'Read Fail!'
		article = cur.fetchone()
		cur.close()
		os.system('cls')
		print ('=' * self.width)
		print (' ' * ((self.width - len(article[2]))/2) , article[2])
		head = article[0] + '     ' + str(article[1])
		print (' ' * ((self.width - len(head))/2) , head)
		print ('-' * self.width)
		print (article[3])
		print ('=' * self.width)
		input('Press any key to return!')
		return ''
		
	def Quit(self):
		###退出
		pass
		
	def MainSurface(self,info):
		###主界面
		os.system('cls')
		print ('=' * self.width)
		title = 'Welcome %s!' % self.Name
		body1 = '[P]Personal Information'
		body2 = '[M]Message'
		body3 = '[Q]Quit'
		print (' ' * ((self.width - len(title))/2),title)
		print (' ' * ((self.width - len(body1))/2),body1)
		print (' ' * ((self.width - len(body1))/2),body2)
		print (' ' * ((self.width - len(body1))/2),body3)
		print (' ' * ((self.width - len(info))/2),info)
		print ('=' * self.width)
		
	def MessageSurface(self,info):
		###消息界面
		os.system('cls')
		print ('=' * self.width)
		title = 'MESSAGES'
		body1 = '[M]Message Detail'
		body2 = '[Q]Quit'
		print (' ' * ((self.width - len(title))/2),title)
		print (' ' * ((self.width - len(body1))/2),body1)
		print (' ' * ((self.width - len(body1))/2),body2)
		print (' ' * ((self.width - len(info))/2),info)
		print( '=' * self.width)
		
	def PersonalInfoSurface(self,info):
		###个人信息界面
		os.system('cls')
		print('=' * self.width)
		title = 'PERSONAL INFORMATION'
		body1 = '[C]Change Information'
		body2 = '[Q]Quit'
		print (' ' * ((self.width - len(title))/2),title)
		print (' ' * ((self.width - len(body1))/2),body1)
		print (' ' * ((self.width - len(body1))/2),body2)
		print (' ' * ((self.width - len(info))/2),info)
		print( '-' * self.width)
		body3 = '          Name: %s' % self.Name
		body4 = 'Student Number: %s' % self.account
		body5 = '        Gender: %s' % self.Gender
		body6 = '         Birth: %s' % self.Birth
		body7 = '      Accademy: %s' % self.Accademy
		body8 = '         Major: %s' % self.Major
		body9 = '         Grade: %s' % self.Grade
		body10= '       Teacher: %s' % self.Teacher
		print (' ' * ((self.width - len(body6))/2),body3)
		print (' ' * ((self.width - len(body6))/2),body4)
		print (' ' * ((self.width - len(body6))/2),body5)
		print (' ' * ((self.width - len(body6))/2),body6)
		print (' ' * ((self.width - len(body6))/2),body7)
		print (' ' * ((self.width - len(body6))/2),body8)
		print (' ' * ((self.width - len(body6))/2),body9)
		print (' ' * ((self.width - len(body6))/2),body10)
		print ('=' * self.width)
		
if __name__ == '__main__':
	conn = pymysql.connect(user='root',passwd = 'zz1zz3zz2',db = 'db_educationalmanagementsystem')
	stu = Student(conn,'0000001','123456')
	stu.MainFunc()
	conn.close()
