#比较指令
cmp_insn = ["jmp","cmp","test","jz","jnz","jc","jnc","je","jne",\
    "js","jns","jo","jno","jp","jpe","jnp","jpo","ja","hnbe",
    "jae","jnb","jb","jane","jbe","jna","jg","jnle",\
        "jge","jnl","jl","jnge","jle","jng","cmp","cmpsb","cmpsw","cmpsd","cmpxchg","cmpxchg"]
#内存操作、文件操作、字符串操作相关的函数
mem_insn = ["malloc","calloc","realloc","alloca","free","shmat",\
    "fopen","fread","fputc","memcpy","memcmp","read","write","memset","strtod"]
#字符串操作
string_insn = ["cmps", "cmpsq", "cmpsb", "cmpsd", "cmpsl", "cmpsw", "lods","lodsq", \
    "lodsb", "lodsl", "lodsd", "lodsw", "movs", "movsq","movsb", "movsl", "movsd", \
        "smovl", "movsw", "smovw", "scas","scasq", "scasb", "scasl", "scasd", \
            "scasw", "stos", "stosq","stosb", "stosl", "stosd", "stosw","rep", "repe", "repz", "repne", "repnz"]