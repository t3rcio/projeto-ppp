#!/bin/bash

MAX=0
MIN=0

function help(){
    # Exibe o texto de ajuda do script
    echo
    echo "Use: between-msgs.sh [input] [options]: "
    echo "Retorna os usuarios dentro da faixa de mensagens indicada em [MIN] e [MAX]"
    echo "Options:"
    echo "    no options: imprime a ajuda (help) "
    echo "    MIN - use para indicar o menor valor de mensagens"
    echo "    MAX - use para indicar o maior valor de mensagens"
    echo
    exit

}
if [ "$1" == '' ] || [ "$1" == 'help' ]; then
    help
fi

MAX=$3
MIN=$2

if [ "$3" -lt "$2" ]; then
    MAX=$2
    MIN=$3
fi

while read -r -a linha; do
    msgs="${linha[2]}"
    if [ "$msgs" -ge "$MIN" ] && [ "$msgs" -le "$MAX" ]; then
        echo "${linha[*]}"
    fi

done < $1

