#!/bin/bash

usage() { 
    echo "Usage: $0 -t <target_program_path> -f <fuzz_out_path> -n <taget_program_name>"
}


while getopts ":t:f:n" arg 
do
    case $arg in 
        t)
            target_program_path=${OPTARG}
            ;;
        f)
            fuzz_out_path=${OPTARG}
            ;;
        h)
            usage
            exit 1
            ;;
        ?)
            echo "Error: Invalid option: -$OPTARG"
            echo "Usage: $0 -t <target_program_path> -f <fuzz_out_path>"
            exit 2
    esac
done

inotifywait -m -r -e modify,delete,create,move --format '%e:%w%f' "$fuzz_out_path" | while read f
do
    ext=${f:(-5):5}
    head=(${f//:/ })
    value=${head[0]}

    if [[ "$ext" == "t.txt" ]] && ([[ "$value"=="CREATE" ]] || [[ "$value"=="MODIFY" ]])
    then
        # echo $f,$ext
       # echo head=${head[0]}
       echo "[+]$f has been produced."
        python3 ../dynamic_adjustment/AICFG_flow.py $target_program_path $fuzz_out_path
        echo "[+]ACG wl subgraph over."
    fi
done
