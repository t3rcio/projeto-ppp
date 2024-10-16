#!/bin/bash

MAIOR_INBOX_SIZE=0;
MENOR_INBOX_SIZE=0;
ARG_MIN="-min"
ARG_MAX="-max"
USER="";

function help(){
    # Exibe o texto de ajuda do script
    echo
    echo "Use: max-min-size [input] [options]: Retorna o usuario com maior size"
    echo "Options:"
    echo "    no options: Retorna o usuario com maior size"
    echo "    -max: Retorna o usuario com maior size"
    echo "    -min: Retorna o usuario com menor size"
    echo
    exit

}
if [ "$1" == '' ] || [ "$1" == 'help' ]; then
    help
fi

read -r -a primeiraLinha fL<$1
MENOR_INBOX_SIZE=${primeiraLinha[4]}

while read -r -a linha; do
    size="${linha[4]}"
    case $2 in
        
        "help")
        help
        ;;
        
        "$ARG_MAX" | "")
            if [ "$size" -gt "$MAIOR_INBOX_SIZE" ]; then
                USER="${linha[*]}"
                MAIOR_INBOX_SIZE=$size
            fi
        ;;

        "$ARG_MIN")
            if [ "$size" -lt "$MENOR_INBOX_SIZE" ]; then
                USER="${linha[*]}"
                MENOR_INBOX_SIZE=$size
            fi
        ;;
    esac

done < $1
echo $USER
