#-*- coding: utf-8 -*-
####管理员账户

import pymysql
import time
import os

class SystemManager:
	def __init__(self,conn,account,pw):
		self.conn = conn
		self.width = 150
		self.account = account
		cur = self.conn.cursor()
		self.password= pw

	def MainFunc(self):
		info = ''
		while True:
			self.MainSurface(info)
			choice = input('What to do?')
			choice = choice.upper()
			if choice == 'T':
				self.OperatTeacher()
			elif choice == 'M':
				self.OperatMessage()
			elif choice == 'S':
				self.OperatStudent()
			elif choice == 'Q': break;
			else: info = 'Error Action!'
	
	def OperatTeacher(self):
		####操作教职工
		info = ''
		while True:
			self.TeacherInfoSurface(info)
			self.ScanTeacherInfo()
			print ('-' * self.width)
			choice = input('What to do?')
			choice = choice.upper()
			if choice == 'R':
				info = self.RegTeacher()
			elif choice == 'C':
				info = self.ChangeTeacherInfo()
			elif choice == 'I':
				info = self.InitTeacherPassword()
			elif choice == 'D':
				info = self.DeleteTeacher()
			elif choice == 'Q': break
			else: info = 'Error Acction!'
			
	def ScanTeacherInfo(self):
		####浏览教职工消息
		cur = self.conn.cursor()
		sqlcmd = "select T.Id,T.Name,T.TeacherNo,T.Gender,T.Birth,P.PositionName,T.Salary from TeacherInfo T,PositionList P where T.PositionNo = P.PositionNo"
		cur.execute(sqlcmd)
		print ('%3s|%20s|%12s|%8s|%15s|%15s|%15s' % ('Id','Name','TeacherNo','Gender','BornDate','Position','Salary'))
		while True:
			res = cur.fetchone()
			if not res: break
			print ('%3d|%20s|%12s|%8s|%15s|%15s|%15.2f' % (res[0],res[1],res[2],res[3],res[4],res[5],res[6]))
		print ('-' * self.width)
		cur.close()
	def RegTeacher(self):
		####注册教职工
		cur = self.conn.cursor()
		print ('')
		title = '    Register New Teacher'
		print (title )
		name   = input('           Name:')
		number = input(' Teacher Number:')
		gender = input('         Gender:')
		birth  = input('      Born Date:')
		pos = self.PrintPositionInfo()
		position=input('Position Number:')
		salary = input('         Salary:')
		sqlcmd = "insert into TeacherInfo(Name,TeacherNo,Gender,Birth,PositionNo,Salary) values('%s','%s','%s','%s',%d,%f)" % (name,number,gender,birth,position,salary)
		res = cur.execute(sqlcmd)
		info = 'Register Success!'
		if res == 0: 
			info = 'Register Fail!'
			self.conn.rollback()
		else :
			sqlcmd = 'select Password from DefaultPassword where AccountLevel = 1'
			if cur.execute(sqlcmd) == 0:
				info = 'Register Fail!'
				self.conn.rollback()
			else :
				pw = cur.fetchone()
				sqlcmd = "insert into LoginAccount(Account,Password,AccountLevel) values('%s','%s',1)" % (number,pw[0])
				if cur.execute(sqlcmd) == 0:
					info = 'Register Fail!'
					self.conn.rollback()
				else :
					self.conn.commit()
		cur.close()
		return info
	def ChangeTeacherInfo(self):
		####修改教职工信息
		cur = self.conn.cursor()
		print ('')
		title = '     Change Teacher Information'
		print (title)
		teacherNo = input('TeacherNo:')
		sqlcmd = "select Name,TeacherNo,Gender,Birth,PositionNo,Salary from TeacherInfo where TeacherNo = '%s'" % teacherNo
		res = cur.execute(sqlcmd)
		info = 'Change Success!'
		if res == 0:
			info = 'Cannot find this teacher'
		else :
			temp = cur.fetchone()
			print ('old information: %s %s %s %s %d %.2f' % (temp[0],temp[1],temp[2],temp[3],temp[4],temp[5]))
			name   = input('           Name:')
			number = input(' Teacher Number:')
			gender = input('         Gender:')
			birth  = input('      Born Date:')
			self.PrintPositionInfo()
			position=input('Position Number:')
			salary = input('         Salary:')
			sqlcmd = "update TeacherInfo Set Name='%s',TeacherNo='%s',Gender='%s',Birth='%s',PositionNo=%d,Salary=%.2f where TeacherNo = '%s'" % (name,number,gender,birth,position,salary,teacherNo)
			res = cur.execute(sqlcmd)
			if res == 0:
				info = 'Change Fail!'
				self.conn.rollback()
			else :
				if number != temp[1]:
					sqlcmd = "update LoginAccount set Account='%s' where Account='%s'" %(number,temp[1])
					if cur.execute(sqlcmd) == 0:
						info = 'Change Fail!'
						self.conn.rollback()
					else :
						self.conn.commit()
				else :
					self.conn.commit()
		cur.close()
		return info
	def InitTeacherPassword(self):
		####初始化教职工密码
		cur = self.conn.cursor()
		sqlcmd = 'select Password from DefaultPassword where AccountLevel = 1'
		info = 'Initial Success!'
		if cur.execute(sqlcmd) == 0: 
			info = 'Initial Fail'
			self.conn.rollback()
		else:
			newPw = cur.fetchone()
			if not newPw: 
				info = 'Initial Fail'
				self.conn.rollback()
			else:
				teacherNo = input('Teacher Number:')
				sqlcmd = "select Password from LoginAccount where Account = '%s'" % teacherNo
				if 0 == cur.execute(sqlcmd):
					info = 'Initial Fail'
					self.conn.rollback()
				else :
					oldPw = cur.fetchone()
					if oldPw[0] != newPw[0]:
						sqlcmd = "update LoginAccount set Password='%s' where Account = '%s'" %(newPw[0],teacherNo)
						if cur.execute(sqlcmd) == 0:
							info = 'Initial Fail'	
							self.conn.rollback()
						else: 
							self.conn.commit()
		cur.close()
		return info
	def	DeleteTeacher(self):
		####删除教职工信息
		cur = self.conn.cursor()
		print('    Delete Teacher')
		teacherNo = input('Teacher Number:')
		sqlcmd = "delete from TeacherInfo where TeacherNo = '%s'" % teacherNo
		res = cur.execute(sqlcmd)
		info = 'Delete Success!'
		if res == 0:
			info = 'Delete Fail!'
			self.conn.rollback()
		else :
			sqlcmd = "delete from LoginAccount where Account = '%s'" % teacherNo
			res = cur.execute(sqlcmd)
			if res == 0: 
				info = 'Delete Fail!'
				self.conn.rollback()
			else : self.conn.commit()
		cur.close()
		return info
	def PrintPositionInfo(self):
		cur = self.conn.cursor()
		cur.execute('select PositionNo,PositionName from PositionList')
		pos = []
		while True:
			tp = cur.fetchone()
			if not tp: break;
			pos.append(tp)
		print( ' '*10,'-'*30)
		print( ' '*10 ,'POSTIONS')
		print (' '*10,'-'*30)
		it = pos.__iter__()
		while True:
			try:
				temp = it.next()
				print (' ' * 10, temp[0],' : ',temp[1])
			except:
				break;
		print (' '*10,'-'*30	)
		cur.close()
	
	def OperatStudent(self):
		####操作学生
		info = ''
		while True:
			self.StudentInfoSurface(info)
			self.ScanStudentInfo()
			print ('-' * self.width)
			choice = input('What to do?')
			choice = choice.upper()
			if choice == 'R':
				info = self.RegStudent()
			elif choice == 'C':
				info = self.ChangeStudentInfo()
			elif choice == 'I':
				info = self.InitStudentPassword()
			elif choice == 'D':
				info = self.DeleteStudent()
			elif choice == 'Q': break;
			else: info = 'Error Acction!'
			
	def ScanStudentInfo(self):
		####浏览学生消息
		cur = self.conn.cursor()
		sqlcmd = "select S.Id,S.Name,S.StudentNo,S.Gender,S.Birth,S.Grade,S.Academy,S.Major,T.Name from StudentInfo S,TeacherInfo T where S.TeacherNo = T.TeacherNo"
		cur.execute(sqlcmd)
		print ('%3s|%20s|%15s|%8s|%15s|%5s|%20s|%20s|%20s' % ('Id','Name','Student Number','Gender','Born Date','Grade','Academy','Major','Teacher'))
		while True:
			res = cur.fetchone()
			if not res: break
			print ('%3d|%20s|%15s|%8s|%15s|%5s|%20s|%20s|%20s' % (res[0],res[1],res[2],res[3],res[4],res[5],res[6],res[7],res[8]))
		print ('-' * self.width)
		cur.close()
		
	def RegStudent(self):
		####注册学生
		cur = self.conn.cursor()
		print( '')
		title = '    Register New Student'
		print (title )
		name   = input('          Name:')
		number = input('Student number:')
		gender = input('        Gender:')
		birth  = input('     Born Date:')
		grade  = input('         Grade:')
		academy= input('       Academy:')
		major  = input('         Major:')
		teacher= input('Teacher Number:')
		sqlcmd = "insert into StudentInfo(Name,StudentNo,Gender,Birth,Grade,Academy,Major,TeacherNo) values('%s','%s','%s','%s','%s','%s','%s','%s')" % (name,number,gender,birth,grade,academy,major,teacher)
		res = cur.execute(sqlcmd)
		info = 'Register Success!'
		if res == 0: 
			info = 'Register Fail!'
			self.conn.rollback()
		else :
			sqlcmd = 'select Password from DefaultPassword where AccountLevel = 2'
			if cur.execute(sqlcmd) == 0:
				info = 'Register Fail!'
				self.conn.rollback()
			else :
				pw = cur.fetchone()
				sqlcmd = "insert into LoginAccount(Account,Password,AccountLevel) values('%s','%s',2)" % (number,pw[0])
				if cur.execute(sqlcmd) == 0:
					info = 'Register Fail!'
					self.conn.rollback()
				else :
					self.conn.commit()
		cur.close()
		return info
	def ChangeStudentInfo(self,):
		####修改学生信息
		cur = self.conn.cursor()
		print ('')
		title = '     Change Student Information'
		print (title)
		studentNo = input('Student Number:')
		sqlcmd = "select Name,StudentNo,Gender,Birth,Grade,Academy,Major,TeacherNo from StudentInfo where StudentNo = '%s'" % studentNo
		res = cur.execute(sqlcmd)
		info = 'Change Success!'
		if res == 0:
			info = 'Cannot find this student'
		else :
			temp = cur.fetchone()
			print ('old information: |%s| |%s| |%s| |%s| |%s| |%s| |%s| |%s|' % (temp[0],temp[1],temp[2],temp[3],temp[4],temp[5],temp[6],temp[7]))
			name   = input('          Name:')
			number = input('Student Number:')
			gender = input('        Gender:')
			birth  = input('     Born Date:')
			grade  = input('         Grade:')
			academy= input('       Academy:')
			major  = input('         Major:')
			teacher= input('Teacher Number:')
			sqlcmd = "update StudentInfo Set Name='%s',StudentNo='%s',Gender='%s',Birth='%s',Grade='%s',Academy='%s',Major='%s',TeacherNo='%s' where StudentNo = '%s'" % (name,number,gender,birth,grade,academy,major,teacher,studentNo)
			if cur.execute(sqlcmd) == 0:
				info = 'Change Fail!'
				self.conn.rollback()
			else :
				if number != temp[1]:
					sqlcmd = "update LoginAccount set Account='%s' where Account='%s'" %(number,temp[1])
					if cur.execute(sqlcmd) == 0:
						info = 'Change Fail!'
						self.conn.rollback()
					else :
						self.conn.commit()
				else :
					self.conn.commit()
		cur.close()
		return info
		
	def InitStudentPassword(self):
		####初始化学生密码
		cur = self.conn.cursor()
		sqlcmd = 'select Password from DefaultPassword where AccountLevel = 2'
		info = 'Initial Success!'
		if cur.execute(sqlcmd) == 0: 
			info = 'Initial Fail'
			self.conn.rollback()
		else:
			newPw = cur.fetchone()
			if not newPw: 
				info = 'Initial Fail'
				self.conn.rollback()
			else:
				studentNo = input('Student Number:')
				sqlcmd = "select Password from LoginAccount where Account = '%s'" % studentNo
				cur.execute(sqlcmd)
				oldPw = cur.fetchone()
				if oldPw[0] != newPw[0]:
					sqlcmd = "update LoginAccount set Password='%s' where Account = '%s'" %(newPw[0],studentNo)
					if cur.execute(sqlcmd) == 0:
						info = 'Initial Fail'	
						self.conn.rollback()
					else: 
						self.conn.commit()
		cur.close()
		return info
		
	def	DeleteStudent(self,):
		####删除学生信息
		cur = self.conn.cursor()
		print ('    Delete Student')
		studentNo = input('Student Number:')
		sqlcmd = "delete from StudentInfo where StudentNo = '%s'" % studentNo
		res = cur.execute(sqlcmd)
		info = 'Delete Success!'
		if res == 0:
			info = 'Delete Fail!'
			self.conn.rollback()
		else :
			sqlcmd = "delete from LoginAccount where Account = '%s'" % studentNo
			res = cur.execute(sqlcmd)
			if res == 0: 
				info = 'Delete Fail!'
				self.conn.rollback()
			else : self.conn.commit()
		cur.close()
		return info
		
	def OperatMessage(self):
		####操作消息
		info = ''
		while True:
			self.MessageSurface(info)
			self.MessageList()
			choice =  input('What to do?')
			choice = choice.upper()
			if choice == 'D':
				info = self.DeleteMessage()
			elif choice == 'P':
				info = self.CreateMessage()
			elif choice == 'C':
				info = self.CheckMessage()
			elif choice == 'M':
				msg = input('Message Id:')
				info = self.MessageInfo(msg)
			elif choice == 'Q': break
			else : info = 'Error Action!'
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
		print( ' ' * ((self.width - len(head))/2) , head)
		print ('-' * self.width)
		print (article[3])
		print ('=' * self.width)
		input('Press any key to return!')
		return ''
		
	def MessageList(self):
		####查看消息列表
		cur = self.conn.cursor()
		print ('')
		sqlcmd = "select Id,SenderName,SendTime,Title from AllMessage where statu = 'pass'"
		if cur.execute(sqlcmd) == 0:  return 
		print ('-' * self.width)
		while True:
			temp = cur.fetchone()
			if not temp: break;
			print ('%3d%-20s%-50s%s' % (temp[0],temp[1],temp[3],temp[2]))
			print ('-' * self.width)
		cur.close()
		
	def CreateMessage(self):
		####发布消息
		print ('')
		print ('    Publish Messsage')
		title = input('Message Title:')
		path  = input('Message Path:')
		fp = open(path,'r')
		body = fp.read()
		fp.close()
		sqlcmd = "insert into AllMessage(MsgLevel,SenderNo,SenderName,SendTime,Title,Content,statu) values(0,'%s','Admin',now(),'%s','%s','pass')" % (self.account,title,body)
		cur = self.conn.cursor()
		info = 'Publish Success!'
		if 0 == cur.execute(sqlcmd):
			info = 'Publish Fail'
			self.conn.rollback()
		else:
			self.conn.commit()
		cur.close()
		return info
		
	def DeleteMessage(self):
		####删除消息
		print ('')
		print ('    Delete Message')
		MsgNo = input('Message id = ')
		cur = self.conn.cursor()
		sqlcmd = "delete from AllMessage where Id = %d" % MsgNo
		info = 'Delete Success!'
		if cur.execute(sqlcmd) == 0:
			info = 'Delete Fail'
			self.conn.rollback()
		else :
			self.conn.commit()
		cur.close()
		return info
		
	def CheckMessage(self):
		####审核消息
		cur = self.conn.cursor()
		MsgCount = cur.execute("select Id,SenderNo,SenderName,SendTime,Title,Content from AllMessage where statu = 'wait'")
		info = 'All Messages Were Checked!'
		MsgInfo = 'You have %d messages need to check!' % MsgCount
		while MsgCount > 0:
			self.WaitMessageSurface(MsgInfo)
			msg = cur.fetchone()
			print (' ' * ((self.width - len(msg[4]))/2),msg[4])
			print ('Sender Name:',msg[2], '     Sender Number:',msg[1], '   Time:',msg[3])
			print (msg[5])
			print ('-' * self.width)
			choice = input('What to do?')
			choice = choice.upper()
			MsgCount -= 1
			MsgInfo = 'You have %d messages need to check!' % MsgCount
			if choice == 'I':
				continue
			elif choice == 'P':
				sqlcmd = "update AllMessage set statu = 'pass' where Id = %d" % msg[0]
				if cur.execute(sqlcmd)  == 0:
					MsgInfo = 'Check Fail!'
					self.conn.rollback()
				else: self.conn.commit()
			elif choice == 'F':
				sqlcmd = "update AllMessage set statu = 'fail' where Id = %d" % msg[0]
				if cur.execute(sqlcmd)  == 0:
					MsgInfo = 'Check Fail!'
					self.conn.rollback()
				else: self.conn.commit()
			elif choice == 'Q': break;
			else : info = 'Error Action!'
		cur.close()
		if MsgCount != 0:
			info = 'Still have %d Messages wait for dealing!' % MsgCount
		return info
		
	def MainSurface(self,info):
		#####主界面
		os.system('cls')
		title = 'Welcome, Administor!'
		body1 = '[T]Teachers Information'
		body2 = '[S]Students Information'
		body3 = '[M]Message  Information'
		body4 = '[Q]Quit'
		print ('=' * self.width)
		print (' ' * ((self.width-len(title))/2),title)
		print (' ' * ((self.width-len(body1))/2),body1)
		print (' ' * ((self.width-len(body1))/2),body2)
		print (' ' * ((self.width-len(body1))/2),body3)
		print (' ' * ((self.width-len(body1))/2),body4)
		print (' ' * ((self.width-len(info))/2),info)
		print ('=' * self.width)
		
	def StudentInfoSurface(self,info):
		####学生信息界面
		os.system('cls')
		title = 'STUDENT LIST'
		body1 = '[R]Register New Student'
		body2 = '[C]Change Student Information'
		body3 = '[I]Initial Student Password'
		body4 = '[D]Delete Student Information'
		body5 = '[Q]Quit'
		print('=' * self.width)
		print(' ' * ((self.width - len(title)) / 2), title)
		print(' ' * ((self.width - len(body1)) / 2), body1)
		print(' ' * ((self.width - len(body1)) / 2), body2)
		print(' ' * ((self.width - len(body1)) / 2), body3)
		print(' ' * ((self.width - len(body1)) / 2), body4)
		print(' ' * ((self.width - len(body1)) / 2), body5)
		print(' ' * ((self.width - len(info)) / 2), info)
		print('=' * self.width)
		
	def TeacherInfoSurface(self,info):
		####教职工信息界面
		os.system('cls')
		title = 'TEACHER LIST'
		body1 = '[R]Register New Teacher'
		body2 = '[C]Change Teacher Information'
		body3 = '[I]Initial Teacher Password'
		body4 = '[D]Delete Teacher Information'
		body5 = '[Q]Quit'
		print ('=' * self.width)
		print (' ' * ((self.width-len(title))/2),title)
		print (' ' * ((self.width-len(body1))/2),body1)
		print (' ' * ((self.width-len(body1))/2),body2)
		print (' ' * ((self.width-len(body1))/2),body3)
		print (' ' * ((self.width-len(body1))/2),body4)
		print (' ' * ((self.width-len(body1))/2),body5)
		print (' ' * ((self.width-len(info))/2),info)
		print ('=' * self.width)
		
	def MessageSurface(self,info):
		####消息列表界面
		os.system('cls')
		title = 'MESSAGE LIST'
		body1 = '[P]Publish Message'
		body2 = '[C]Check   Message'
		body3 = '[D]Delete  Message'
		body4 = '[M]Message Detail'
		body5 = '[Q]Quit'
		print ('=' * self.width)
		print (' ' * ((self.width-len(title))/2),title)
		print (' ' * ((self.width-len(body1))/2),body1)
		print (' ' * ((self.width-len(body1))/2),body2)
		print (' ' * ((self.width-len(body1))/2),body3)
		print (' ' * ((self.width-len(body1))/2),body4)
		print (' ' * ((self.width-len(body1))/2),body5)
		print (' ' * ((self.width-len(info))/2),info)
		print ('=' * self.width)
	def WaitMessageSurface(self,info):
		####审核消息界面
		os.system('cls')
		title = 'CHECK MESSAGE'
		body1 = '[I]Ignore'
		body2 = '[P]Pass'
		body3 = '[F]Fail'
		body4 = '[Q]Quit'
		print ('=' * self.width)
		print (' ' * ((self.width-len(title))/2),title)
		print (' ' * ((self.width-len(body1))/2),body1)
		print (' ' * ((self.width-len(body1))/2),body2)
		print (' ' * ((self.width-len(body1))/2),body3)
		print (' ' * ((self.width-len(body1))/2),body4)
		print (' ' * ((self.width-len(info))/2),info)
		print ('=' * self.width)

if __name__ == '__main__':
	conn = pymysql.connect(user = 'root',passwd = '',db = 'DB_EducationalManagementSystem');
	sm = SystemManager(conn,'123','123456')
	sm.MainFunc()
	conn.close()