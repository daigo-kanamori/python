import json
import os
import random
import shutil


class Database:

    def __init__(self,root):
        self.root = []
        for dir in root:
            self.root.append(dir)
        self.meta_tag = {}
        self.check_condition()
        self.set_tags()

    def check_condition(self):
        for dir in self.root:
             mymkdir("./"+dir)
             mymkdir("./"+dir+"/tags")
             mymkdir("./"+dir+"/data")

    def set_tags(self):
        for dir in self.root:
            st = get_file_list(dir+"/tags")
            subset = {}
            for file in st:
                f = open(file,"r")
                js = json.load(f)
                
                s = file.split("/")[-1]
                id = s.split(".")[-3]
                subset[str(id)] = js
            self.meta_tag[dir] = subset

    def load_tags(self,dir,id_list):
        if dir not in self.root:
            print("error Database.py : load_data : the directory is invalid")
            return
        subset = self.meta_tag[dir]
        ret = []
        for id in id_list:
            js = subset[str(id)]
            ret.append(js)
        return ret

    def tag(self,dir,id):
        return self.meta_tag[dir][id]
    
    def data(self,dir,id):
        file = dir + "/data/" + str(id) + ".data.json"
        f = open(file,"r")
        js = json.load(f)
        return js


            
    def load_data(self,dir,id_list):
        if str(dir) not in self.root:
            print("error Database.py : load_data : the directory is invalid")
            return 
        ret = []
        for id in id_list:
            file = dir + "/data/" + str(id) + ".data.json"
            f = open(file,"r")
            js = json.load(f)
            ret.append(js)
            print(type(js))
        return ret
        
    
    def search(self,dir,check_func):

        ret = []
        st = self.meta_tag[dir]
        for id, tag in st.items():
            if check_func(tag) == True:
                ret.append(id)
            
        return ret
    
    def register(self,dir,tag,data):
        if tag == {} or data == {}:
            print("error : Database.py in register(tags,data): you input invalid tags and data with augument")
            return 
        id = random.randint(0,90000000)
        subset = self.meta_tag[dir]
        while str(id) in subset.keys():
            id = random.randint(0,90000000)
        subset[str(id)] = tag
        with open(dir+"/tags/"+str(id)+".tags.json","w") as f:
            json.dump(tag,f)
        with open(dir+"/data/"+str(id)+".data.json","w") as f:
            json.dump(data,f)
        print(str(id) + " regsitration is done")
    
    def dump(self,dir,id,set_tag):
        tags = self.meta_tag[dir][id]
        for key in set_tag:
            if key in tags.keys():
                print("  " + key + ":",end=" ")
                print(tags[key])
            else :
                print("  " + key + ": Nothing")
        
    def dump_list(self,dir,id_list,set_tag):
        n = len(set_id)
        for id in set_id:
            print("ID number :" + str(id))
            tags = self.meta_tag[dir][id]
            for key in set_tag:
                if key in tags.keys():
                    print("  " + key + ":",end=" ")
                    print(tags[key])
                else :
                    print("  " + key + ": Nothing")
        
    


    #def dump_list(self,dir,condition,set_tag) :
    #    set_id = self.search(dir,condition)
    #    n = len(set_id)
    #    print("number of data is " + str(n))
    #    for id in set_id:
    #        print("ID number :" + str(id))
    #        tags = self.meta_tag[dir][id]
    #        for key in set_tag:
    #            if key in tags.keys():
    #                print("  " + key + ":",end=" ")
    #                print(tags[key])
    #            else :
    #                print("  " + key + ": Nothing")
    #    
    #    print("dump is done")






def mymkdir(path):
    if os.path.isdir(path):
        return 
    else :
        os.makedirs(path)

def mymkdirs(path):
    s = path.split('/')
    curr = "."
    for nex in s:
        curr = curr + "/" + nex
        mymkdir(curr)
    return 

def get_file_list(path):
    dir_stack = [path]
    file_set = []
    while len(dir_stack) > 0 :
        path = dir_stack.pop(-1)
        files = os.listdir(path)
        for f in files:
            if os.path.isdir(path+"/"+f) == True:
                dir_stack.append(path+"/"+f)
            else :
                file_set.append(path+"/"+f)
    return file_set






