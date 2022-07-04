#!/usr/bin/env bash

BASEDIR=$(dirname "$0")
REFDIR=ref


function result() {
    local fgcolor=$1
    local bgcolor=1
    local text=$2
    local code=""

    case "${fgcolor}" in
        r*) code="\033[${bgcolor};31m" ;;  # Red
        g*) code="\033[${bgcolor};32m" ;;  # Green
        y*) code="\033[${bgcolor};33m" ;;  # Yellow
        b*) code="\033[${bgcolor};34m" ;;  # Blue
        p*) code="\033[${bgcolor};35m" ;;  # Purple
        c*) code="\033[${bgcolor};36m" ;;  # Cyan
        w*) code="\033[${bgcolor};37m" ;;  # White
    esac

    echo -e "[${code}${text}\033[0m]" "${3-}"
}


function test-script() {
    local reference="${REFDIR}/${1}" && shift
    local exitcode=0
    local cw=64
    local rw=32

    if ! [[ -e "$reference" ]]; then
        echo "$reference does not exist, generating..."
        mkdir -p $(dirname "$reference")
        "$@" > "$reference"
    fi

    printf "%-*s => %-*s .. " $cw "$*" $rw "$reference"
    if diff "$reference" <("$@" 2>&1) >&/dev/null; then
        result green "PASS"
    else
        result red "FAIL"
        exitcode=1
    fi

    return $exitcode
}


function test-csvalign() {
    local file
    local ext

    for file in empty typical complex; do
        local suffix

        # Simple options
        for ext in csv psv tsv; do
            test-script csvalign_${file} csvalign ${file}.${ext}
            test-script csvalign_${file}_n csvalign -n ${file}.${ext}
            test-script csvalign_${file}_n csvalign --number ${file}.${ext}
            test-script csvalign_${file}_p csvalign -p' | ' ${file}.${ext}
            test-script csvalign_${file}_p csvalign --padding=' | ' ${file}.${ext}
            test-script csvalign_${file}_w1 csvalign -w1 ${file}.${ext}
            test-script csvalign_${file}_w1 csvalign --width=1 ${file}.${ext}
            test-script csvalign_${file}_w7 csvalign -w7,13,31 ${file}.${ext}
            test-script csvalign_${file}_w7 csvalign --width=7,13,31 ${file}.${ext}

            test-script csvalign_${file}_np csvalign -np ' | ' ${file}.${ext}
            test-script csvalign_${file}_np csvalign --number --padding=' | ' ${file}.${ext}
            test-script csvalign_${file}_nw7 csvalign -nw7,13,31 ${file}.${ext}
            test-script csvalign_${file}_nw7 csvalign --number --width=7,13,31 ${file}.${ext}
            test-script csvalign_${file}_npw7 csvalign -np ' | ' -w7,13,31 ${file}.${ext}
            test-script csvalign_${file}_npw7 csvalign --number --padding=' | ' --width=7,13,31 ${file}.${ext}
        done

        # Manual delimiter
        test-script csvalign_${file} csvalign -d^ ${file}.rsv
        test-script csvalign_${file}_n csvalign -d^ -n ${file}.rsv
        test-script csvalign_${file}_n csvalign --delim=^ --number ${file}.rsv
        CSV_DELIMS=^ test-script csvalign_${file} csvalign ${file}.rsv
        CSV_DELIMS=^ test-script csvalign_${file}_n csvalign -n ${file}.rsv
        CSV_DELIMS=^ test-script csvalign_${file}_n csvalign --number ${file}.rsv

        # Multitable
        if [[ "$file" == "complex" ]]; then
            suffix="_m"
        fi
        test-script csvalign_${file}${suffix-} csvalign -m ${file}.csv
        test-script csvalign_${file}${suffix-} csvalign --multitable ${file}.csv
        test-script csvalign_${file}${suffix-_}n csvalign -nm ${file}.csv
        test-script csvalign_${file}${suffix-_}n csvalign --number --multitable ${file}.csv
    done
}


function test-csvcut() {
    local extrasuffix=$1
    local extraopts=$2
    local file
    local -A colcount=(
        [empty]=0
        [typical]=6
        [complex]=4
    )
    local -A firstcolname=(
        [empty]=""
        [typical]="ID"
        [complex]="FIRST_NAME"
    )
    local -A lastcolname=(
        [empty]=""
        [typical]="TEL"
        [complex]="EMAIL"
    )
    local -A allcolnames=(
        [empty]=""
        [typical]="ID,FIRST_NAME,LAST_NAME,NOTES,EMAIL,TEL"
        [complex]="FIRST_NAME,LAST_NAME,NOTES,EMAIL"
    )

    for file in empty typical complex; do
        local lastnum=${colcount[$file]}
        local firstname=${firstcolname[$file]}
        local lastname=${lastcolname[$file]}
        local allnums=$(echo $(seq 1 $lastnum) ) && allnums=${allnums// /,}
        local allnumsbut=$(echo $(seq 1 $((lastnum-1)) ) ) && allnumsbut=${allnumsbut// /,}
        local allnames=${allcolnames[$file]}
        local suffix

        # Delimiters
        test-script csvcut_${file}_two_csv${extrasuffix} csvcut ${extraopts} -f1-2 ${file}.csv
        test-script psvcut_${file}_two_psv${extrasuffix} csvcut ${extraopts} -f1-2 ${file}.psv
        test-script tsvcut_${file}_two_tsv${extrasuffix} csvcut ${extraopts} -f1-2 ${file}.tsv
        test-script csvcut_${file}_two_rsv${extrasuffix} csvcut ${extraopts} -f1-2 -d^ ${file}.rsv
        test-script csvcut_${file}_two_rsv${extrasuffix} csvcut ${extraopts} -f1-2 --delim=^ ${file}.rsv
        CSV_DELIMS=^ test-script csvcut_${file}_two_rsv${extrasuffix} csvcut ${extraopts} -f1-2 ${file}.rsv

        # RANGE
        test-script csvcut_${file}_all${extrasuffix} csvcut ${extraopts} -f- ${file}.csv
        test-script csvcut_${file}_all${extrasuffix} csvcut ${extraopts} -f1- ${file}.csv
        test-script csvcut_${file}_all${extrasuffix} csvcut ${extraopts} -f1,2- ${file}.csv
        test-script csvcut_${file}_all${extrasuffix} csvcut ${extraopts} -f1-$lastnum ${file}.csv
        test-script csvcut_${file}_all${extrasuffix} csvcut ${extraopts} -f1,2-$lastnum ${file}.csv
        test-script csvcut_${file}_all${extrasuffix} csvcut ${extraopts} -f "$allnums" ${file}.csv
        test-script csvcut_${file}_all${extrasuffix} csvcut ${extraopts} -f "${allnumsbut},${lastnum}" ${file}.csv
        test-script csvcut_${file}_all${extrasuffix} csvcut ${extraopts} -f "${allnumsbut},${lastname}" ${file}.csv
        test-script csvcut_${file}_all${extrasuffix} csvcut ${extraopts} -f "${allnames}" ${file}.csv

        # REGEX
        test-script csvcut_${file}_all${extrasuffix} csvcut ${extraopts} -f/./ ${file}.csv
        test-script csvcut_${file}_all${extrasuffix} csvcut ${extraopts} -f/^${firstname}/,2- ${file}.csv
        test-script csvcut_${file}_all${extrasuffix} csvcut ${extraopts} -f/^${firstname^^}/i,2- ${file}.csv
        test-script csvcut_${file}_all${extrasuffix} csvcut ${extraopts} -f/^${firstname,,}/i,2- ${file}.csv
        test-script csvcut_${file}_all${extrasuffix} csvcut ${extraopts} -f1-$((lastnum-1)),/$lastname/ ${file}.csv

        # COLNUM, COLNAME
        test-script csvcut_${file}_one${extrasuffix} csvcut ${extraopts} -f ${lastnum} ${file}.csv
        test-script csvcut_${file}_one${extrasuffix} csvcut ${extraopts} -f "${lastname}" ${file}.csv
        test-script csvcut_${file}_one${extrasuffix} csvcut ${extraopts} --fields=${lastnum} ${file}.csv
        test-script csvcut_${file}_one${extrasuffix} csvcut ${extraopts} --fields="${lastname}" ${file}.csv

        # -COLNUM
        if [[ "$file" == "complex" ]]; then
            suffix="last"
        else
            suffix="one"
        fi
        test-script csvcut_${file}_${suffix}${extrasuffix} csvcut ${extraopts} -f-1 ${file}.csv
        test-script csvcut_${file}_${suffix}${extrasuffix} csvcut ${extraopts} --fields=-1 ${file}.csv
    done
}


function test-csvread() {
    local file
    local ext

    for file in empty typical complex; do
        local suffix

        # Delimiters
        test-script csvread_${file} csvread ${file}.csv
        test-script csvread_${file} csvread ${file}.psv
        test-script csvread_${file} csvread ${file}.tsv
        test-script csvread_${file} csvread -d^ ${file}.rsv
        test-script csvread_${file} csvread --delim=^ ${file}.rsv
        CSV_DELIMS=^ test-script csvread_${file} csvread ${file}.rsv

        # Short options
        test-script csvread_${file}_n csvread -n ${file}.csv
        test-script csvread_${file}_s csvread -s ${file}.csv
        test-script csvread_${file}_ns csvread -ns ${file}.csv

        # Long options
        test-script csvread_${file}_n csvread --no-header ${file}.csv
        test-script csvread_${file}_s csvread --strip-quotes ${file}.csv
        test-script csvread_${file}_ns csvread --no-header --strip-quotes ${file}.csv

        # Multitable
        if [[ "$file" == "complex" ]]; then
            suffix="_m"
        fi

        test-script csvread_${file}${suffix-} csvread -m ${file}.csv
        test-script csvread_${file}${suffix-_}n csvread -nm ${file}.csv
        test-script csvread_${file}${suffix-_}s csvread -sm ${file}.csv
        test-script csvread_${file}${suffix-_}ns csvread -nsm ${file}.csv

        test-script csvread_${file}${suffix-} csvread --multitable ${file}.csv
        test-script csvread_${file}${suffix-_}n csvread --no-header --multitable ${file}.csv
        test-script csvread_${file}${suffix-_}s csvread --strip-quotes --multitable ${file}.csv
        test-script csvread_${file}${suffix-_}ns csvread --no-header --strip-quotes --multitable ${file}.csv
    done

    for ext in csv psv raw; do
        test-script csvread_fix csvread -ntfix fixmessages.$ext
        test-script csvread_fix csvread --no-header --translator=fix fixmessages.$ext
    done

    for ext in csv psv tsv; do
        test-script csvread_diff_f csvread --diff-only diff-order.$ext
        test-script csvread_diff_g csvread --show-change diff-order.$ext
    done

    for ext in csv psv raw; do
        test-script csvread_diff_fix_f csvread -ntfix -f diff-fixmessages.$ext
        test-script csvread_diff_fix_g csvread -ntfix -g diff-fixmessages.$ext
    done
}


function test-csvgrep() {
    local -A opts=(
        [_]=""
        [_]="-i"
        [_k]="-k"
        [_n]="-n"
        [_v]="-v"
    )
    local -A patterns=(
        [_]=""
        [_dot]="."
        [_not]="notinanyfile"
        [_blank]="^$"
    )
    local ok

    for ok in "${!opts[@]}"; do
        local opt=${opts[${ok}]}
        local pk

        for pk in "${!patterns[@]}"; do
            local pattern=${patterns[${pk}]}
            local fields

            # All of these fields should be equivalent
            for fields in "" "-f1-" "-f/./"; do
                test-script csvgrep_empty${ok}${pk}    csvgrep    $opt $fields "$pattern" empty.csv
                test-script csvgrep_typical${ok}${pk}  csvgrep    $opt $fields "$pattern" typical.csv
                test-script csvgrep_complex${ok}${pk}  csvgrep    $opt $fields "$pattern" complex.csv
                test-script csvgrep_complex${ok}m${pk} csvgrep -m $opt $fields "$pattern" complex.csv
            done
        done
    done

    opts=(
        [_]=""
        [_v]="-v"
        [_i]="-i"
        [_iv]="-iv"
        [_ik]="-ik"
        [_ivk]="-ivk"
    )

    for ok in "${!opts[@]}"; do
        local opt=${opts[${ok}]}

        test-script csvgrep_typical${ok}_email  csvgrep    $opt -f/email/i '^JDOE@EMAIL.COM$' typical.csv
        test-script csvgrep_complex${ok}_email  csvgrep    $opt -f/email/i '^JDOE@EMAIL.COM$' complex.csv
        test-script csvgrep_complex${ok}m_email csvgrep -m $opt -f/email/i '^JDOE@EMAIL.COM$' complex.csv

        test-script csvgrep_typical${ok}_badisin  csvgrep    $opt -fISIN '^JDOE@EMAIL.COM$' typical.csv
        test-script csvgrep_complex${ok}_badisin  csvgrep    $opt -fISIN '^JDOE@EMAIL.COM$' complex.csv
        test-script csvgrep_complex${ok}m_badisin csvgrep -m $opt -fISIN '^JDOE@EMAIL.COM$' complex.csv
    done
}


function main() {
    cd "$BASEDIR"

    test-csvalign
    test-csvcut
    test-csvcut "_inv" "-v"
    test-csvread
    test-csvgrep
}


main "$@"

