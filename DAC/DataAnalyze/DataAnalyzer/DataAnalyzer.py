import matplotlib.pyplot as plt
import numpy as np
import os
import shutil
import copy

class raw_data:

    def __init__(self):
        self.array = []


    def clear(self):
        self.array = []

    def get(self,arr):
        self.array.append(arr)

    def cast_type(self,x,tp):
        if tp == "int" : 
            for d in self.array :
                d[x] = int(d[x])

        elif tp == "float" :
            for d in self.array : 
                d[x] = float(d[x])

    def multiply(self,ind,x):
        for d in self.array:
            d[ind] = d[ind] * x

    def operate(self,func,i):
        self.array[i] = func(self.array[i])


class data_2d:
    def __init__(self):
        self.data = []
        self.x = np.empty(0)
        self.y = np.empty(0)
        self.error = np.empty(0)
    
    def input_data(self,raw,x,y):
        for lis in raw.array:
            self.data.append((lis[x],lis[y]))

    def input_data_2d(self,x,y,err):
        self.x = np.append(self.x,x)
        self.y = np.append(self.y,y)
        self.error = np.append(self.error,err)

    def process_data(self):
        sorted_data = sorted(self.data)
        
        raw_data = []

        bvalue = -1
        ind = -1
        
        for key,val in sorted_data:
            if key != bvalue:
                ind = ind+1
                raw_data.append(np.empty(0))
                self.x = np.append(self.x,key)
                bvalue = key

            raw_data[ind] = np.append(raw_data[ind],val)

            

        for i in range(0,len(raw_data)):
            self.y = np.append(self.y, np.mean(raw_data[i]))
            self.error = np.append(self.error, max(np.std(raw_data[i]),0))
    def noprocess(self):
        for u,v in self.data:
            self.x = np.append(self.x,u)
            self.y = np.append(self.y,v)
        

    def export(self,path,separator):
        f = open(path,"w")
        for i in range(0,len(self.x)):
            f.write(str(self.x[i]) + separator + str(self.y[i]) + separator + str(self.error[i]) + "\n")
        f.close()
        print("writing data is done")




class graph_2d:

    def __init__(self):
        self.fig,self.ax = plt.subplots()
        self.plot_data =  []
        self.nd = 0
        self.datand = []
        self.xlabel = ""
        self.ylabel = ""
        self.legend = []
        self.color = []
        self.labelsize = 18
        self.legendsize = 6
        self.xticssize = 6
        self.yticssize = 6
        self.ticksize = 8

        self.legend_flag = False
        self.error_flag = False
    def input(self,data2d,legend,fm,colo=""):
        self.plot_data.append((data2d,legend,fm,colo))

    def set_xrange(self,lx):
        plt.xlim(lx)
    def set_yrange(self,ly):
        plt.ylim(ly)
    
    def set_label(self,lab):
        self.xlabel = lab[0]
        self.ylabel = lab[1]

    def set_legend(self):
        self.legend_flag = True
    def set_legendsize(self,fs):
        self.legendsize = fs

    def set_labelsize(self,size):
        self.labelsize = size

    def set_ticks_size(self,size):
        plt.tick_params(labelsize = size)

    def errorbar(self):
        self.error_flag = True

    def set_title(self,tit):
        self.ax.set_title(tit)

    def plot(self):

        self.ax.set_xlabel(self.xlabel,fontsize=self.labelsize)
        self.ax.set_ylabel(self.ylabel,fontsize=self.labelsize)

        self.fig.tight_layout()
        for dat,leg,fm,colo in self.plot_data:
            if fm == "plot":
                self.ax.plot(dat.x,dat.y,label=leg)
            elif fm == "scatter":
                if self.error_flag == False: 
                    self.ax.scatter(dat.x, dat.y,label = leg,marker='o',color=colo)
                else :
                    self.ax.errorbar(dat.x,dat.y,yerr = dat.error,label=leg,fmt='o',capsize=5,ecolor=colo,color=colo,linestyle="None")
            else :
                print("DataAnalyzer ERROR class graph_2d.show() : pass collect format of ploting")
        if self.legend_flag == True:
            self.ax.legend(fontsize = self.legendsize)
    
    def show(self):
        plt.show()

    def grid(self):
        plt.grid()


class set_graph_2d:
    def __init__(self,many = 1):
        self.graphs = []
        for i in range(0,many):
            self.graphs.append(graph_2d())

    def new(self):
        self.graphs.append(graph_2d())
    def input(self,idx,data2d,legend,fm,colo=""):
        self.graphs[idx].input(data2d,legend,fm,colo)

    def set_xrange(self,idx,lx):
        self.graphs[idx].set_xrange(lx)

    def set_yrange(self,idx,ly):
        self.graphs[idx].set_yrange(ly)
    
    def set_label(self,idx,lab):
        self.graphs[idx].set_label(lab)

    def set_legend(self,idx):
        self.graphs[idx].set_legend()

    def set_legendsize(self,idx,fs):
        self.graphs[idx].set_legendsize(fs)

    def set_labelsize(self,idx,size):
        self.graphs[idx].set_labelsize(size)

    def set_ticks_size(self,size):
        self.graphs[idx].set_labelsize(size)

    def errorbar(self):
        self.graphs[idx].errorbar()

    def plot(self,idx):
        self.graphs[idx].plot()

    def show(self):
        plt.show()

    def grid(self):
        plt.grid()



def readfile(f,raw,sep):
    str = myreadline(f)
    if str == "":
        return False
    if ("&" in str) == True :
        str = myreadline(f)
    while ("&" in str) == False :
        s = str.strip()
        s = s.replace("\n","")
        s = s.split(sep)
        raw.array.append(s)
        str = myreadline(f)
    return True


def myreadline(f):
    str = f.readline();
    while True :
        if str == "":
            break

        elif str[0] == "#" or str == '\n' : 
            str = f.readline()
            continue
        break


    return str


def Linear_Fitting(data2d,xlim):

    tmp2d = copy.deepcopy(data2d)
    x = np.empty(0)
    y = np.empty(0)
    err = np.empty(0)
    for i in range(0,len(data2d.x)):
        if xlim[0] < data2d.x[i] and data2d.x[i] < xlim[1]:
            x = np.append(x,data2d.x[i])
            y = np.append(y,data2d.y[i])
            err = np.append(err,data2d.x[i])

    p, cov = np.polyfit(x,y,1,w=1.0/err,cov=True)
    a = p[0]
    b = p[1]
    sigma_a = np.sqrt(cov[0,0])
    sigma_b = np.sqrt(cov[1,1])
    tmp2d.y = copy.deepcopy(np.polyval(p,tmp2d.x))
    return  tmp2d,a,b

