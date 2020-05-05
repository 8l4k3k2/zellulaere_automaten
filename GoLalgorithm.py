import copy
import time

class board(object):
    def __init__(self,array,rule="2G3"): #rules: '2G3', '26G3', 'G1357'
        self.rule=rule
        self.array=array
        self.len=len(array[0])
        self.array_2=copy.deepcopy(array)

    def getneighbour(self,i0,j0):
        neighbours=0
        for i in range(3):
            for j in range(3):
                ix=i0-1+i
                iy=j0-1+j
                if 0<=ix<=self.len-1 and 0<=iy<=self.len-1:
                    if i==1 and j==1:
                        pass
                    else:
                        if self.xornox(ix,iy):
                            neighbours+=1
        return neighbours

    def printarray(self):
        print(""),
        for p in range(self.len):
            print("___"),
        print 
        for i in range(self.len):
            l1=""
            l2=""
            for j in range(self.len):
                l1+="| "+str(self.array[i][j])+" "
                l2+="|___"
            l1+="|"
            l2+="|"
            print(l1)
            print(l2)

    def surviveornot(self,i0,j0):
        #gol standart
        if self.rule=="2G3":
            if 2==self.getneighbour(i0,j0) or 3==self.getneighbour(i0,j0):
                pass
            else:
                self.array_2[i0][j0]=0

        #gol modulo2/kopierwelt
        elif self.rule=='G1357':
            if self.getneighbour(i0,j0)%2==0:
                self.array_2[i0][j0]=0

        #236/3 regel
        elif self.rule=="26G3":
            if 2==self.getneighbour(i0,j0) or 3==self.getneighbour(i0,j0) or 6==self.getneighbour(i0,j0):
                pass
            else:
                self.array_2[i0][j0]=0

        ##rand der vernichtung
        #if i0==0 or j0==0 or j0==self.len or i0==self.len:
         #   self.array_2[i0][j0]=0


    def bornornot(self,i0,j0):
        #gol standart
        if self.rule=="2G3":
            if self.getneighbour(i0,j0)==3:
                self.array_2[i0][j0]=1

        #gol modulo 2
        elif self.rule=='G1357':
            if (self.getneighbour(i0,j0)+1)%2==0:
                self.array_2[i0][j0]=1

        #236/3 regel
        elif self.rule=="26G3":
            if self.getneighbour(i0,j0)==3:
                self.array_2[i0][j0]=1

        ##rand der vernichtung
        #if i0==0 or j0==0 or j0==self.len or i0==self.len:
         #   self.array_2[i0][j0]=0


    def xornox(self,i,j):
        return self.array[i][j]==1

    def algorithm(self):
        for i in range(self.len):
            for j in range(self.len):
                if self.xornox(i,j):
                    self.surviveornot(i,j)
                else:
                    self.bornornot(i,j)
        self.array=copy.deepcopy(self.array_2)
        return self.array
        
        
"""
a=[[0,1,0,0,0],
   [0,0,1,0,0],
   [1,1,1,0,0],
   [0,0,0,0,0],
   [0,0,0,0,0]]

#c=board(a)

#c.array[0][2]="d"
#print c.getneighbour(3,4)
#c.printarray()
#for i in range(20):
 #   x=c.algorithm()
"""