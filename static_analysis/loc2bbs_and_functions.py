# -*- coding: utf-8 -*-
import idaapi
import idautils
import idc
from data_process import *
from bisect import bisect_right
import datetime
from collections import defaultdict
import os
import json

bin = idc.GetInputFilePath()

dirname = os.path.dirname(bin)
basename = os.path.basename(bin)

key2function = {}
bbl2hash = {}                 # bbl_addr -> hash, different bbls may 
hashed_functions = set() # normal hash functions(except lib functions, thunk functions, ...)

loc2funcion = defaultdict(set) #loc->[fun1_addr,fun2_addr,...]
loc2addr = defaultdict(set)  # loc -> [addr1,addr2, ...]

bbl2_seen_hash = defaultdict(set)


funtions_end_without_f = defaultdict(list)
functions_end_with_f = defaultdict(list)#函数->结尾处调用的函数
fun2_end_nodes = defaultdict(list)
nodes2functions = defaultdict(list)

all_functions_addrs = list(idautils.Functions())

min_addr = idc.get_inf_attr(INF_MIN_EA)
max_addr = idc.get_inf_attr(INF_MAX_EA)

Nonenum = 0

class BBWrapper(object):
  def __init__(self, ea, bb):
    self.ea_ = ea
    self.bb_ = bb

  def get_bb(self):
    return self.bb_

  def __lt__(self, other):
    return self.ea_ < other.ea_
class BBCache(object):
  def __init__(self):
    self.bb_cache_ = []
    for f in idautils.Functions():
        for bb in idaapi.FlowChart(idaapi.get_func(f)):
            self.bb_cache_.append(BBWrapper(bb.startEA, bb))
    self.bb_cache_ = sorted(self.bb_cache_)

  def find_block(self, ea):
    i = bisect_right(self.bb_cache_, BBWrapper(ea, None))
    if i:
      return self.bb_cache_[i-1].get_bb()
    else:
      return None
bb_cache = BBCache()


def get_block_hash(block):
    # specific = ["movsxd","mov","xor","add","mov","mov"]
    rv = -2 #-2 for no operand, -1 for ready，>0 for already set
    rv_shiift = -2 #same as rv
    # imm_op_values = []

    start,endEA = block.startEA, block.endEA
    cur_addr = start
    while cur_addr<endEA:
        if idc.get_operand_type(cur_addr, 0) == 5 and \
                (min_addr < idc.get_operand_value(cur_addr, 0) < max_addr):
            idc.OpOff(cur_addr, 0, 0)
        if idc.get_operand_type(cur_addr, 1) == 5 and \
                (min_addr < idc.get_operand_value(cur_addr, 1) < max_addr):
            idc.op_plain_offset(cur_addr, 1, 0)

        line = idc.generate_disasm_line(cur_addr,0)
        # print(hex(cur_addr),line)
        if "__afl_area_ptr" in line:
            rv = -1
        elif rv==-1 and "xor" in line:
            rv = idc.get_operand_value(cur_addr, 1)
        if "movedwordptrfs:[rbx]" in line.replace(" ",""):
            rv_shiift = -1
        if rv_shiift==-1:
            rv_shiift = idc.get_operand_value(cur_addr, 1)
            if rv_shiift!=(rv>>1):
                print("XOR ERROR...")
                print(rv)
                print(rv>>1)
                print(rv_shiift)
                # exit(1)

        cur_addr = idc.NextHead(cur_addr)

    return rv
def write_loc2bbs(s="_loc2addrs.json"):
    for loc in loc2addr:
        loc2addr[loc] = list(loc2addr[loc])
        # if len(loc2bbs[loc])>=3:
            # print(loc,loc2bbs[loc])
    output_loc2bbs = dirname + os.sep+ basename + s
    with open(output_loc2bbs,"w") as ouf:
        json.dump(loc2addr,ouf)
def write_loc2functions(s="_loc2functions.json"):
    for loc in loc2funcion:
        loc2funcion[loc] = list(loc2funcion[loc])
        # if len(loc2functions[loc])>=2:
            # print(loc,loc2functions[loc])
    output_loc2function = dirname + os.sep+ basename + s
    with open(output_loc2function,"w") as ouf:
        json.dump(loc2funcion,ouf)
def find_hashed_blocks(func):
    global key2function
    addrhash = {}
    f = idaapi.FlowChart(idaapi.get_func(func),flags=idaapi.FC_PREDS)
    for bb in f:
        key2function[(bb.startEA,bb.endEA)]=func
        hashVal = get_block_hash(bb)
        if hashVal>0:
            addrhash[(bb.startEA,bb.endEA)] = hashVal
            bbl2hash[(bb.startEA,bb.endEA)] = hashVal
    return addrhash

def function_filter(f):
    function_name = GetFunctionName(f)
    if "afl" in function_name or "__libc" in function_name:
        return False    
    flags = idc.GetFunctionAttr(f, FUNCATTR_FLAGS)
    if flags & FUNC_LIB or flags & FUNC_THUNK: 
        return False
    if idc.SegName(f)!=".text":
        return False
    return True

#目的是得到所有的调用函数的结束基本块，包括循环调用
def get_all_ends(key,result,avoid_cyc=[]):
    if key in avoid_cyc:
        return
    avoid_cyc.append(key)
    f2 = nodes2functions[key][0]

    # print idc.GetFunctionName(f2)

    end_with_functions = functions_end_with_f[f2]#函数f2中存在函数调用的结束基本块
    end_without_functions = funtions_end_without_f[f2]#函数f2中不存在函数调用的结束基本块
    result += end_without_functions
    for k in end_with_functions:
        get_all_ends(k,result,avoid_cyc)
#同上，但是输入是函数
def get_all_ends_by_fun_addr(f2,result):
    end_with_functions = functions_end_with_f[f2]
    end_without_functions = funtions_end_without_f[f2]
    result += end_without_functions
    #如果存在多个基本块调用，取最后的一个
    if len(end_with_functions)>0:
        k  = end_with_functions[-1]
        get_all_ends(k,result)
#得到函数对应的开始结点和结束结点（这里的结束结点就包括）
def get_start_end_nodes_by_fun_addr(start_fun_addr):
    start_node = idaapi.FlowChart(idaapi.get_func(start_fun_addr),flags=idaapi.FC_PREDS)[0]
    start = [(start_node.startEA,start_node.endEA)]
    result = []
    get_all_ends_by_fun_addr(start_fun_addr,result)
    # if len(result)==0:
        # write_log(log_file,"find no end nodes for function:%s"%(idautils.GetFunctionName(start_fun_addr)))
    return (start,result)
    
def find_next_start(entry,avoid_cyc2):
    result = []

    for bb in entry.succs():#对结点的后继结点进行循环
        key = (bb.startEA,bb.endEA)
        if key in bbl2hash: #如果当前结点是hash结点，那么就是函数调用之后的hash结点
            result.append(key)
            avoid_cyc2.add(bb.startEA)
        elif len(nodes2functions[key])>0:#不是hash结点的时候，并且调用了函数，那么下一个函数就会形成函数间的loc
                start_fun_addr = nodes2functions[key][0]#只取第一个
                start_node = idaapi.FlowChart(idaapi.get_func(start_fun_addr),flags=idaapi.FC_PREDS)[0]
                start = (start_node.startEA,start_node.endEA)
                result.append(start)
        else:
            #连续非hash并且无函数调用的情况，继续搜索下一个
            if entry.startEA not in avoid_cyc2:
                avoid_cyc2.add(bb.startEA)
                result += find_next_start(bb,avoid_cyc2)
    return result
 #计算pre_nodes看见的结点和当前结点所计算的hash值
def for_calculate(pre_nodes,cur_nodes):
    ret = -1
    for pre_key_seen in pre_nodes:
        for pre_key in bbl2_seen_hash[pre_key_seen]:    
            #对于比较复杂的程序来说，有些地方没插桩，跳过
            if pre_key not in bbl2hash:
                print("jump:",pre_key)
                continue
            for cur_key in cur_nodes:
                #对于比较复杂的程序来说，有些地方没插桩，跳过
                if cur_key not in bbl2hash:
                    print("jump:",cur_key)
                    continue
                pre = bbl2hash[pre_key]
                cur = bbl2hash[cur_key]
                loc = (pre >> 1)^cur
                # if loc==32716:
                    # ret=1
                    # print("***************")
                # loc2addr[loc].append((hex(pre_key[0]),hex(cur_key[0])))
                loc2addr[loc].add(pre_key[0])
                loc2addr[loc].add(cur_key[0])
                loc2funcion[loc].add(key2function[pre_key])
                loc2funcion[loc].add(key2function[cur_key])
    return ret
#PREV是基本块结点entry所对应的hash值
#END则是entry调用函数之后回到的基本块
def process_node_with_functions(entry,PREV,END):
    cur_addr = entry.startEA
    end_addr = entry.endEA
    key = (cur_addr,end_addr)

    funs = nodes2functions[key]
    # num_funs = len(funs)
    #处理了连续调用的情况，即一个基本块中调用了多个函数
    prev = None
    for i,f in enumerate(funs):
        start,end = get_start_end_nodes_by_fun_addr(f)
        if i==0:
            ret = for_calculate(PREV,start)
            # if ret==1:
            #     print("--------------")
        else:
            if prev==None:
                print("**************ERROR/207*************")
                # exit(1)
            ret = for_calculate(prev,start)
            
        prev = end
    ret = for_calculate(prev,END)
    # if ret==1:
    #     print(key)
    #     print(cur_addr)
    #     print(funs)
    #     print(start)
    #     print(end)
    #     print(prev)
    #     print(END)
    #     print("--------------")
def calculate_special_loc(entry,avoid_cyc):
        #避免循环的操作
        if entry.startEA in avoid_cyc:
            return
        avoid_cyc.add(entry.startEA)
        cur_addr = entry.startEA
        end_addr = entry.endEA
        key = (cur_addr,end_addr)#获取key
        if len(nodes2functions[key])>=1:
            prevs = bbl2_seen_hash[key]#获取当前结点可以看到的hash值
            avoid_cyc2 = set()
            ends = find_next_start(entry,avoid_cyc2)
        
        # if len(nodes2functions[key])>=1:
            process_node_with_functions(entry,prevs,ends)
        # print "first finish"
        for bb in entry.succs():
            calculate_special_loc(bb,avoid_cyc)


def calculate_inter_hash(hashed_functions):
    sum = len(hashed_functions)
    for count,f in enumerate(hashed_functions):
        print("[+]outer cal,[%d/%d],function name:%s"%(count,sum,idc.GetFunctionName(f)))
        avoid_cyc = set()
        entry = list(idaapi.FlowChart(idaapi.get_func(f),flags=idaapi.FC_PREDS))[0]
        calculate_special_loc(entry,avoid_cyc)

#过程内
def calculate_intra_hash(f,addrhash):
    #addrhash: (start_addr,end_addr)->hash

    cur_function = idaapi.get_func(f)
    cur_function_addr_start = cur_function.startEA
    cur_function_addr_end = cur_function.endEA
    global loc2funcion,loc2addr

    entry = list(idaapi.FlowChart(idaapi.get_func(f),flags=idaapi.FC_PREDS))[0]
    
    seen_hash = defaultdict(set)
    # bbsd=searchbb(f)
    
    for node in addrhash:
        if node[0] == entry.startEA:
            # cur = addrhash[node]
            # loc = (0>>1)^cur

            # loc2addr[loc].append((hex(0),hex(node[0])))#loc->(start_addr,end_addr)
            # loc2funcion[loc].add(f)
            # continue
            pass
        seen_hash[node].add(node)
        bbl2_seen_hash[node].add(node)

        propagated = set()

        def propagate_hash(node):
    
            #找到当前结点对应的基本块对象
            # cur_basic = bbsd[node[0]]
            cur_basic = bb_cache.find_block(node[0])

            for ss in cur_basic.succs():
                s = (ss.startEA,ss.endEA)
                # not an instrumented node, and never seen before (such as in a loop)
                if not s in addrhash and not s in propagated:
                    seen_hash[s] |= seen_hash[node]
                    bbl2_seen_hash[s] |= bbl2_seen_hash[node]

                    propagated.add(s)
                    propagate_hash(s)
                # elif s in addrhash:
                    # next_hash[node].add(s)
        propagated.add(node)
        propagate_hash(node)

    for node in addrhash:
        if node[0] != entry.startEA:
            for pp in bb_cache.find_block(node[0]).preds():
            # for pp in bbsd[node[0]].preds():
                p = (pp.startEA,pp.endEA)
                for h in seen_hash[p]:
                    prev = addrhash[h]
                    cur = addrhash[node]
                    loc = (prev >> 1) ^ cur
                    if loc==40956:
                        print("***************")
                    loc2addr[loc].add(h[0])
                    loc2addr[loc].add(node[0])
                    loc2funcion[loc].add(f)
    #入口结点（入度为0的结点）
    # entry_hash_node = (entry.startEA,entry.endEA)
    #结束结点（初度为0的结点）
    #这里用字典，是要区分开不同结束结点所对应的hash结点
    # exit_hash_nodes = defaultdict(set)

    #寻找结束结点能看到的hash结点
    # for n in get_node_ends(f):
        # for h in seen_hash[n]:
            # exit_hash_nodes[n].add(h)

    #存储的是函数开始结点和结束结点所能看到的hash结点
    # function_hashes[f] = (entry_hash_node, exit_hash_nodes)

    # for ff in CodeRefsTo(f,0):
        # funtions_refTo_f[ff].append(f)

    bbs = idaapi.FlowChart(idaapi.get_func(f),flags=idaapi.FC_PREDS)
    ex_bb = []

    #对基本块进行循环
    for bb in bbs:
        #对于某些如jmp结尾处调用情况，会出现不属于该函数的基本块出现，这里跳过
        if bb.startEA < cur_function_addr_start or bb.endEA >= cur_function_addr_end:
            continue
        if bb.startEA in ex_bb:
            continue   
        key = (bb.startEA,bb.endEA)
        cur_addr = bb.startEA
        end_addr = bb.endEA
        temp_addr = -1
        #对每一条指令进行循环
        while cur_addr < end_addr:
            menm = idc.GetMnem(cur_addr)
            if menm == "call" or menm == "jmp":
                addr = idc.GetOperandValue(cur_addr,0)
                # print len(all_functions_addrs),cur_addr,hex(cur_addr),hex(addr),addr,addr in all_functions_addrs
                #如果指令是call或者jmp(这两种指令都可能是调用指令)，查看其后的地址是否是函数开始地址，如果是就是调用指令
                #in all functions or in hash functions?
                if addr in all_functions_addrs and function_filter(addr):
                    # if menm == "jmp":
                        # print idc.GetDisasm(cur_addr)
                    if key not in nodes2functions:
                        print(key)
                        print("**************ERROR/345*************")
                        # exit(1)
                    if addr not in nodes2functions[key]:
                        print(addr)
                        print("**************ERROR/349*************")
                        # exit(1)
                    # nodes2functions[key].append(addr)#记录此结点调用的函数
            temp_addr = cur_addr
            cur_addr = idc.NextHead(cur_addr)
        #如果最后一条指令是jmp指令
        menm = idc.GetMnem(temp_addr)
        if menm == "jmp":
            #判断结尾处是否函数调用
            addr = idc.GetOperandValue(temp_addr,0)
            #结尾处存在jmp形式函数调用时，其初度为1
            if len(list(bb.succs()))==1 and addr in all_functions_addrs:
                fun2_end_nodes[f].append(key)#将结束结点添加到fun2_end_nodes中
                if len(nodes2functions[key]) > 0:
                    functions_end_with_f[f].append(key)#如果该基本块存在函数调用，存入functions_end_with_f，f->(bb.startEA,bb.endEA)
                else:
                    funtions_end_without_f[f].append(key)#如果该基本块不存在函数调用，存入functions_end_without_f，f->(bb.startEA,bb.endEA)
                for ss in bb.succs():
                    ex_bb.append(ss.startEA)#如果是jmp跳转会将初度算1，将其他函数开始结点算入，因此为了避免重复多算，加入变量ex_bb中
        else:
            if len(list(bb.succs()))==0:#如果最后一条指令不是jmp指令，并且当前基本块初度为0，那么这是函数的结束结点
                # print hex(key[0]),hex(key[1])
                fun2_end_nodes[f].append(key)#将结束结点添加到fun2_end_nodes中
                if len(nodes2functions[key]) > 0:
                    functions_end_with_f[f].append(key)#如果该基本块存在函数调用，存入functions_end_with_f，f->(bb.startEA,bb.endEA)
                else:
                    funtions_end_without_f[f].append(key)#如果该基本块不存在函数调用，存入functions_end_without_f，f->(bb.startEA,bb.endEA)

def get_all_node2functions():
    global nodes2functions,Nonenum
    for i,f in enumerate(idautils.Functions()):
        if not function_filter(f):
            continue
        refto = CodeRefsTo(f, 0)
        for ref in refto:
            call_bb = bb_cache.find_block(ref)
            # print(bb_cache.bb_cache_)
            # if call_bb==None:
            #     print(ref)
            #     # print(bb_cache.find_block(ref))
            #     # print(bb_cache.bb_cache_)
            #     Nonenum+=1
            # else:
            key = (call_bb.startEA,call_bb.endEA)
            nodes2functions[key].append(f)#记录此结点调用的函数

    # refto = CodeRefsTo(f, 0)
def main():
    hash_cnt = 0 #hash基本块数量
    hash_funcs = 0 #被插桩的的函数数量
    get_all_node2functions()
    sum_functions = len(list(idautils.Functions()))
    for i,f in enumerate(idautils.Functions()):
        if not function_filter(f):
            print("[-]jump, function is %s and addr is %s"%(idc.GetFunctionName(f),f))
            continue
        print("[+]inter cal,[%d/%d],function name:%s and addr is %s"%(i,sum_functions,idc.GetFunctionName(f),hex(f)))
        addrhash = find_hashed_blocks(f)
        hash_cnt += len(addrhash)
        if len(addrhash) == 0:
            print("has no hash node the function is %s and addr is %s"%(idc.GetFunctionName(f),f))
            continue
        hash_funcs = hash_funcs + 1
        hashed_functions.add(f)
        calculate_intra_hash(f,addrhash)
    calculate_inter_hash(hashed_functions)
    # print(loc2addr)
    write_loc2bbs()
    write_loc2functions()

if __name__ == '__main__':
    q = None
    f = None
    # idc.Wait() 
    import sys

    sys.setrecursionlimit(65536)
    start=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(start)
    print(bb_cache.find_block(4197997))
    # print(len(bb_cache.bb_cache_))
    # print([b.bb_.startEA for b in bb_cache.bb_cache_])
    main()
    end=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(end)
    print(start)
    # print(end-start)
    print(Nonenum)
    print("over")
    # idc.Exit(0)