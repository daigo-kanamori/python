import subprocess
import random
import os
import shutil


class input_file:
    separator = "^$"
    def __init__(self):
        self.filename = ""
        self.input = []
        self.variable = []
        self.nv = 0

    def get(self,filename):
        f = open(filename,"r")
        self.filename = filename
        s = f.readline()
        while s != "":
            self.input = self.input + self.detect(s)
            s = f.readline()
        f.close()

    def detect(self,line):
        s = line.split(self.separator)
        ret = [s[0]]
        if len(s) > 1:
            for i in range(0,len(s)-1):
                ret.append("")
                ret.append(s[i+1])
                self.nv = self.nv + 1
                #print("self.nv = ",self.nv)
        return ret


    def get_variable(self,val):
        if self.nv != len(val):
            print("error : input_file : number of variable is not consistent with input file!, file = " + self.filename)
            #print(self.input)
            #jnnprint(self.nv,",",len(val))
            return 
        self.variable = val

    def clear_variable(self):
        self.variable = []

    def leave_file(self,file):
        f = open(file,"w")
        self.leave_file_object(f)
        f.close()

    def leave_file_object(self,f):
        i = 0
        for s in self.input:
            if s != "":
                f.write(s)
            else :
                f.write(str(self.variable[i]))
                i = i+1

class TaskManager:
    extension = ".origin"
    def __init__(self):
        self.original_inputfile = []
        self.inputfile_name = []
        self.origianl_command= []
        self.command_name = []
        self.outdir = "./"

    def load_inputfile(self,file):
        inp = input_file()
        inp.get(file)
        self.original_inputfile.append(inp)
        self.inputfile_name.append(file+".inp")

    def load_command(self,file):
        cmd = input_file()
        cmd.get(file)
        self.origianl_command.append(cmd)
        self.command_name.append(file+"cmd")

    def load_variable_inputfile(self,id,var,name):
        inp = self.original_inputfile[id]
        inp.get_variable(var)
        self.inputfile_name[id] = name

    def load_variable_command(self,id,var,name):
        self.origianl_command[id].get_variable(var)
        self.command_name[id] = name

    def set_outdir(self,dir):
        self.outdir = self.outdir + dir


    def leave_inputfile(self):
        for i in range(len(self.original_inputfile)):
            self.original_inputfile[i].leave_file(self.inputfile_name[i])


    def leave_commandfile(self):
        for i in range(len(self.origianl_command)):
            self.origianl_command[i].leave_file(self.command_name[i])

    def clear_variable(self):
        for inp in self.original_inputfile:
            inp.clear_variable()
        for inp in self.origianl_command:
            inp.clear_variable()


    def run(self):
        for cmd in self.command_name:
            run = subprocess.run(["bash",cmd],capture_output=True,text=True)
            file = self.outdir + "/" + cmd + ".log"
            file =  cmd + ".log"
            f = open(file,"w")
            f.write(str(run.stdout))
            f.close()

