#include <stdio.h>
#include <stdlib.h>     // atoi()
#include <string.h>
#include <sys/stat.h>   //  lstat()
#include <sys/file.h>
#include <unistd.h>     //  access()
#include <limits.h>
#include <math.h>

#include "alloc-inl.h"  //  ck_alloc()
#include "types.h"
#include "cJSON/cJSON.h"
#include "uthash.h"
#include "list.h"
#include "config.h"

struct score_union{
    double seed_score;
    double energy_score;
};

// struct function_count{
//     int function;
//     int count;
//     struct basicblock_count *bbcount;
//     UT_hash_handle hh;         /* makes this structure hashable */
// };

struct basicblock_count{
    int bb_random;
    int count;
    UT_hash_handle hh; 
};

struct basicblocks{
    int bb_random;
    double attributes_seed[ATTRIBUTES_NUMBER];
    double attributes_energy[ATTRIBUTES_NUMBER];
    double score_seed;
    double score_energy;
    UT_hash_handle hh;
    struct list_head list;
};


// struct function2bbs{
//     int function;
//     struct basicblocks *bbs;
//     UT_hash_handle hh;
// };

// struct loc2functions{
//     int loc;
//     int length;
//     int functions[20];
//     UT_hash_handle hh;
// };

struct loc2bbs{
    int loc;
    int length;
    int bbs[20];
    UT_hash_handle hh;
};

// extern struct function2bbs *f2bbs;
// extern struct function_count *f2count;

// extern struct loc2functions *record_loc2funs;
extern struct loc2bbs *record_loc2bbs;
extern struct basicblocks *bbs2attribute;
extern struct basicblock_count *b2count;

extern double average_score;
extern double sum_score;
extern int number_score;

extern double average_score_energy;
extern double sum_score_energy;
extern int number_score_energy;
extern d64 max_score;
extern d64 min_score;

extern int read_success;

// void read_function2attribute(char *fname);
// void read_function2attribute_not_first(u8 *bname,u8 *fuzz_out);
// void print_fun2bbs2attrs(struct function2bbs* f2bb);
// void delete_function2attribute_htab(struct function2bbs *htab);
// void print_fun2count(struct function_count* f2count);
// void write_function_count(u8 *basename);
// void read_loc2functions(char *bname);
void read_loc2bbs(char *bname);
int double_is_equal(double a,double b);
void print_loc2bbs(struct loc2bbs* loc2bb);
void read_bb2attribute(char *bname);
void read_bb2attribute_not_first(u8 *bname,u8 *fuzz_out);
void print_bb2attribute(struct basicblocks* loc2bb);
void print_bb2attribute_not_first(struct basicblocks* loc2bb);
void write_bb_count(u8 *basename);
// struct score_union* get_score_with_loc_and_update_function_count(u32* function_hit_record);
struct score_union* get_score_with_loc_and_update_function_count(int new_tracebit_index[],int count_new_tracebit_index);
