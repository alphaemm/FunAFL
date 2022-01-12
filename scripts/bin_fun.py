class Binary_functions(object):
    def __init__(self,addr,name,hashval):
        super(Binary_functions, self).__init__()
        self.addr = addr
        self.name = name
        self.hash = hashval
        self.cmp_num = 0
        self.mem_num = 0
        self.ins_num = 0
        self.bb_nums = 0
        self.offspring_reciprocal = 0
        self.betweeness = 0
        self.retain1 = 0
        self.retain2 = 0
        self.retain3 = 0
    
    # def __init__(self,cmp_num,mem_num,ins_num,bb_nums,offspring_reciprocal,betweeness,retain1,retain2,retain3):
    #     self.cmp_num = cmp_num
    #     self.mem_num = mem_num
    #     self.ins_num = ins_num
    #     self.bb_nums = bb_nums
    #     self.offspring_reciprocal = offspring_reciprocal
    #     self.betweeness = betweeness
    #     self.retain1 = retain1
    #     self.retain2 = retain2
    #     self.retain3 = retain3

    #[16750, 122, 217548, 15488, 249.24458717480363, 0.05709518512633081, 0, 0, 0]
    #[16750, 122, 217548, 15488, 249.24458717480363, 0.020694952063138938, 0, 0, 0]
    def set_attr(self,cmp_num,mem_num,ins_num,bb_nums,offspring_reciprocal,betweeness,retain1,retain2,retain3):
        self.cmp_num = cmp_num
        self.mem_num = mem_num
        self.ins_num = ins_num
        self.bb_nums = bb_nums
        self.offspring_reciprocal = offspring_reciprocal
        self.betweeness = betweeness
        self.retain1 = retain1
        self.retain2 = retain2
        self.retain3 = retain3
    def set_attr_by_list(self,list_attr):
        self.cmp_num = list_attr[0]
        self.mem_num = list_attr[1]
        self.ins_num = list_attr[2]
        self.bb_nums = list_attr[3]
        self.offspring_reciprocal = list_attr[4]
        self.betweeness = list_attr[5]
        self.retain1 = list_attr[6]
        self.retain2 = list_attr[7]
        self.retain3 = list_attr[8]
    def get_attr(self):
        return [self.cmp_num,self.mem_num,self.ins_num,self.bb_nums,self.offspring_reciprocal,self.betweeness,self.retain1,self.retain2,self.retain3]

    def set_cmp_num(self,cmp_num):
        self.cmp_num = cmp_num
    def get_cmp_num(self):
        return self.cmp_num
    
    def increase_mem_num(self):
        self.mem_num = self.mem_num+1
    def set_mem_num(self,mem_num):
        self.mem_num = mem_num
    def get_mem_num(self):
        return self.mem_num

    def set_ins_num(self,ins_num):
        self.ins_num = ins_num
    def get_ins_num(self):
        return self.ins_num

    def set_bb_nums(self,bb_nums):
        self.bb_nums = bb_nums
    def get_bb_nums(self):
        return self.bb_nums

    def set_offspring_reciprocal(self,offspring_reciprocal):
        self.offspring_reciprocal = offspring_reciprocal
    def get_offspring_reciprocal(self):
        return self.offspring_reciprocal

    def set_betweeness(self,betweeness):
        self.betweeness = betweeness
    def get_betweeness(self):
        return self.betweeness

    def set_retain1(self,retain1):
        self.retain1 = retain1
    def get_retain1(self):
        return self.retain1
    def set_retain2(self,retain2):
        self.retain2 = retain2
    def get_retain2(self):
        return self.retain2
    def set_retain3(self,retain3):
        self.retain3 = retain3
    def get_retain3(self):
        return self.retain3
    
    

    


        