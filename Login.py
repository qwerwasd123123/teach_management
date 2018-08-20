# -*- coding:utf-8 -*-
#####系统登录

import os
import pymysql
import time


class Login:
    def __init__(self, conn):
        self.account = ''
        self.password = ''
        self.level = 2
        self.conn = conn

    def LoginSurface(self, info):
        os.system('cls')

        width = 50
        title = 'LOGIN'
        body1 = '[A]Admin'
        body2 = '[T]Teacher'
        body3 = '[S]Student'
        body4 = '[Q]Quit'
        print('=' * width)
        print(' ' * ((width - len(title)) / 2), title)
        print(' ' * ((width - len(body1)) / 2), body1)
        print(' ' * ((width - len(body1)) / 2), body2)
        print( ' ' * ((width - len(body1)) / 2), body3)
        print(' ' * ((width - len(body1)) / 2), body4)
        print(' ' * ((width - len(info)) / 2), info)
        print('-' * width)


    def MainFunc(self):
        err = ''
        while True:
            self.LoginSurface(err)
            level = raw_input('Access:')
            level = level.upper()
            if level == 'A':
                    self.level = 0
            elif level == 'T':
                    self.level = 1
            elif level == 'S':
                    self.level = 2
            elif level == 'Q':
                    return False
            else:
                err = 'Error Action!'
                continue
                self.account = input('Account:')
                self.password = input('Password:')
                if self.CheckAccount():
                    err = 'Login Success!'
                    self.LoginSurface(err)
                    print('Please wait...')
                    time.sleep(3)
                    return True;
                else:
                    err = 'Login Failed!'

    def GetLoginAccount(self):
        return [self.account, self.password, self.level]

    def CheckAccount(self):
        cur = self.conn.cursor()

        sqlcmd = "select Account,Password,AccountLevel from LoginAccount where Account = '%s'" % self.account
        if cur.execute(sqlcmd) == 0: return False
        temp = cur.fetchone()
        cur.close()
        if temp[1] == self.password and temp[2] == self.level:
            return True
        else:
            return False

    def Quit(self):
        pass


        if __name__ == '__main__':
            conn = pymysql.connect(user='root', passwd='', db='DB_EducationalManagementSystem');
            a = Login(conn)
            a.MainFunc()
            a.Quit()
            conn.close()