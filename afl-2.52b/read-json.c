#include "read-json.h"


int double_is_equal(double a,double b){
    return fabs(a-b)<1e-15;
}

double get_score_for_each_array(double attributes[]){
    double sum = 0.0;
    for(int i=0;i<ATTRIBUTES_NUMBER;i++){
        sum = sum + (attributes[i]*attributes[i]);
    }
    return sqrt(sum);
}

void add_bb_count(int bb){
    struct basicblock_count *bbc;
    HASH_FIND_INT(b2count,&bb,bbc);
    if(bbc==NULL){
        ACTF("add count can't find bb.");
        exit(1);
    }
    bbc->count++;
    if(bbc->count>2147483600){
        ACTF("INT ERROR:TOO BIG");
        exit(1);
    }
}

struct score_union* get_score_by_bb(int bb)
{
    struct basicblocks *current_bb = NULL;

    HASH_FIND_INT(bbs2attribute,&bb,current_bb);
    if(current_bb==NULL)
    {
        return NULL;
    }
    add_bb_count(bb);
    // add_bb_count_key
    struct score_union * sc = (struct score_union *)malloc(sizeof(struct score_union));
    sc->seed_score = current_bb?current_bb->score_seed:0;
    sc->energy_score = current_bb?current_bb->score_energy:0;
    return sc;
}

struct score_union* get_score_with_loc_and_update_function_count(int new_tracebit_index[],int count_new_tracebit_index)
{
    double score_seed = 0.0;
    double score_energy = 0.0;
    struct score_union* sc_record;

    int bb_num = 0;
    int bb_num_energy = 0;
    for(int j=0;j<count_new_tracebit_index;j++){
        int loc = new_tracebit_index[j];
        struct loc2bbs *temp_loc2bbs;

        HASH_FIND_INT(record_loc2bbs,&loc,temp_loc2bbs);
        if(temp_loc2bbs==NULL){
            continue;
        }else{
            // fprintf(fp_not_found,"found %d:%d\n",j,loc);
        }

        for(int n=0;n<temp_loc2bbs->length;n++){
            int bb_cal = temp_loc2bbs->bbs[n];
            sc_record = get_score_by_bb(bb_cal);
            if(sc_record==NULL){
                // fprintf(fp_not_found,"score equals zero:%d",bb_cal);
            }else{
                score_seed += sc_record->seed_score;
                score_energy += sc_record->energy_score;
                if(!double_is_equal(sc_record->seed_score,0.0)){
                    bb_num++;
                }
                if(!double_is_equal(sc_record->energy_score,0.0)){
                    bb_num_energy++;
                }
            }
	    free(sc_record);
        }

        
    }
    struct score_union* result = (struct score_union*)malloc(sizeof(struct score_union));
    result->seed_score = bb_num==0?average_score:score_seed/(bb_num+0.0);
    result->energy_score = bb_num_energy==0?average_score_energy:score_energy/(bb_num_energy+0.0);

    number_score++;
    if(number_score>2147483600){
        ACTF("INT ERROR:TOO BIG");
        exit(1);
    }
    sum_score = sum_score + result->seed_score;
    average_score = sum_score/number_score;

    number_score_energy++;
    if(number_score_energy>2147483600){
        ACTF("INT ERROR:TOO BIG");
        exit(1);
    }
    sum_score_energy = sum_score_energy + result->energy_score;
    average_score_energy = sum_score_energy/number_score_energy;

    if(result->energy_score<min_score) min_score=result->energy_score;
    if(result->energy_score>max_score) max_score=result->energy_score;
    return result;

}


char* read_info_file(u8 *fname) {
    FILE *fp;
    if (access(fname, R_OK))
    {
        ACTF("Cannot read %s!\n", fname);
        return NULL;
    }
    fp = fopen(fname, "r");
    if (!fp)
    {
        ACTF("Unable to open '%s'", fname);
        goto ret;
    }
    fseek( fp , 0 , SEEK_END );
    int file_size;
    file_size = ftell( fp );
    char *content =  (char *)ck_alloc(file_size * sizeof(char)+1);
    fseek( fp , 0 , SEEK_SET);
    fread(content, file_size , sizeof(char) , fp);
ret:
    fclose(fp);
    return content;
}

// funcMode == 0 -> read_bb2attribute
// funcMode == 1 -> read_bb2attribute_not_first
// funcMode == 2 -> read_loc2bbs
void parse_content(char* content, int funcMode)
{
    int loc;
    const char delims[] = "]";
    char* item_str = strtok(content, delims);
    struct basicblocks *bb;
    struct loc2bbs *s;
    while (item_str != NULL && item_str[0] != '}')
    {
        char* loc_str_start, *loc_str_end;
        loc_str_start = strchr(item_str, '"');
        item_str = loc_str_start;
        loc_str_end = strchr(item_str+1, '"');
        char* loc_str;
        loc_str = (char*)malloc(sizeof(char)*(loc_str_end-loc_str_start));
        strncpy(loc_str, loc_str_start+1, loc_str_end-loc_str_start-1);
        loc_str[loc_str_end-loc_str_start-1] = '\0';
        loc = atoi(loc_str);
        if (funcMode == 2)
        {
            HASH_FIND_INT(record_loc2bbs,&loc,s);
            if(s==NULL){
                s = (struct loc2bbs*)malloc(sizeof(struct loc2bbs));
                s->loc = loc;
                s->length = 0;
                HASH_ADD_INT(record_loc2bbs,loc,s);
            } 
        }
        else
        {
            HASH_FIND_INT(bbs2attribute,&loc,bb);
            if(bb==NULL){
                if (funcMode == 0)
                {
                    bb = (struct basicblocks*)malloc(sizeof(struct basicblocks));
                    bb->bb_random = loc;
                    HASH_ADD_INT(bbs2attribute,bb_random,bb);
                }
                else if (funcMode == 1)
                {
                    ACTF("Read twice but bbs not found:%d\n",loc);
                    exit(1);
                }
            }
            if (funcMode == 0)
                add_bb_count_key(loc);
        }
        free(loc_str);
        int cnt = 0;
        char* val_str;
        char* val_str_start = strchr(item_str, '[');
        while (val_str_start != NULL)
        {
            item_str = val_str_start;
            char* val_str_end = strchr(item_str, ',');
            if (val_str_end == NULL)
            {
                if (funcMode == 2)
                {
                    int value = atoi(item_str+1);
                    s->bbs[s->length++]=value;
                    if(s->length>=20){
                        ACTF("Too many functions in one loc\n");
                        break;
                    }
                }
                else
                {
                    float value = atof(item_str+1);
                    if (funcMode == 0)
                    {
                        bb->attributes_seed[cnt] = value;
                        bb->attributes_energy[cnt++] = value;
                    }
                    else if (funcMode == 1)
                        bb->attributes_seed[cnt++] = value;
                }
                break;
            }
            else
            {
                val_str = (char*)malloc(sizeof(char)*(val_str_end-val_str_start));
                strncpy(val_str, val_str_start+1, val_str_end-val_str_start-1);
                val_str[val_str_end-val_str_start-1] = '\0';
                if (funcMode == 2)
                {
                    int value = atoi(val_str);
                    s->bbs[s->length++]=value;
                    if(s->length>=20){
                        ACTF("Too many functions in one loc\n");
                        break;
                    }
                }
                else 
                {
                    float value = atof(val_str);
                    if (funcMode == 0)
                    {
                        bb->attributes_seed[cnt] = value;
                        bb->attributes_energy[cnt++] = value;
                    }
                    else if (funcMode == 1)
                        bb->attributes_seed[cnt++] = value;
                }
                free(val_str);
                item_str = val_str_end + 1;
                val_str_start = strchr(item_str, ' ');
            }
        }
        if (funcMode == 0)
        {
            bb->score_seed = get_score_for_each_array(bb->attributes_seed);
            bb->score_energy = get_score_for_each_array(bb->attributes_energy);
        }
        else if (funcMode == 1)
            bb->score_seed = get_score_for_each_array(bb->attributes_seed);
        item_str = strtok(NULL, delims);
    }
}


void add_bb_count_key(int bbRandomVal)
{
    struct basicblock_count *s;
    HASH_FIND_INT(b2count,&bbRandomVal,s);
    if(s==NULL){
        s = (struct basicblock_count*)malloc(sizeof(struct basicblock_count));
        s->bb_random = bbRandomVal;
        s->count = 0;
        HASH_ADD_INT(b2count,bb_random,s);
    }
    // return s;
}

void read_bb2attribute(char *bname)
{
    struct basicblocks *bb;
    u8 *fname;


    ACTF("Reading the function attributes of the target binary...");

    fname = alloc_printf("%s_bb2attributes.json", bname);
    char* content = read_info_file(fname);

    int time = 0;
    while (time<JSON_READ_RETRY&&!content)
    {
        content = read_info_file(fname);
        time++;
    }

    if(!content)
        FATAL("Error in read_bb2attribute");

    if (content[strlen(content)-1] == '}')
        parse_content(content, 0);

    ck_free(fname);
    ck_free(content);
}

void read_bb2attribute_not_first(u8 *bname,u8 *fuzz_out)
{
    struct basicblocks *bb;
    char *pLastSlash = strrchr(bname, '/');
    char *pszBaseName = pLastSlash ? pLastSlash + 1 : bname;
    u8* fname = alloc_printf("%s/%s_bb2attributes_not_first.json",fuzz_out,pszBaseName);
    char* content = read_info_file(fname);

    int time = 0;
    while (time<JSON_READ_RETRY&&!content)
    {
        content = read_info_file(fname);
        time++;
    }

    if(!content)
        FATAL("Error in read_bb2attribute");
    
    if (content[strlen(content)-1] == '}')
        parse_content(content, 1);

    ck_free(fname);
    ck_free(content);
}


void read_loc2bbs(char *bname)
{
 
    u8 *fname;
    struct loc2bbs *s;
    ACTF("Reading the loc2bbs of the target binary...");
    fname = alloc_printf("%s_loc2addrs.json", bname);
    char* content = read_info_file(fname);

    int time = 0;
    while (time<JSON_READ_RETRY&&!content)
    {
        content = read_info_file(fname);
        time++;
    }

    if(!content)
        FATAL("Error in read_bb2attribute");
    
    if (content[strlen(content)-1] == '}')
        parse_content(content, 2);
        
    ck_free(content);
    ck_free(fname);
}



void write_bb_count(u8 *basename){
    u8 *fname = alloc_printf("%s/function2count.txt", basename);
    FILE *fp;
    fp = fopen(fname,"w");
    
    // struct function_count* s;
    struct basicblock_count *start_bb;
    for(start_bb=b2count;start_bb!=NULL;start_bb=(struct basicblock_count*)(start_bb->hh.next)){
        fprintf(fp,"%d:%d\n",start_bb->bb_random,start_bb->count);
    }

    ck_free(fname);
    fclose(fp);
}

void print_loc2bbs(struct loc2bbs* loc2bb)
{  
    FILE *fp;
    fp = fopen("loc2bbs.txt","w");
    struct loc2bbs* s;
    // struct basicblock_count* ss,*start_bb;
    for (s = loc2bb; s != NULL; s = (struct loc2bbs*)(s->hh.next)){
        fprintf(fp,"loc:%d,length:%d\n",s->loc,s->length);

        // ss = s->bbcount;
        // printf("%d\n",ss==NULL);
        for(int i=0;i<s->length;i++){
            fprintf(fp,"%d ",s->bbs[i]);
        }
        fprintf(fp,"\n");
    }
    fclose(fp);
}

void print_bb2attribute(struct basicblocks* loc2bb)
{  
    FILE *fp;
    fp = fopen("bb2attributes.txt","w");
    struct basicblocks* s;
    // struct basicblock_count* ss,*start_bb;
    for (s = loc2bb; s != NULL; s = (struct basicblocks*)(s->hh.next)){
        fprintf(fp,"loc:%d,score1:%lf,score2:%lf\n",s->bb_random,s->score_seed,s->score_energy);

        // ss = s->bbcount;
        // printf("%d\n",ss==NULL);
        for(int i=0;i<ATTRIBUTES_NUMBER;i++){
        // for(start_bb=ss;start_bb!=NULL;start_bb=(struct basicblock_count*)(start_bb->hh.next)){
            fprintf(fp,"%lf ",s->attributes_seed[i]);
        }
        fprintf(fp,"\n");
        for(int i=0;i<ATTRIBUTES_NUMBER;i++){
        // for(start_bb=ss;start_bb!=NULL;start_bb=(struct basicblock_count*)(start_bb->hh.next)){
            fprintf(fp,"%lf ",s->attributes_energy[i]);
        }
        fprintf(fp,"\n");
    }
    fclose(fp);
}
void print_bb2attribute_not_first(struct basicblocks* loc2bb)
{  
    FILE *fp;
    fp = fopen("bb2attributes_not_first.txt","w");
    struct basicblocks* s;
    // struct basicblock_count* ss,*start_bb;
    for (s = loc2bb; s != NULL; s = (struct basicblocks*)(s->hh.next)){
        fprintf(fp,"loc:%d,score1:%lf,score2:%lf\n",s->bb_random,s->score_seed,s->score_energy);

        // ss = s->bbcount;
        // printf("%d\n",ss==NULL);
        for(int i=0;i<ATTRIBUTES_NUMBER;i++){
        // for(start_bb=ss;start_bb!=NULL;start_bb=(struct basicblock_count*)(start_bb->hh.next)){
            fprintf(fp,"%lf ",s->attributes_seed[i]);
        }
        fprintf(fp,"\n");
        for(int i=0;i<ATTRIBUTES_NUMBER;i++){
        // for(start_bb=ss;start_bb!=NULL;start_bb=(struct basicblock_count*)(start_bb->hh.next)){
            fprintf(fp,"%lf ",s->attributes_energy[i]);
        }
        fprintf(fp,"\n");
    }
    fclose(fp);
}
