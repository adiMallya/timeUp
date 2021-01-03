import numpy as np
import random
# from dataclasses import dataclass


class Subject:  #Class that represents each subject
    def __init__(self, subname=0, id=0):                 #contructor
        self.countw = 0                 #number of periods of that subject in a week
        self.countd = np.zeros(6)       #number of periods per day, array of 6, cause 6 days
        self.id = id                 #subject ID
        self.name = subname

class Teacher:
    def __init__(self, id, wrkhrs):
        self.tmat = np.zeros([6, 7])
        self.countd = np.zeros(6)
        self.countw = 0
        self.id = id        #ID is passed as argument
        self.maxcountw = wrkhrs
        self.maxcountd = wrkhrs / 5
        self.sec_sub = {}                           #DIctionary that holds section id as key and subject id as value
        self.sec_id = []                              #List of sections they take class for
        self.sub = [Subject() for i in range(10)]     #object of type class Subject

    def print(self):
        print(self.tmat)


class Section:
    labmat = np.zeros([3, 6, 7])
    elcmat = np.zeros([3, 6, 7])
    subname: str
    labname: str

    def __init__(self, id, sublist, maxsubcount, subname):
        #self.sub = [Subject() for i in range(len(sublist))]          #Object of type class Subject
        self.sub = []
        self.id = id
        self.labcount = 3
        self.subcount = 4
        self.subcountw = [5 for i in range(len(sublist))]
        for i in range(len(sublist)):
            self.sub.append(Subject(subname[i],sublist[i]))
        self.mat = np.zeros([6, 7])
        self.mat_str = [[None for _ in range(7)] for _ in range(6)]
        self.sub_theo = []
        self.offset = 2
        if self.id == '3A' or self.id == '3B' or self.id == '3C':
            self.lab_sem = 0
        elif self.id == '5A' or self.id == '5B' or self.id == '5C':
            self.lab_sem = 1
        elif self.id == '7A' or self.id == '7B' or self.id == '7C':
            self.lab_sem = 2
            self.offset = 3
        for i in range(len(sublist) - self.offset):
            self.sub_theo.append(sublist)

        #self.tch = tch_list                              #List of teachers taking class for the section
        self.batch = np.zeros(3)

        #print("Allocated Ection ID", self.id)
        self.subname = subname
        self.subcount = len(sublist) - self.offset #Number of periods the section has
        self.elcindex = [0,0]
        for i in range(len(self.sub)):
            if self.sub[i].id == 50:
                self.labindex = i
                # print(self.labindex)
            if self.sub[i].id == 100:
                self.elcindex[0] = i
            if self.sub[i].id == 200:
                self.elcindex[1] = i

        for i in range(len(maxsubcount)): #Allocating number of periods per week
            if maxsubcount[i] > 40:
                self.subcountw[i] = 5
            else:
                self.subcountw[i] = 3
        for i in range(len(sublist)):
            #print(i)
            self.sub[i].id = sublist[i]                            #Assigning subject ID, probably remove later
        z = 0
        for i in range(3):
            while True:
                x = random.randint(1, 3)
                for y in range(3):
                    if self.batch[y] == x:
                        x = 0
                        break
                if x != 0:
                    break
            self.batch[z] = x
            z = z + 1

    def print(self):
        print(self.mat)

    def print_name(self):
        for i in range(len(self.mat_str)):
            print(self.mat_str[i])

    def lab_allocater(self):
        while self.sub[self.labindex].countw < self.labcount:
            i = random.randint(0, 5)
            for j in range(6):
                if i == 5 and j > 3:
                    continue
                if self.mat[i][j] == 0 and self.labmat[self.lab_sem][i][j] == 0 and self.sub[self.labindex].countw < self.labcount and j != 6 and j % 2 == 0 and \
                        self.sub[self.labindex].countd[i] < 2:
                    self.mat[i][j] = self.sub[self.labindex].id
                    self.mat_str[i][j] = self.sub[self.labindex].name
                    self.mat[i][j + 1] = self.sub[self.labindex].id
                    self.mat_str[i][j + 1] = self.sub[self.labindex].name
                    self.labmat[self.lab_sem][i][j] = self.sub[self.labindex].id
                    self.labmat[self.lab_sem][i][j + 1] = self.sub[self.labindex].id
                    self.sub[self.labindex].countw = self.sub[self.labindex].countw + 1
                    self.sub[self.labindex].countd[i] = self.sub[self.labindex].countd[i] + 1
                    i = random.randint(0, 5)

    def ele(self, no):
        #ele_tch = []    #List of teachers taking elective class
        flag = 0

        while self.sub[self.elcindex[no]].countw < 3:   #3 periods for elc in a week
            i = random.randint(0, 5)
            j = random.randint(0, 3)

            while self.elcmat[self.lab_sem][i][j] == 0 and self.labmat[self.lab_sem][i][j] == 0 and self.sub[self.elcindex[no]].countd[i] < 1:
                self.elcmat[self.lab_sem][i][j] = 1 + no
                self.mat[i][j] = self.sub[self.elcindex[no]].id
                self.mat_str[i][j] = self.sub[self.elcindex[no]].name
                self.sub[self.elcindex[no]].countw = self.sub[self.elcindex[no]].countw + 1
                self.sub[self.elcindex[no]].countd[i] = self.sub[self.elcindex[no]].countd[i] + 1

    def ele_allocator(self,no):
        for i in range(6):
            for j in range(7):
                if self.elcmat[self.lab_sem][i][j] == 1 and no == 0:
                    self.mat[i][j] = self.sub[self.elcindex[no]].id
                    self.mat_str[i][j] = self.sub[self.elcindex[no]].name
                    self.sub[self.elcindex[no]].countw = self.sub[self.elcindex[no]].countw + 1
                    self.sub[self.elcindex[no]].countd[i] = self.sub[self.elcindex[no]].countd[i] + 1
                if self.elcmat[self.lab_sem][i][j] == 2 and no == 1:
                    self.mat[i][j] = self.sub[self.elcindex[no]].id
                    self.mat_str[i][j] = self.sub[self.elcindex[no]].name
                    self.sub[self.elcindex[no]].countw = self.sub[self.elcindex[no]].countw + 1
                    self.sub[self.elcindex[no]].countd[i] = self.sub[self.elcindex[no]].countd[i] + 1

    def allocator(self):
        flag = 0
        cnt1 = 0
        cnt2 = 0
        cnt3 = 0
        while True:
            for i in range(self.subcount):
                if self.sub[i].countw < self.subcountw[i]:
                    flag = 0
                else:
                    flag += 1

            if flag == self.subcount:
                return
            k = random.randint(0, self.subcount - 1)
            if cnt3 > 6000:
                break

            for j in range(7):
                cnt2 = 0
                if cnt3 > 6000:
                    break
                for i in range(6):
                    if i == 5 and j > 3:
                        continue
                    if cnt2 > 1070:
                        break
                    cnt1 = 0

                    while self.mat[i][j] == 0 and cnt1 < 200:
                        for a in range(self.subcount):
                            if self.sub[a].countw == self.subcountw[a]:
                                flag += 1
                            else:
                                flag = 0
                            if flag == self.subcountw:
                                return
                        k = random.randint(0, self.subcount - 1)

                        if cnt1 > 200:
                            break
                        if self.sub[k].countw < self.subcountw[k] and self.sub[k].countd[i] < 2 and self.mat[i][j - 1] != self.sub[k].id:
                            #print("Allocating for subject id", self.sub[k].id,"Section",self.id)
                            self.mat[i][j] = self.sub[k].id
                            self.mat_str[i][j] = self.sub[k].name
                            #tch[t].tmat[i][j] = self.sub[k].id
                            self.sub[k].countw += 1
                            self.sub[k].countd[i] += 1
                            #tch[t].countd[i] += 1
                            #tch[t].countw += 1

                        cnt1 += 1
                        cnt2 += 1
                        cnt3 += 1


if __name__ == "__main__":
    pass 