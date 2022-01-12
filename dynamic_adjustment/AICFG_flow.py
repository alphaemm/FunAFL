# -*- coding: utf-8 -*-
import networkx as nx
from bin_fun import Binary_functions
from copy import deepcopy
import json
import math
import argparse
import pickle
import sys
import os
from data_process import *
from collections import defaultdict

basename = ""
fuzz_out = ""
filename = ""

dirname = os.path.dirname(sys.argv[0])
parameters_path = os.path.join(dirname, "parameters.json")
parameters = json.load(open(parameters_path, "r"))

CG = nx.DiGraph()
hash2fun_node = {}
function2count = defaultdict(dict)

partition_wl_graph = parameters['partition_wl_graph']
function_count_lower = parameters['function_count_lower']
wl_time_base = parameters['wl_time_base']
attributes_num = parameters["attributes_num"]
base_exp = 1
wl_time = 1


def get_sum_of_attributes():
    global CG
    start = list(CG.nodes())[0].get_attr()
    for i,node in enumerate(CG.nodes()):
        if i!=0:
            cur_attr = node.get_attr()
            start = list_add(start,cur_attr)
    return start

def number_range():
    attributes_sum = []
    attributes = []
    for node in CG.nodes():
        attributes.append(node.get_attr())
        attributes_sum = list_add(attributes_sum,node.get_attr())
    print (attributes_sum)

def wl_subgraph(time=1):
    global CG,hash2fun_node
    for _ in range(time):
        new_CG = deepcopy(CG)
        new_hash2funcnodes = {}
        for node in new_CG.nodes():
            new_hash2funcnodes[node.addr] = node
        node2node = {}
        for hashv in hash2fun_node:
            node2node[hash2fun_node[hashv]]=new_hash2funcnodes[hashv]
        for node in CG.nodes():
            cur_attr = node.get_attr()
            cycle_nodes = []
            for temp_cycle_node in CG.predecessors(node):
                cycle_nodes.append(temp_cycle_node)
            for temp_cycle_node in CG.successors(node):
                cycle_nodes.append(temp_cycle_node)
            cycle_num = len(cycle_nodes)
            if cycle_num==0:
                continue
            attributes = []
            for cycle_node in cycle_nodes:
                attributes.append(cycle_node.get_attr())
            sum_of_attributes = sum_of_list_of_list(attributes)
            averget_of_attributes = list_parameter_multiply(sum_of_attributes,1.0/cycle_num)
            new_attributes1 = list_parameter_multiply(averget_of_attributes,partition_wl_graph)
            new_attributes2 = list_parameter_multiply(cur_attr,1-partition_wl_graph)
            new_attributes = list_add(new_attributes1,new_attributes2)
            node2node[node].set_attr_by_list(new_attributes)
        CG = new_CG
        hash2fun_node = new_hash2funcnodes


def get_count_score(count):
    return base_exp**count

def standardization(average_v,std_v):
    for node in CG.nodes():
        attr = node.get_attr()
        new_attr = []
        for i,v in enumerate(attr):
            if v!=0:
                new_attr.append((v-average_v[i])/std_v[i])
            else:
                new_attr.append(v)
        node.set_attr_by_list(new_attr)

def get_data_feature():
    max_value = []
    min_value = []
    sum_value = []
    average_value = []
    square_average_value = [] 
    s_square = []
    square = []
    number = len(CG.nodes())

    for i,node in enumerate(CG.nodes()):
        attrs = node.get_attr()
        if i==0:
            max_value = deepcopy(attrs)
            min_value = deepcopy(attrs)
            sum_value = deepcopy(attrs)
            s_square = list_square(attrs)
        else:
            s_square = list_add(s_square,list_square(attrs))
            for j,attr in enumerate(attrs):
                if attr > max_value[j]:
                    max_value[j] = attr
                if attr < min_value[j]:
                    min_value[j] = attr
                sum_value[j] = sum_value[j] + attr
    for p,value in enumerate(sum_value):
        average_value.append(value/(number+0.0))  
        square_average_value.append(s_square[p]/(number+0.0))

    for p,value in enumerate(average_value):
        square.append(math.sqrt(square_average_value[p]-average_value[p]**2))


    print ("max:",max_value)
    print ("min:",min_value)
    print ("sum:",sum_value)
    print ("average:",average_value)
    print ("square",square)

    return {"mmax":max_value,"mmin":min_value,"ssum":sum_value,"aaverage":average_value,"ssquare":square}

def normalization_max_min_range(start=[0]*9,end=[100]*9):
    max_value = []
    min_value = []
    sum_value = []
    average_value = []
    number = len(CG.nodes())

    for i,node in enumerate(CG.nodes()):
        attrs = node.get_attr()
        if i==0:
            max_value = deepcopy(attrs)
            min_value = deepcopy(attrs)
            sum_value = deepcopy(attrs)
        else:
            for j,attr in enumerate(attrs):
                if attr > max_value[j]:
                    max_value[j] = attr
                if attr < min_value[j]:
                    min_value[j] = attr
                sum_value[j] = sum_value[j] + attr
    for p,value in enumerate(sum_value):
        average_value.append(value/(number+0.0))    

    for node in CG.nodes():
        attrs = node.get_attr()
        new_attrs = []
        for j,attr in enumerate(attrs):
            div = max_value[j]-min_value[j]
            if div==0:
                div = 1
            new_attrs.append(start[j]+(end[j]-start[j])*((attr-min_value[j])/(div)))
        node.set_attr_by_list(new_attrs)

def write_graph_attributes(tail_name):
    with open(basename+filename+"_"+tail_name,"w") as target:
        title = "function_name,cmp_num,mem_num,ins_num,bb_nums,offspring_reciprocal,betweeness,retain1,retain2,retain3"+"\n"
        target.write(title)
        for node in CG.nodes():
            target.write(node.name+",")
            for i,attr in enumerate(node.get_attr()):
                target.write(str(attr))
                if i!=len(node.get_attr())-1:
                    target.write(",")
            target.write("\n")
            
def write_function2attributes(s="_function2attribute.json"):
    function2attributes = defaultdict(dict)
    for node in CG.nodes():
        function2attributes[node.funNameHash][node.hashVal]=node.get_attr()
    output_loc2function = fuzz_out + os.sep+ filename + s
    with open(output_loc2function,"w") as ouf:
        json.dump(function2attributes,ouf)

def write_bb2attributes(s="_bb2attributes.json"):
    function2attributes = defaultdict(list)
    for node in CG.nodes():
        function2attributes[node.addr]=node.get_attr()
    output_function2attributes = fuzz_out + os.sep+ filename + s
    with open(output_function2attributes,"w") as ouf:
        # ouf.write(str(dict(function2attributes)))
        json.dump(function2attributes, ouf)

def reconstruct_graph():
    global base_exp
    global CG,hash2fun_node
    cg_name = os.path.join(basename,filename+"_cg.pkl")
    cg_name2 = os.path.join(fuzz_out,filename+"_cg_not_first.pkl")
    if os.path.exists(cg_name2):
        cg_name = cg_name2
    CG = pickle.load(open(cg_name,"rb"))
    for node in CG.nodes():
        hash2fun_node[node.addr] = node
    
    data_feature = get_data_feature()
    name = os.path.join(fuzz_out,"function2count.txt")
    fp = open(name,"r")
    max_function_count = 0
    datas = fp.readlines()
    bbs_hit={}
    for line,data in enumerate(datas):
        cur_data = data.strip().replace("\n","")
        key = int(cur_data.split(":")[0])
        value = int(int(cur_data.split(":")[1]))
        bbs_hit[key]=value
        if value>max_function_count:
            max_function_count = value
    fp.close()

    base_exp = math.pow(function_count_lower,1.0/max_function_count)

    number_range()
    for node in CG.nodes():
        if node.addr in bbs_hit:
            count = bbs_hit[node.addr]
            new_attr = list_parameter_multiply(node.get_attr(),get_count_score(count))
            node.set_attr_by_list(new_attr)
    normalization_max_min_range(data_feature["mmin"],data_feature["mmax"])

def keep_average(average1,average2):
    average_ratio = []
    for i in range(attributes_num):
        average_ratio.append(average1[i]/average2[i])
    for node in CG.nodes():
        attrs = node.get_attr()
        new_attrs = []
        for i,att in enumerate(attrs):
            if i >= attributes_num:
                new_attrs.append(0)
                continue
            new_attrs.append(att*average_ratio[i])
        node.set_attr_by_list(new_attrs)

def main():
    reconstruct_graph()
    global wl_time
    nodes_num = len(list(CG.nodes()))
    if int(nodes_num/wl_time_base)>1 and wl_time<=1:
        wl_time = int(nodes_num/wl_time_base)
    print(("nodes_num:%d,wl_time_base:%d,wl_times:%d")%(nodes_num,wl_time_base,wl_time))
    wl_subgraph(wl_time)
    print("wl:")
    data_feature2 = get_data_feature()
    normalization_max_min_range([0]*9,[100]*9)
    write_bb2attributes("_bb2attributes_not_first.json")
    cg_file = os.path.join(fuzz_out,filename+"_cg_not_first.pkl")
    nx.write_gpickle(CG,cg_file)


if __name__ == '__main__':
    base_file = sys.argv[1]
    fuzz_out = sys.argv[2] # fuzz_out directory
    filename = os.path.basename(base_file) # target program directory
    basename = os.path.dirname(base_file) # target program name
    main()
    
