#-*- coding:utf-8 -*-
####教师帐号

import os
import pymysql

class Teacher:
	def __init__(self,conn,account,passwd):
		cur = conn.cursor()
		sqlcmd = "select Name,TeacherNo,Gender,Birth,PositionNo,Salary from TeacherInfo where TeacherNo = '%s'" % account
		cur.execute(sqlcmd)
		temp = cur.fetchone()
		sqlcmd = "select PositionName from PositionList where PositionNo = '%s'" % temp[1]
		cur.execute(sqlcmd)
		pos = cur.fetchone()
		cur.close()
		
		self.PositionName = pos[0]
		self.width = 150
		self.conn = conn
		self.Name = temp[0]
		self.TeacherNo = temp[1]
		self.Gender = temp[2]
		self.Birth = temp[3]
		self.PositionNo = temp[4]
		self.Salary = temp[5]
		self.Password = passwd
	
	def MainFunc(self):
		####主要执行函数
		info = ''
		while True:
			self.MainSurface(info)
			choice = nput('What to do?')
			choice = choice.upper()
			if choice == 'P':
				info = self.OperatePersonalInfo()
			elif choice == 'M':
				info = self.OperateMessage()
			elif choice == 'Q': break
			else : info = 'Error Action'
	
	def OperatePersonalInfo(self):			
		####操作个人信息
		info = ''
		while True:
			self.PersonalInfoSurface(info)
			choice = input('What to do?')
			choice = choice.upper()
			if choice == 'C':
				info = self.ChangePersonalInfo()
			elif choice == 'Q': break
			else : info = 'Error Action'
		return info

	def	ChangePersonalInfo(self):
		####修改个人信息
		NewGender = self.Gender
		NewBirth  = self.Birth
		NewPw = self.Password
		cur = self.conn.cursor()
		while True:
			choice = input('Change Gender?(y/n)')
			choice = choice.lower()
			if choice == 'y':
				NewGender = input('New Gender:')
				break
			elif choice == 'n': break
			else : pass
		while True:
			choice = input('Change Born Data?(y/n)')
			choice = choice.lower()
			if choice == 'y':
				NewBirth = input('New Born Date:')
				break
			elif choice == 'n': break
			else : pass
		while True:
			choice = input('Change Password?(y/n)')
			choice = choice.lower()
			if choice == 'y':
				NewPw = input('New Password:')
				break
			elif choice == 'n': break
			else :pass
		if NewBirth != self.Birth or NewGender != self.Gender:
			sqlcmd = "update TeacherInfo set Birth='%s',Gender='%s' where TeacherNo = '%s'" % (NewBirth,NewGender,self.TeacherNo)
			if 0 == cur.execute(sqlcmd):
				self.conn.rollback()
				cur.close()
				return 'Changer Fail'
		if NewPw != self.Password:
			sqlcmd = "update LoginAccount set Password='%s' where Account='%s'" % (NewPw,self.TeacherNo)
			if 0 == cur.execute(sqlcmd):
				self.conn.rollback()
				cur.close()
				return 'Change Fail!'
			else :
				self.conn.commit()
		self.Gender = NewGender
		self.Password = NewPw
		self.Birth = NewBirth
		cur.close()
		return 'Change Success!'
		
	def	MessageList(self):
		#####查看消息列表
		cur = self.conn.cursor()
		print ('')
		sqlcmd = "select Id,SenderName,SendTime,Title from AllMessage where statu = 'pass' and MsgLevel <= 1"
		if cur.execute(sqlcmd) == 0:  return 
		print ('-' * self.width)
		while True:
			temp = cur.fetchone()
			if not temp: break;
			print ('%3d%-20s%-50s%s' % (temp[0],temp[1],temp[3],temp[2]))
		cur.close()
		
	def MessageInfo(self,MsgNo):
		####查看详细消息, MsgNo消息编号
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
		
	def CreateMessage(self):
		####发布消息
		print ('')
		print ('    Publish Messsage')
		title = input('Message Title:')
		path  = input('Message Path:')
		fp = open(path,'r')
		body = fp.read()
		fp.close()
		sqlcmd = "insert into AllMessage(MsgLevel,SenderNo,SenderName,SendTime,Title,Content,statu) values(1,'%s','%s',now(),'%s','%s','wait')" % (self.TeacherNo,self.Name,title,body)
		cur = self.conn.cursor()
		info = 'Publish Success!'
		if 0 == cur.execute(sqlcmd):
			info = 'Publish Fail'
			self.conn.rollback()
		else:
			self.conn.commit()
		cur.close()
		return info
	def OperateMessage(self):
		#####管理消息
		info = ''
		while True:
			self.MessageSurface(info)
			self.MessageList()
			choice = input('What to do?')
			choice = choice.upper()
			if choice == 'P':
				info = self.CreateMessage()
			elif choice == 'Y':
				info = self.PersonalMessage()
			elif choice == 'M':
				msg = input('Message Id:')
				info = self.MessageInfo(msg)
			elif choice == 'Q': break
			else : info = 'Error Action'
		return info
	
	def PersonalMessageList(self):
		cur = self.conn.cursor()
		sqlcmd = "select Id,SenderName,SendTime,Title from AllMessage where SenderNo='%s'" % self.TeacherNo
		if cur.execute(sqlcmd) != 0:
			print ('-' * self.width)
			while True:
				temp = cur.fetchone()
				if not temp: break;
				print ('%3d%-20s%-50s%s' % (temp[0],temp[1],temp[3],temp[2]))
				print ('-' * self.width)
		cur.close()
		
	def PersonalMessage(self):
		#####查看个人消息
		info = ''
		while True:
			self.PersonalMessageSurface(info)
			self.PersonalMessageList()
			choice = input('What to do?')
			choice = choice.upper()
			if choice == 'M':
				msg = input('Message Id:')
				info = self.MessageInfo(msg)
			elif choice == 'D':
				info = self.DeleteMessage()
			elif choice == 'Q': break
			else : info = 'Error Action!'
		return info
			
	def DeleteMessage(self):
		####删除个人消息
		print ('')
		print ('    Delete Message')
		MsgNo = input('Message id = ')
		cur = self.conn.cursor()
		sqlcmd = "delete from AllMessage where Id = %d and SenderNo = '%s'" % (MsgNo,self.TeacherNo)
		info = 'Delete Success!'
		if cur.execute(sqlcmd) == 0:
			info = 'Delete Fail'
			self.conn.rollback()
		else :
			self.conn.commit()
		cur.close()
		return info
		
	def MainSurface(self,info):
		os.system('cls')
		####主界面
		title = "Welcome, %s" % self.Name
		body1 = '[P]Personal Information'
		body2 = '[M]Message Management'
		body3 = '[Q]Quit'
		print('=' * self.width)
		print(' ' * ((self.width - len(title)) / 2), title)
		print(' ' * ((self.width - len(body1)) / 2), body1)
		print(' ' * ((self.width - len(body1)) / 2), body2)
		print(' ' * ((self.width - len(body1)) / 2), body3)
		print(' ' * ((self.width - len(info)) / 2), info)
		print('=' * self.width)
	
	def PersonalInfoSurface(self,info):
		####个人信息界面
		os.system('cls')
		title = 'Personal Information'
		body1 = '[C]Change Information'
		body2 = '[Q]Quit'
		body3 = '     Name: %s' % self.Name
		body4 = '   Gender: %s' % self.Gender
		body5 = 'Born Date: %s' % self.Birth
		body6 = ' Position: %s' % self.PositionName
		body7 = '   Salary: %.2f' %self.Salary
		print ('=' * self.width)
		print (' ' * ((self.width - len(title))/2), title)
		print (' ' * ((self.width - len(body1))/2), body1)
		print (' ' * ((self.width - len(body1))/2), body2)
		print (' ' * ((self.width - len(info))/2), info)
		print ('-' * self.width)
		print( ' ' * ((self.width - len(body3))/2), body3)
		print (' ' * ((self.width - len(body3))/2), body4)
		print (' ' * ((self.width - len(body3))/2), body5)
		print (' ' * ((self.width - len(body3))/2), body6)
		print (' ' * ((self.width - len(body3))/2), body7)
		print ('=' * self.width)
		
	def MessageSurface(self,info):
		#####消息界面
		os.system('cls')
		title = 'MESSAGE'
		body1 = '[P]Publish Message'
		body2 = '[Y]Your Message'
		body3 = '[M]Message Detail'
		body4 = '[Q]Quit'
		print('=' * self.width)
		print(' ' * ((self.width - len(title)) / 2), title)
		print(' ' * ((self.width - len(body1)) / 2), body1)
		print(' ' * ((self.width - len(body1)) / 2), body2)
		print(' ' * ((self.width - len(body1)) / 2), body3)
		print (' ' * ((self.width - len(body1))/2), body4)
		print (' ' * ((self.width - len(info))/2), info)
		print ('=' * self.width)
		
	def PersonalMessageSurface(self,info):
		#####个人消息界面
		os.system('cls')
		title = 'PERSONAL MESSAGE'
		body1 = '[M]Message Detail'
		body2 = '[D]Delete Message'
		body3 = '[Q]Quit'
		print ('=' * self.width)
		print (' ' * ((self.width - len(title))/2), title)
		print (' ' * ((self.width - len(body1))/2), body1)
		print (' ' * ((self.width - len(body1))/2), body2)
		print (' ' * ((self.width - len(body1))/2), body3)
		print (' ' * ((self.width - len(info))/2), info)
		print ('=' * self.width)
		
if __name__ == '__main__':
	conn = pymysql.connect(user='root',passwd = '',db = 'db_educationalmanagementsystem')
	t = Teacher(conn,'00001','123456')
	t.MainFunc()
	conn.close()
		