## LAMMPSの構造ファイルを調整するためのスクリプト
import sys
import random


class Position:
    def __init__(self):
        self.pos = [0.0, 0.0,0.0]
        self.bound = [0,0,0]

    def input_Position(self,val):
        self.pos = [float(val[2]),float(val[3]),float(val[4])]
        if len(val) > 5:
            self.bound = [int(val[5]),int(val[6]),int(val[7])]

class Velocity:
    def __init__(self):
        self.velo = [0.0, 0.0,0.0]

    def input_Velocity(self,val):
        self.velo = [float(val[1]),float(val[2]),float(val[3])]

class Atom:

    def __init__(self,pos,vel):
        self.type = -1
        self.posi  = pos
        self.velo = vel

    def input_Atomic(self,s):
        self.type = int(s[1])-1
        self.posi.input_Position(s)

    def input_Velocity(self,s):
        self.velo.input_Velocity(s)




class System:
    def __init__(self):
        self.na = 0
        self.nt = 0
        self.atoms = [] 
        self.masses = []
        self.x = [0.0,0.0]
        self.y = [0.0,0.0]
        self.z = [0.0,0.0]

    def getline(self,file):
        str = file.readline()
        str = str.rstrip('\n')
        return str


    def getlinewhile(self,file):
        cond = True
        while cond == True:
            str = f.readline()
            if str == "\n" :
                continue
            elif str == "":
                return ""
            else :
                str = str.rstrip('\n')
                return str

    def input_sysytem(self,file):
        file.readline()


        line = self.getlinewhile(file).split(" ")
        self.na = int(line[0])

        for i in range(0,self.na):
            self.atoms.append(Atom(Position(),Velocity()))


        line = self.getlinewhile(file).split(" ")
        self.nt = int(line[0])

        for i in range(0,self.nt):
            self.masses.append(0.0)


        line = self.getlinewhile(file).split(" ")
        self.x = [float(line[0]),float(line[1])]
        line = file.readline().split(" ")
        self.y = [float(line[0]),float(line[1])]
        line = file.readline().split(" ")
        self.z = [float(line[0]),float(line[1])]

        while True:
            line = self.getlinewhile(file)
            print(line)
            param = line.split(" ")
            if param[0] == "Atoms": 
                self.input_Atoms(file)
            elif param[0] == "Velocities":
                self.input_Velocity(file)
            elif param[0] == "Masses": 
                self.input_Masses(file)
            else:
                print("end")
                break

    def input_Masses(self,file):
        str = self.getlinewhile(file)
        while str != "\n" and str != "":
            line = str.split(" ")
            self.masses[int(line[0])-1] = float(line[1])
            str = self.getline(file)



    def input_Atoms(self,file):
        str = self.getlinewhile(file)
        i = 0
        while str != "\n" and str != "":
            line = str.split(" ")
            self.atoms[i].input_Atomic(line)
            i = i+1
            #self.atoms[int(line[0])-1].input_Atomic(line)
            str = self.getline(file)

    def input_Velocity(self,file):
        str = self.getlinewhile(file)
        i = 0
        while str != "\n" and str != "":
            line = str.split(" ")
            self.atoms[i].input_Velocity(line)
            i = i+1
            #self.atoms[int(line[0])-1].input_Velocity(line)
            str = self.getline(file)

    
    def output_System(self,file):
        file.write("\n")
        file.write("\n")
        line = str(self.na) + " atoms\n"
        file.write(line)
        line = str(self.nt) + " atom types\n"
        file.write(line)

        file.write("\n")
        line = str(self.x[0]) + " " + str(self.x[1]) + " " + "xlo xhi\n"
        file.write(line)
        line = str(self.y[0]) + " " + str(self.y[1]) + " " + "ylo yhi\n"
        file.write(line)
        line = str(self.z[0]) + " " + str(self.z[1]) + " " + "zlo zhi\n"
        file.write(line)

        file.write("\n")
        file.write("Masses\n")
        for i in range(0,self.nt):
            file.write("\n") 
            line = str(i+1) + " " + str(self.masses[i]) 
            file.write(line)

        file.write("\n\n")
        file.write("Atoms #atomic\n")
        for i in range(0,self.na):
            file.write("\n")
            line = str(i+1) + " " + str(self.atoms[i].type+1) + " " + str(self.atoms[i].posi.pos[0])+ " " + str(self.atoms[i].posi.pos[1])+ " " + str(self.atoms[i].posi.pos[2]) + " " + str(self.atoms[i].posi.bound[0]) + " " + str(self.atoms[i].posi.bound[1])+ " " + str(self.atoms[i].posi.bound[2]) 
            file.write(line)


        file.write("\n\n")
        file.write("Velocities\n")

        for i in range(0,self.na):
            file.write("\n")
            line = str(i+1) + " " + str(self.atoms[i].velo.velo[0])+ " " + str(self.atoms[i].velo.velo[1])+ " " + str(self.atoms[i].velo.velo[2]) 
            file.write(line)

             

def random_vacancy(lat,porosity):
    nv = int(lat.na * porosity+0.50)
    lat.na = lat.na - nv
    print(lat.na)
    st = set()
    print(type(st))
    while len(st) < nv :
        k = random.randint(0,lat.na)
        st.add(k)

    vlist = list(st)
    vlist.sort()
    print(type(vlist))
    print(vlist)

    vlist.reverse()
    print(vlist)
    print(type(vlist))
    for i in vlist:
        lat.atoms.pop(i)




        






       




#file = "in.min.structure"
file = "in.structure.replicate"
f = open(file,"r")

file = "in.structure"
fo = open(file,"w")


lattice = System()
lattice.input_sysytem(f)

porosity = 0.05

random_vacancy(lattice,porosity)
lattice.output_System(fo)




