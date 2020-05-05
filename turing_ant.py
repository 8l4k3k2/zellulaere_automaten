
class turing_ant(object):
    def __init__(self,array,i,j,dir_nr):
        if dir_nr==None:
            dir_nr=2
        self.array=array
        self.dir_nr=dir_nr #dir=['n','o','s','w'](himmelsrichtungen)
        self.i=i
        self.j=j
        self.len=len(self.array)


    def algorithm(self):
        if self.array[self.j][self.i]==0:
            self.changedir('R')
            self.array[self.j][self.i]=1
        else:
            self.changedir('L')
            self.array[self.j][self.i]=0

        if self.dir_nr==0: #north
            #print "go north"
            self.j-=1
        elif self.dir_nr==1: #east
            #print "go east"
            self.i+=1
        elif self.dir_nr==2: #south
            #print "go south"
            self.j+=1
        elif self.dir_nr==3: #west
            #print "go west"
            self.i-=1
        #print "position",self.i,self.j
        return self.array,self.i,self.j,self.dir_nr

    def changedir(self,LoR):
        if LoR=='L':
            self.dir_nr-=1
            if self.dir_nr<0:
                self.dir_nr+=4
        elif LoR=='R':
            self.dir_nr+=1
            if self.dir_nr>3:
                self.dir_nr-=4
    """
    def printarray(self):
        for i in range(self.len):
            print self.array[i]

a=[[0,0,0,0,0,0,0],
   [0,0,0,0,0,0,0],
   [0,0,0,0,0,0,0],
   [0,0,0,0,0,0,0],
   [0,0,0,0,0,0,0],
   [0,0,0,0,0,0,0],
   [0,0,0,0,0,0,0]]

#a[1][0]=1
b=turing_ant(a,3,3,None)
b.printarray()

import time
for i in range(10):
    time.sleep(2)
    b.algorithm()
    print b.dir_nr
    b.printarray()
"""
