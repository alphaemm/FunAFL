# -*- coding: utf-8 -*-
import os
import sys
import time
from collections import defaultdict
import shutil
import json


class FunAFL(object):
    def __init__(self, name, path):
        self.name = name
        self.path = path
        self.parameters = ""

    def set_afl_parameters(self,parameters):
        self.parameters = parameters

    def get_afl_command(self,afl_path,in_dir,out_dir,target_progs_exec):
        command = afl_path + " "+self.parameters+" "+"-i"+" "+in_dir+" "+"-o"+" "+out_dir
        command += " -- " + target_progs_exec
        return command
    
    def get_script_command(self,out_dir,target_progs,brige_path):
        command = ""
        if os.path.exists(out_dir):
            command = command+"rm -rf "+out_dir+"&&"
        command = command+"mkdir -p "+out_dir
        os.system(command)
        command = os.path.join(brige_path,"brige.sh")+" -t "+target_progs +" -f "+out_dir
        return command

    def get_delete_command(self,out_dir):
        command = "rm -rf "+out_dir
        # os.system(command)
        return command
    


if __name__=="__main__":
    target_progs_path = sys.argv[1]
    code_root_path = sys.argv[2]
    target_progs_csv = sys.argv[3]
    funafl = FunAFL("FunAFL", os.path.join(code_root_path, "afl-2.52b"))

    f = open(target_progs_csv,"r")
    data = f.readline()
    while data:
        data = data.replace("\n","")
        file_path = data.split(",")
        prog_name = file_path[0]
        progs = file_path[1]
        out_dir = file_path[2]
        in_dir = file_path[3]
        progs_exec = progs
        if file_path[4] != "-1":
            progs_exec = progs_exec + " " + file_path[4]
        if file_path[5] != "0":
            progs_exec = progs_exec + " " + "@@"
        if os.path.exists(out_dir):
            os.system("rm -rf " + out_dir)
        brige_path = os.path.join(code_root_path, "dynamic_adjustment")
        cur_script_path = funafl.get_script_command(out_dir, progs, brige_path)
        cmd = "screen -L -t %s -dmS %s-brige %s" % (prog_name, prog_name, cur_script_path)
        print(cmd)
        os.system(cmd)
        time.sleep(3)

        cur_fuzzer  = funafl.get_afl_command(os.path.join(funafl.path, "afl-fuzz"), in_dir, out_dir, progs_exec)
        cmd = "screen -L -t %s -dmS %s-%s %s" % (prog_name, prog_name, "funafl", cur_fuzzer)
        print(cmd)
        os.system("screen -L -t %s -dmS %s-%s %s" % (prog_name, prog_name, "funafl", cur_fuzzer))
        data = f.readline()

